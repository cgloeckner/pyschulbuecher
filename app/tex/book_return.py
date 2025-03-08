import os
import bottle

from app.db import book_queries as books, orga

from app.tex.compiler import compile_pdf


class BookreturnPdf(object):

    def __init__(self, settings, export='export'):
        # load LaTeX templates
        with open('docs/bookreturn/header.tpl') as f:
            self.header = f.read()
        with open('docs/bookreturn/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/bookreturn/content.tpl') as f:
            self.content = f.read()
        with open('docs/bookreturn/overview.tpl') as f:
            self.overview = f.read()
        # prepare output directory
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = settings

        self.tex = bottle.template(self.header)

    def getPath(self):
        return os.path.join(self.export, 'Rückgaben.pdf')

    def addOverview(self, grade):
        """Generate overviews for class teachers about returning books.
        """
        # fetch and order books that are used next year by this class
        bks = books.get_books_finished_in(grade)
        bks = books.order_books_list(bks)

        # render template
        self.tex += bottle.template(self.overview, s=self.s, grade=grade, bks=bks)

    def __call__(self, class_):
        """Generate requestlist pdf file for the given class.
        """
        # fetch and order books that are used next year by this class
        bks = books.get_books_finished_in(class_.grade)
        bks = books.order_books_list(bks)

        # query students
        students = orga.get_students_in(class_.grade, class_.tag)

        # render template
        self.tex += bottle.template(self.content, s=self.s, class_=class_, bks=bks, students=students)

    def saveToFile(self):
        self.tex += bottle.template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'Rückgaben.tex')
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname)

