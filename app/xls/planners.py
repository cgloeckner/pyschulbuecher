import os
import xlsxwriter

from db.orm import db


class PlannerXls(object):
    def __init__(self, export='export'):
        # prepare output directory
        if not os.path.isdir(export):  # base dir
            os.mkdir(export)
        self.fname = 'planner.xlsx'
        self.path = os.path.join(export, self.fname)
        self.data = xlsxwriter.Workbook(self.path)

    def __call__(self, classes, advance):
        tab = self.data.add_worksheet('Schulplaner')

        title_format = self.data.add_format()
        title_format.set_bold()
        title_format.set_align('center')

        center_format = self.data.add_format()
        center_format.set_align('center')

        tab.set_column(0, 0, 10, center_format)
        tab.set_column(1, 1, 10, center_format)
        tab.write(0, 0, 'Klasse', title_format)
        tab.write(0, 1, 'Anzahl', title_format)

        # query planner
        planner = db.Book.select(
            lambda b: b.publisher.name == 'schulintern').first()

        row = 1
        for c in classes:
            n = 0
            for s in c.student:
                for l in s.person.request:
                    if l.book == planner:
                        n += 1
                        break
            tab.write(row, 0, c.to_string(advance=advance))
            tab.write(row, 1, n)
            row += 1

    def saveToFile(self):
        assert(self.data is not None)
        self.data.close()
