import os
import xlsxwriter

from app.utils import shortify_name

from app.db import books, orga


class DatabaseDumpXls(object):
    def __init__(self, settings, export='export'):
        # prepare output directory
        if not os.path.isdir(export):  # base dir
            os.mkdir(export)
        self.export = export
        # load settings
        self.s = settings
        # setup xlsx file
        path = os.path.join(
            self.export, '%s.xlsx' %
            self.s.data['general']['school_year'])
        self.data = xlsxwriter.Workbook(path)

    def getPath(self):
        return os.path.join(
            self.export, '%s.xlsx' %
            self.s.data['general']['school_year'])

    def __call__(self, class_, bks):
        # local import to avoid cycles
        from app.db import loan_queries as loans

        # pre-order students abd books
        bks = books.order_books_list(bks)
        students = list(class_.student)
        orga.sort_students(students)

        title_format = self.data.add_format()
        title_format.set_bold()

        rotate_format = self.data.add_format()
        rotate_format.set_rotation(90)

        # create tab sheet for this class
        tab = self.data.add_worksheet(class_.to_string())
        tab.set_column(0, 1, 12)
        tab.set_column(2, 2 + len(bks), 4)
        tab.set_row(0, 150, rotate_format)

        fields = ['Name', 'Vorname']
        for col, b in enumerate(bks):
            fields.append(b.subject.tag if b.subject is not None else '')
            tab.write(0, col + 2, b.title)  # todo: 90° rotated format
        for col, caption in enumerate(fields):
            tab.write(1, col, caption, title_format)

        # fill students in
        for row, s in enumerate(students):
            tab.write(row + 2, 0, s.person.name)
            tab.write(row + 2, 1, shortify_name(s.person.firstname))
            for col, b in enumerate(bks):
                n = loans.get_loan_count(s.person, b)
                tab.write(row + 2, col + 2, n if n > 0 else '')

    def saveToFile(self):
        assert(self.data is not None)
        self.data.close()
