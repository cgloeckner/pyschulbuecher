import os
import bottle

from app.tex.compiler import compile_pdf


class ClassListPdf(object):
    def __init__(self, settings, export='export'):
        # load LaTeX templates
        with open('docs/classlist/header.tpl') as f:
            self.header = f.read()
        with open('docs/classlist/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/classlist/content.tpl') as f:
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
        return os.path.join(self.export, 'Klassenliste.pdf')

    def __call__(self, classes):
        """Add classes to the listing
        """
        self.tex += bottle.template(self.content, s=self.s, classes=classes)

    def saveToFile(self):
        self.tex += bottle.template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'Klassenliste.tex')
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        compile_pdf(self.s.data['hosting']['remote_latex'], self.tex, fname) 
