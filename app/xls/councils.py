import os
import xlsxwriter

from app.db import books


class SubjectCouncilXls(object):
    def __init__(self, settings, export='export'):
        # prepare output directory
        if not os.path.isdir(export):  # base dir
            os.mkdir(export)
        self.export = os.path.join(export, 'councils')
        if not os.path.isdir(self.export):  # councils dir
            os.mkdir(self.export)
        # load settings
        self.s = settings
        self.data = None

    def getPath(self, subject):
        return os.path.join(self.export, '%s.xlsx' % subject.tag)

    def __call__(self, subject):
        self.data = xlsxwriter.Workbook(self.getPath(subject))

        """items = {
            'Leihbuch': books.get_real_books_by_subject(subject, False),
            'AH': books.get_workbooks_by_subject(subject),
            'Klassensatz': books.get_classsets_by_subject(subject)
        }"""
        
        all_books = books.order_books_index(books.get_all_books())

        title_format = self.data.add_format()
        title_format.set_bold()

        euro_format = self.data.add_format({'num_format': '#,##0.00€'})

        center_format = self.data.add_format()
        center_format.set_align('center')

        tab = self.data.add_worksheet(subject.tag)
        tab.set_landscape()
        tab.set_footer('Bücherbedarf &A (Stand &D)')
        tab.set_margins(top=1.25)

        tab.set_column(0, 0, 25)
        tab.set_column(1, 1, 20)
        tab.set_column(2, 2, 20)
        tab.set_column(3, 3, 8, euro_format)
        tab.set_column(4, 4, 8, center_format)
        tab.set_column(5, 5, 10, center_format)
        tab.set_column(6, 6, 25)

        for col, caption in enumerate(
                ['Titel', 'Verlag', 'ISBN', 'Preis', 'Klasse', 'Art', 'Bemerkungen']):
            tab.write(0, col, caption, title_format)

        row = 0
        for b in all_books:
            if b.subject != subject:
                continue
            
            if b.workbook:
                kind = 'Arbeitsheft'
            elif b.classsets:
                kind = 'Klassensatz'
            else:
                kind = 'Leihbuch'
            tab.write(row + 1, 0, b.title)
            if b.publisher is not None:
                tab.write(row + 1, 1, b.publisher.name)
            if b.isbn is not None:
                tab.write(row + 1, 2, b.isbn)
            if b.price is not None:
                tab.write(row + 1, 3, b.price / 100.0)
            if b.inGrade == b.outGrade:
                tab.write(row + 1, 4, b.inGrade)
            else:
                tab.write(row + 1, 4, '%d-%d' % (b.inGrade, b.outGrade))
            tab.write(row + 1, 5, kind)

            comments = list()
            if b.comment != '':
                comments.append(b.comment)
            if b.novices:
                comments.append('gA')
            if b.advanced:
                comments.append('eA')
            tab.write(row + 1, 6, ' '.join(comments))

            row += 1

    def saveToFile(self):
        assert(self.data is not None)
        self.data.close()
