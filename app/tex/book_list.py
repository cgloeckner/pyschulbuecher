import os
import bottle

from app.db import book_queries as books

from app.tex.compiler import compile_pdf


class BooklistPdf(object):
    def __init__(self, settings, export='export'):
        # load LaTeX templates
        with open('docs/booklist/header.tpl') as f:
            self.header = f.read()
        with open('docs/booklist/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/booklist/info.tpl') as f:
            self.info = f.read()
        with open('docs/booklist/select.tpl') as f:
            self.select = f.read()
        with open('docs/booklist/empty.tpl') as f:
            self.empty = f.read()
        with open('docs/booklist/special.tpl') as f:
            self.special = f.read()
        # prepare output directory
        if not os.path.isdir(export):  # base dr
            os.mkdir(export)
        self.export = os.path.join(export, 'booklists')
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.export):  # specific dir
            os.mkdir(self.export)
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = settings

    def __call__(self, grade: int, exclude: set, new_students: bool = False):
        """Generate booklist pdf file for the given grade. A separate booklist
        can be generated for new_students, which include additional books other
        students already have from earlier classes.
        The provided exclude set can be used to exclude books from the
        booklist. The keys are built from <grade>_<bookid>, if excluded this
        key's value is set to false.
        """
        # fetch special books
        spec_bks = books.get_books_used_in(0, True)

        # fetch and order books
        if new_students:
            bks = books.get_books_used_in(grade, booklist=True)
            suffix = '_Neuzugänge'
            deadline = 'Abgabe bei Anmeldung'
        else:
            bks = books.get_books_started_in(grade, booklist=True)
            suffix = ''
            date = self.s.data['deadline']['booklist_return']
            year = int(self.s.data['general']['school_year'])
            deadline = f'Abgabe bis spätestens {date}{year+1}'
        bks = books.order_books_list(bks)
        if grade == 5:
            deadline = 'Abgabe bei Anmeldung'

        # determine number of books
        num_books = sum(1 for b in bks if not b.workbook)

        # render templates
        tex = bottle.template(self.header, s=self.s, grade=grade, new_students=new_students, deadline=deadline)
        # render pure books
        if num_books > 0:
            tex += bottle.template(
                self.select, grade=grade, bs=bks, workbook=False, exclude=exclude, new_students=new_students
            )
        else:
            tex += bottle.template(self.empty, workbook=False, new_students=new_students)
        # render pure workbooks
        if num_books < len(bks):
            tex += bottle.template(
                self.select, grade=grade, bs=bks, workbook=True, exclude=exclude, new_students=new_students
            )
        else:
            tex += bottle.template(self.empty, workbook=True, new_students=new_students)
        tex += bottle.template(self.special, grade=grade, s=self.s, spec_bks=spec_bks)
        tex += bottle.template(self.footer, s=self.s)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, '%d_%s.tex' % (grade, suffix))
        with open(dbg_fname, 'w') as h:
            h.write(tex)

        # export PDF
        fname = os.path.join(
            self.export, 'Bücherzettel%d%s.pdf' %
            (grade, suffix))
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname)

    def infosheet(self):
        # render templates
        tex = bottle.template(self.info, s=self.s)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'info.tex')
        with open(dbg_fname, 'w') as h:
            h.write(tex)

        # export PDF
        fname = os.path.join(self.export, 'Bücherzettel_Information.pdf')
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname)
