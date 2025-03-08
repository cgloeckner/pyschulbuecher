import os
import bottle

from app.db import loan_queries as loans

from app.tex.compiler import compile_pdf



class LoanContractPdf(object):
    def __init__(
            self,
            prefix,
            settings,
            export='export',
            advance=False):
        # load LaTeX templates
        with open('docs/loancontract/header.tpl') as f:
            self.header = f.read()
        with open('docs/loancontract/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/loancontract/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.prefix = prefix
        if not os.path.isdir(export):  # base dir
            os.mkdir(export)
        self.export = os.path.join(export, 'contracts')
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.export):  # specific dir
            os.mkdir(self.export)
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = settings

        self.tex = bottle.template(self.header)
        self.advance = advance

    def getPath(self):
        return os.path.join(self.export, 'Leihverträge_%s.pdf' % self.prefix)

    def __call__(self, student, include_requests=False, loan_report=False):
        """Generate loan contract pdf file for the given student. This contains
        all books that are currently given to him or her. With 'loan_report'
        all books are listed as "you loan these books"
        """
        lns = loans.order_loan_overview(student.person.loan)
        rqs = list()
        if include_requests:
            rqs = loans.order_request_overview(student.person.request)
        self.tex += bottle.template(
            self.content, s=self.s, student=student, lns=lns, rqs=rqs, advance=self.advance,
            loan_report=loan_report
        )

    def saveToFile(self):
        self.tex += bottle.template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(
            self.texdir,
            'Leihverträge_%s.tex' %
            self.prefix)
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname)
