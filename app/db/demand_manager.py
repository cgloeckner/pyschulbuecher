import json

from app.db import orga_queries as orga
from app.db import book_queries as books
from app.db import db

from pony.orm import *


class DemandManager(object):

    def __init__(self, grade_query=orga.get_students_count, filename: str = './demand.json'):
        self.data = dict()
        self.grade_query = grade_query
        self.filename = filename

    def parse(self, forms):
        """Parse demand data from a form. The given forms parameter is a
        function handle with __call__(key), where key is a UI-related name tag.
        """
        # note: str(grade) because json will dump to str it anyway
        # parse student numbers for elective subjects (until 10th grade)
        tmp = dict()
        for grade in orga.get_secondary_level1_range():
            tmp[str(grade)] = dict()
            for sub in books.get_subjects(elective=True):
                key = "%d_%s" % (grade, sub.tag)
                val = forms(key)
                tmp[str(grade)][sub.tag] = int(val) if val != "" else 0
        # parse student numbers for each subject (after 11th grade)
        for grade in orga.get_secondary_level2_range():
            tmp[str(grade)] = dict()
            for sub in books.get_subjects():
                tmp[str(grade)][sub.tag] = dict()
                for level in ['novices', 'advanced']:
                    key = "%d_%s_%s" % (grade, sub.tag, level)
                    val = forms(key)
                    tmp[str(grade)][sub.tag][level] = int(
                        val) if val != "" else 0
        # overwrite internal data
        self.data = tmp

    def get_unavailable_books_count(self, book):
        """Return total amount of books that are continued to be in use during
        the next school year.
        """
        continued = 0
        for l in book.loan:
            if l.person.student is None:
                # count teacher books
                continued += l.count
            elif l.person.student.class_.grade < book.outGrade:
                # count student books
                continued += l.count
        return continued

    def count_books_in_use(self, book):
        """Return total amount of books that will be used after the end of this
        school year. Expected returns are not included, as well as requested
        books.
        """
        in_use = 0
        for l in book.loan:
            if l.person.student is None:
                # teacher books are in use
                in_use += l.count
            elif l.person.student.class_.grade < book.outGrade:
                # student books are in use if loan is continued
                in_use += l.count
        return in_use

    # @TODO für Klassensätze nutzen?!
    def get_student_number(
            self,
            grade: int,
            subject: db.Subject,
            level: str = None):
        """Return total number of students for the given grade and subject.
        Optionally specified novice and/or advanced courses are considered.
        """
        # note: str(grade) because json will dump to str it anyway
        assert level in [None, 'novices', 'advanced']

        if str(grade) not in self.data:
            # no such grade (maybe there is not 8th grade this year)
            return 0
        if subject.tag not in self.data[str(grade)]:
            # no such subject (maybe there is no french class in this grade)
            # note that the n th grade is currently (n-1)th grade
            return self.grade_query(grade - 1)

        if level is None:
            # consider regular class
            return self.data[str(grade)][subject.tag]
        else:
            # consider course levels
            return self.data[str(grade)][subject.tag][level]

    # @TODO für Klassensätze nutzen?!
    def get_max_demand(self, book: db.Book):
        """Calculate worst case demand of the given book assuming.
        Note that this calculates the demand for the NEXT year, so all grades
        are considerd -1.
        E.g. the new 10th grade is currently 9th grade now.
        """
        total = 0
        for grade in range(book.inGrade, book.outGrade + 1):
            if book.subject is None:
                # use student count (e.g. cross-subject books)
                # note that the n th grade is currently (n-1)th grade
                total += self.grade_query(grade - 1)
            elif grade <= 10:
                # use regular class size
                total += self.get_student_number(grade, book.subject)
            else:
                # consider course level
                if book.novices:
                    total += self.get_student_number(grade, book.subject, 'novices')
                if book.advanced:
                    total += self.get_student_number(grade, book.subject, 'advanced')
        return total

    def load_from_file(self):
        with open(self.filename, 'r') as h:
            self.data = json.load(h)

    def save_to_file(self):
        with open(self.filename, 'w') as h:
            json.dump(self.data, h, indent=4)
