import os
import datetime
import bottle

from db import books, loans

from app.tex.compiler import compile_pdf


class BookpendingPdf(object):

    def __init__(self, settings, export='export'):
        # load LaTeX templates
        with open('docs/bookpending/header.tpl') as f:
            self.header = f.read()
        with open('docs/bookpending/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/bookpending/page_header.tpl') as f:
            self.page_header = f.read()
        with open('docs/bookpending/page_footer.tpl') as f:
            self.page_footer = f.read()
        with open('docs/bookpending/page_content.tpl') as f:
            self.page_content = f.read()
        # prepare output directory
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        self.export = os.path.join(export, 'pending')
        if not os.path.isdir(self.export):
            os.mkdir(self.export)
        # load settings
        self.s = settings

        self.tex = bottle.template(self.header)

        self.n = 0

    def queryBooks(self, grade: int, tooLate=False):
        """Query and add all pending books for the given grade.
        """
        if tooLate:
            def test(l): return l.tooLate()
        else:
            def test(l): return l.isPending()

        n = 0
        # iterate students in classes in grade
        for b in books.getBooksFinishedIn(grade):
            k = 0
            # ignore class sets
            if b.classsets:
                continue
            # add all pending loan records
            page = bottle.template(self.page_header, book=b)
            for l in loans.queryLoansByBook(b):
                # add if pending
                if test(l):
                    page += bottle.template(self.page_content, l=l, i=k)
                    k += 1
            page += bottle.template(self.page_footer)
            # add page to document if at least one student was found
            if k > 0:
                self.tex += page
            n += k

        return n

    def saveToFile(self, suffix, with_date=False):
        self.tex += bottle.template(self.footer)

        ext = ''
        if with_date:
            ext = '_%s' % datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        pdfname = 'AusstehendeBücher_%s%s' % (suffix, ext)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, '%s.tex' % pdfname)
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = os.path.join(self.export, '%s.pdf' % pdfname)
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname)

        return pdfname
