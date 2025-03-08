import os
import bottle

from app.db import book_queries as books
from app.db import loan_queries as loans

from app.tex.compiler import compile_pdf


class InventoryReport(object):
    def __init__(self, settings, export='export'):
        # load LaTeX templates
        with open('docs/inventoryreport/header.tpl') as f:
            self.header = f.read()
        with open('docs/inventoryreport/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/inventoryreport/content.tpl') as f:
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
        return os.path.join(self.export, 'Inventarbericht.pdf')

    def __call__(self):
        """Collect all books (existing, loaned, remaining)
        """
        all_bks = books.get_real_books()
        all_bks = books.order_books_index(all_bks)

        loan_count = dict()
        for b in all_bks:
            loan_count[b] = loans.get_loan_count(person=None, book=b)

        self.tex += bottle.template(self.content, s=self.s, all_bks=all_bks, loan_count=loan_count)

    def saveToFile(self):
        self.tex += bottle.template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'Inventarbericht.tex')
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname)
