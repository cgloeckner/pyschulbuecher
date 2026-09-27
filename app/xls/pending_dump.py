import os
import xlsxwriter

from app.db import orga_queries, book_queries
from app.db.orm import db


class PendingDumpXls(object):
    def __init__(self, export="export"):
        # prepare output directory
        if not os.path.isdir(export):  # base dir
            os.mkdir(export)
        self.export = export
        # setup xlsx file
        self.data = xlsxwriter.Workbook(self.getPath())

    def getPath(self):
        return f"{self.export}/pending.xlsx"

    def __call__(self, data):
        tab = self.data.add_worksheet("ausstehend")

        fields = ["Klasse", "Name", "Vorname", "Bücher"]
        for index, label in enumerate(fields):
            tab.write(0, index, label)
        
        row = 1
        for class_, subdata in data.items():
            for student, booklist in subdata.items():
                books = ", ".join([
                    book_queries.get_shorthand(book)
                    for book in booklist
                ])
                tab.write(row, 0, class_.to_string())
                tab.write(row, 1, student.person.name)
                tab.write(row, 2, student.person.firstname)
                tab.write(row, 3, books)
                row += 1
        
    def saveToFile(self):
        assert(self.data is not None)
        self.data.close()

