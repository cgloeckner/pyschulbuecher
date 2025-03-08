import os
import bottle

from db import loans

from app.tex.compiler import compile_pdf


class LoanReportPdf(object):
    def __init__(self, prefix, settings, export='export'):
        # load LaTeX templates
        with open('docs/loanreport/header.tpl') as f:
            self.header = f.read()
        with open('docs/loanreport/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/loanreport/content.tpl') as f:
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

    def getPath(self):
        return os.path.join(self.export, 'Leihübersicht_%s.pdf' % self.prefix)

    def __call__(self, person):
        """Generate loan report pdf file for the given person. This will contain
        all books that are currently given to this person
        """
        lns = loans.orderLoanOverview(person.loan)
        self.tex += bottle.template(self.content, s=self.s, p=person, lns=lns)

    def saveToFile(self):
        self.tex += bottle.template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(
            self.texdir,
            'Leihübersicht_%s.tex' %
            self.prefix)
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname)
