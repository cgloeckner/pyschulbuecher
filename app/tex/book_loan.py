import os
import bottle

from app.db import book_queries as books
from app.db import loan_queries as loans
from app.db import orga_queries as orga

from app.tex.compiler import compile_pdf


class BookloanPdf(object):

    def __init__(self, settings, export='export'):
        # load LaTeX templates
        with open('docs/bookloan/header.tpl') as f:
            self.header = f.read()
        with open('docs/bookloan/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/bookloan/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = settings

        self.tex = bottle.template(self.header)

    def getPath(self):
        return os.path.join(self.export, 'Ausgaben.pdf')

    def __call__(self, class_, request=False):
        """Generate requestlist pdf file for the given class. If `requests` is
        provided with true, the request list for this year is used.
        """
        grade = class_.grade
        if request:
            grade += 1

        # fetch and order books that were requested by this class
        bks = books.get_books_used_in(grade)
        bks = books.order_books_list(bks)

        # fetch special books
        spec_bks = books.get_books_used_in(0, True)

        # query students
        students = orga.get_students_in(class_.grade, class_.tag)

        if request:
            query_func = loans.get_request_count
        else:
            query_func = loans.get_loan_count

        # render template
        self.tex += bottle.template(
            self.content, s=self.s, class_=class_, bks=bks, students=students, spec_bks=spec_bks,
            query_func=query_func, advance=request
        )

    def saveToFile(self):
        self.tex += bottle.template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'Ausgaben.tex')
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname)
