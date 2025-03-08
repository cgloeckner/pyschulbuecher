import os
import bottle

from db import loans

from app.tex.compiler import compile_pdf


class ClasssetsPdf(object):
    def __init__(self, prefix, settings, threshold, export='export'):
        """ All books, that are either class sets or if more than `threshold`
        pieces are loaned by a person, are written to the PDF. """
        # load LaTeX templates
        with open('docs/classsets/header.tpl') as f:
            self.header = f.read()
        with open('docs/classsets/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/classsets/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.prefix = prefix
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = settings

        self.tex = bottle.template(self.header)
        self.threshold = threshold

        # used to page break not too often
        self.page_count = 0

    def getPath(self):
        return os.path.join(self.export, 'Klassensätze_%s.pdf' % self.prefix)

    def __call__(self, person):
        """Generate loan report pdf file for the given person. This will contain
        all books that are currently given to this person
        """
        # count books before running template
        lns = loans.orderLoanOverview(person.loan)
        n = 0
        for l in lns:
            if l.count > self.threshold:
                n += 1

        if n > 0:
            self.page_count += 1
            # run template only if books are relevant
            self.tex += bottle.template(
                self.content, s=self.s, p=person, lns=lns, threshold=self.threshold,
                pagebreak=self.page_count % 2 == 0
            )

    def saveToFile(self):
        self.tex += bottle.template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(
            self.texdir,
            'Klassensätze_%s.tex' %
            self.prefix)
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname)
