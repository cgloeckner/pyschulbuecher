#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json, math
from datetime import date

from db.orm import db
from db import books, orga

__author__ = "Christian Glöckner"

def orderLoanOverview(loans):
    # 1st: outGrade, 2nd: subject, 3rd: title
    loans = list(loans.order_by(lambda l: l.book.title))
    loans.sort(key=lambda l: l.person.firstname)
    loans.sort(key=lambda l: l.person.name)
    loans.sort(key=lambda l: l.book.subject.tag if l.book.subject is not None else '')
    loans.sort(key=lambda l: l.book.outGrade)
    loans.sort(key=lambda l: l.person.student.class_.tag if l.person.student is not None and l.person.student.class_ is not None else '')
    loans.sort(key=lambda l: l.person.student.class_.grade if l.person.student is not None and l.person.student.class_ is not None else -1)
    return loans

def orderRequestOverview(requests):
    # 1st: outGrade, 2nd: subject, 3rd: title
    requests = list(requests.order_by(lambda r: r.book.title))
    requests.sort(key=lambda r: r.book.subject.tag if r.book.subject is not None else '')
    requests.sort(key=lambda r: r.book.outGrade)
    return requests

def getExpectedReturns(student: db.Student):
    """Returns a list of loans which are expected to be returned referring
    the student's current grade.
    """
    return select(l
        for l in db.Loan
            if l.person == student.person
            and l.book.outGrade <= student.class_.grade
    )

def isRequested(student: db.Student, book: db.Book):
    """Returns whether the given book is requested by the given student.
    """
    for r in student.person.request:
        if r.book == book:
            return True
    return False

def getRequestCount(person: db.Person, book: db.Book):
    """Returns whether the given book is requested by the given person.
    """
    for r in person.request:
        if r.book == book:
            return 1
    return 0

def updateRequest(student: db.Student, book: db.Book, status: bool):
    """Update request status for the given book and the given student. If True
    is provided, a request object is created. If not, no request object exists
    for that student to that book.
    """
    was = isRequested(student, book)
    if not was and status:
        # new request
        db.Request(person=student.person, book=book)
    elif was and not status:
        # delete request
        r = db.Request.get(person=student.person, book=book)
        r.delete()
    # else: nothing to update

def addLoan(person: db.Person, book: db.Book, count: int):
    """Add the given number of books to the given person's loaning."""
    l = db.Loan.get(person=person, book=book)
    if l is None and count > 0:
        # create new loan
        db.Loan(person=person, book=book, given=date.today(), count=count)
    elif l is not None:
        # update it
        l.count += count 

def updateLoan(person: db.Person, book: db.Book, count: int):
    """Update the loan status for the given book and the given person. If the
    count is set to zero, the loan object is deleted from the database.
    Otherwise the loan object is updated. If no such object exists, it will be
    created as needed.
    """
    l = db.Loan.get(person=person, book=book)
    if l is None and count > 0:
        # create new loan
        db.Loan(person=person, book=book, given=date.today(), count=count)
    elif l is not None:
        if count == 0:
            # delete loan
            l.delete()
        else:
            # update it
            l.count = count


def getLoanCount(person: db.Person, book: db.Book):
    """Return number of this specific book, either loaned by that person
    or all together.
    """
    if person is not None:
        # determine loan count
        for l in person.loan:
            if l.book == book:
                return l.count
        return 0
        
    else:
        # determine total loan count for all persons
        return sum(l.count for l in db.Loan if l.book == book)


def queryLoansByBook(book: db.Book):
    """Return a list of persons who loan that book.
    """
    loans = select(l for l in db.Loan if l.book == book)
    if loans is None:
        loans = list()
    else:
        loans = orderLoanOverview(loans)
    return loans


def applyRequest(student: db.Student):
    """Apply person's request be transfering to loaning these books.
    Note that the requests are deleted after that.
    """
    # add loaning
    bks = list()
    for l in student.person.request:
        if l.book.inGrade == 0:
            # ignore special books
            l.delete()
        else:
            updateLoan(student.person, l.book, 1)
            bks.append(l.book)
    
    # drop as requests
    for b in bks:
        updateRequest(student, b, False)

# -----------------------------------------------------------------------------

class DemandManager(object):

    def __init__(self, grade_query=orga.getStudentsCount):
        self.data        = dict()
        self.grade_query = grade_query
    
    def parse(self, forms):
        """Parse demand data from a form. The given forms parameter is a
        function handle with __call__(key), where key is a UI-related name tag.
        """
        # note: str(grade) because json will dump to str it anyway
        # parse student numbers for elective subjects (until 10th grade)
        tmp = dict()
        for grade in orga.getSecondary1Range():
            tmp[str(grade)] = dict()
            for sub in books.getSubjects(elective=True):
                key = "%d_%s" % (grade, sub.tag)
                val = forms(key)
                tmp[str(grade)][sub.tag] = int(val) if val != "" else 0
        # parse student numbers for each subject (after 11th grade)
        for grade in orga.getSecondary2Range():
            tmp[str(grade)] = dict()
            for sub in books.getSubjects():
                tmp[str(grade)][sub.tag] = dict()
                for level in ['novices', 'advanced']:
                    key = "%d_%s_%s" % (grade, sub.tag, level)
                    val = forms(key)
                    tmp[str(grade)][sub.tag][level] = int(val) if val != "" else 0
        # overwrite internal data
        self.data = tmp
    
    def getUnavailableBooksCount(self, book):
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
    
    def countBooksInUse(self, book):
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
    def getStudentNumber(self, grade: int, subject: db.Subject, level: str=None):
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
            return self.grade_query(grade-1)
        
        if level is None:
            # consider regular class
            return self.data[str(grade)][subject.tag]
        else:
            # consider course levels
            return self.data[str(grade)][subject.tag][level]
    
    # @TODO für Klassensätze nutzen?!
    def getMaxDemand(self, book: db.Book):
        """Calculate worst case demand of the given book assuming.
        Note that this calculates the demand for the NEXT year, so all grades
        are considerd -1.
        E.g. the new 10th grade is currently 9th grade now.
        """
        total = 0
        for grade in range(book.inGrade, book.outGrade+1):
            if book.subject is None:
                # use student count (e.g. cross-subject books)
                # note that the n th grade is currently (n-1)th grade
                total += self.grade_query(grade-1)
            elif grade <= 10:
                # use regular class size
                total += self.getStudentNumber(grade, book.subject)
            else:
                # consider course level
                if book.novices:
                    total += self.getStudentNumber(grade, book.subject, 'novices')
                if book.advanced:
                    total += self.getStudentNumber(grade, book.subject, 'advanced')
        return total
    
    def load_from(self, fhandle):
        tmp = json.load(fhandle)
        # overwrite internal data
        self.data = tmp
    
    def save_to(self, fhandle):
        json.dump(self.data, fhandle, indent=4)


# -----------------------------------------------------------------------------

import unittest
from decimal import Decimal

from pony.orm import *

from db.orm import db

class Tests(unittest.TestCase):

    @staticmethod
    @db_session
    def prepare():
        import db.orga, db.books
        
        db.orga.Tests.prepare()
        db.books.Tests.prepare()
    
    def setUp(self):
        db.create_tables()
        
    def tearDown(self):
        db.drop_all_tables(with_all_data=True)
        
    @db_session
    def test_isRequested(self):
        Tests.prepare()
        
        db.Request(person=db.Student[3].person, book=db.Book[3])
        
        self.assertTrue(isRequested(db.Student[3], db.Book[3]))
        self.assertFalse(isRequested(db.Student[3], db.Book[5]))
        self.assertFalse(isRequested(db.Student[1], db.Book[3]))

    @db_session
    def test_updateRequest(self):
        Tests.prepare()
        
        self.assertEqual(len(db.Student[3].person.request), 0)
        
        # register book 3
        updateRequest(db.Student[3], db.Book[3], True)
        self.assertEqual(len(db.Student[3].person.request), 1)
        self.assertTrue(isRequested(db.Student[3], db.Book[3]))
        
        # double-register book 3
        updateRequest(db.Student[3], db.Book[3], True)
        self.assertEqual(len(db.Student[3].person.request), 1)
        
        # double-unregister book 5
        updateRequest(db.Student[3], db.Book[5], False)
        self.assertEqual(len(db.Student[3].person.request), 1)
        
        # register book 5
        updateRequest(db.Student[3], db.Book[5], True)
        self.assertEqual(len(db.Student[3].person.request), 2)
        self.assertTrue(isRequested(db.Student[3], db.Book[5]))
        
        # unregister book 3
        updateRequest(db.Student[3], db.Book[3], False)
        self.assertEqual(len(db.Student[3].person.request), 1)
        self.assertFalse(isRequested(db.Student[3], db.Book[3]))
        
        # unregister book 5
        updateRequest(db.Student[3], db.Book[5], False)
        self.assertEqual(len(db.Student[3].person.request), 0)
        self.assertFalse(isRequested(db.Student[3], db.Book[5]))

    @db_session
    def test_updateLoan(self):
        Tests.prepare()
        
        s = db.Student[3]
        self.assertEqual(len(s.person.loan), 0)
        
        # register book 3
        updateLoan(s.person, db.Book[3], 1)
        self.assertEqual(len(s.person.loan), 1)
        self.assertEqual(getLoanCount(s.person, db.Book[3]), 1)
        
        # register 2nd book 3
        updateLoan(s.person, db.Book[3], 2)
        self.assertEqual(len(s.person.loan), 1)
        self.assertEqual(getLoanCount(s.person, db.Book[3]), 2)
        
        # return book 5 (not loaned yet)
        updateLoan(s.person, db.Book[5], 0)
        self.assertEqual(len(s.person.loan), 1)
        
        # register book 5
        updateLoan(s.person, db.Book[5], 1)
        self.assertEqual(len(s.person.loan), 2)
        self.assertEqual(getLoanCount(s.person, db.Book[5]), 1)
        
        # return book 3
        updateLoan(s.person, db.Book[3], 0)
        self.assertEqual(len(s.person.loan), 1)
        self.assertEqual(getLoanCount(s.person, db.Book[3]), 0)
        
        # return book 5
        updateLoan(s.person, db.Book[5], 0)
        self.assertEqual(len(s.person.loan), 0)
        self.assertEqual(getLoanCount(s.person, db.Book[5]), 0)

    @db_session
    def test_getLoanCount_without_person(self):
        Tests.prepare()
        
        # register some books
        updateLoan(db.Student[3].person, db.Book[3], 2)
        updateLoan(db.Student[1].person, db.Book[3], 1)
        updateLoan(db.Student[2].person, db.Book[3], 4)
        updateLoan(db.Teacher[2].person, db.Book[3], 30)
        
        # query total loan count without specifying a single person
        n = getLoanCount(person=None, book=db.Book[3])
        self.assertEqual(n, 37)

    @db_session
    def test_addLoans(self):
        Tests.prepare()
        
        # regular usecase
        db.Loan(person=db.Student[3].person, book=db.Book[3], given=date.today())
        db.Loan(person=db.Student[3].person, book=db.Book[5], given=date.today())
        db.Loan(person=db.Student[3].person, book=db.Book[8], given=date.today())
        
        ln = list(db.Student[3].person.loan)
        self.assertEqual(len(ln), 3)
        bs = set()
        for l in ln:
            self.assertEqual(l.count, 1)
            self.assertEqual(l.given, date.today())
            bs.add(l.book)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[8], bs)
        
        # with 2nd set
        db.Loan(person=db.Student[1].person, book=db.Book[3], given=date.today(), count=2)
        db.Loan(person=db.Student[1].person, book=db.Book[5], given=date.today(), count=2)
        db.Loan(person=db.Student[1].person, book=db.Book[8], given=date.today(), count=2)

        ln = list(db.Student[1].person.loan)
        self.assertEqual(len(ln), 3)
        bs = set()
        for l in ln:
            self.assertEqual(l.count, 2)
            self.assertEqual(l.given, date.today())
            bs.add(l.book)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[8], bs)
        
        # giving 30 books to a teacher
        db.Loan(person=db.Teacher[1].person, book=db.Book[3], given=date.today(), count=30)

        ln = list(db.Teacher[1].person.loan)
        self.assertEqual(len(ln), 1)
        self.assertEqual(ln[0].book, db.Book[3])
        self.assertEqual(ln[0].count, 30)
        self.assertEqual(ln[0].given, date.today())
    
    @db_session
    def test_getExpectedReturns(self):
        Tests.prepare()
        
        # give away some books to 12th grade student
        db.Loan(person=db.Student[3].person, book=db.Book[3], given=date.today())
        db.Loan(person=db.Student[3].person, book=db.Book[5], given=date.today())
        db.Loan(person=db.Student[3].person, book=db.Book[8], given=date.today())
        
        # expected returns for 12th grade
        ln = list(getExpectedReturns(db.Student[3]))
        self.assertEqual(len(ln), 3)
        bs = set()
        for l in ln:
            bs.add(l.book)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[8], bs)
        
        # expected returns for 11th
        db.Student[3].class_.grade = 11
        
        ln = list(getExpectedReturns(db.Student[3]))
        self.assertEqual(len(ln), 1)
        self.assertEqual(ln[0].book, db.Book[3]) # yet outdated (ends at 10)
        
        # give away some books to 8th grade student
        db.Loan(person=db.Student[1].person, book=db.Book[2], given=date.today())
        db.Loan(person=db.Student[1].person, book=db.Book[6], given=date.today())
        db.Loan(person=db.Student[1].person, book=db.Book[8], given=date.today())
        
        # expected returns for 8th grade
        ln = list(getExpectedReturns(db.Student[1]))
        self.assertEqual(len(ln), 1)
        self.assertEqual(ln[0].book, db.Book[2])
        
        # expected returns for 7th grade
        db.Student[1].class_.grade = 7
        ln = list(getExpectedReturns(db.Student[1]))
        self.assertEqual(len(ln), 1)
    
    @db_session
    def test_queryLoansByBook(self):
        Tests.prepare()
        
        # modify db to have two students in one class
        db.Student[2].class_ = db.Class[2] 
        
        # setup some loans
        updateLoan(db.Student[2].person, db.Book[2], 2)
        updateLoan(db.Teacher[2].person, db.Book[2], 3)
        updateLoan(db.Student[1].person, db.Book[2], 1)
        updateLoan(db.Student[3].person, db.Book[2], 6)
        
        # query loans
        loans = queryLoansByBook(db.Book[1])
        self.assertEqual(len(loans), 0)
        
        loans = queryLoansByBook(db.Book[2])
        self.assertEqual(len(loans), 4)
        self.assertEqual(db.Teacher[2].person, loans[0].person) # teacher listed first
        self.assertEqual(db.Student[1].person, loans[1].person) # 1st student in 8a
        self.assertEqual(db.Student[2].person, loans[2].person) # 1st student in 12glö
        self.assertEqual(db.Student[3].person, loans[3].person) # 2nd student in 12glö

    @db_session
    def test_DemandManager(self):
        Tests.prepare()
        
        # stub for grade sizes
        grade_size = { # become 5th, 6th, ..., 12th grade next year
            4: 73, 5: 67, 6: 55, 7: 0, 8: 62, 9: 51, 10: 43, 11: 33
        }
        
        # setup elective subjects
        sub_fr = db.Subject(name='Französisch', tag='Fr')
        sub_la = db.Subject(name='Latein', tag='La')
        sub_fr.elective = True
        sub_la.elective = True
        sub_ru = db.Subject.get(tag='Ru')
        sub_ru.elective = True
        sub_ma = db.Subject.get(tag='Ma')
        sub_de = db.Subject(name='Deutsch', tag='De')
        
        # stub complete for UI query
        # this demand is based on the NEW year (so the current 4th is then 5th etc.)
        keys = {
            '5_Fr': 27,
            '5_Ru': 13,
            '5_La': 19,
            '6_Fr': 8,
            '11_Ma_novices': 20,
            '11_Ma_advanced': 17,
            '11_De_novices': 18,
            '11_De_advanced': 22,
            '12_Ma_novices': 13,
            '12_Ma_advanced': 7,
            '12_De_novices': 13,
            '12_De_advanced': 12,
        }
        for grade in orga.getSecondary1Range():
            for sub in books.getSubjects(elective=True):
                key = '%s_%s' % (grade, sub.tag)
                if key not in keys:
                    keys[key] = 0
        for grade in orga.getSecondary2Range():
            for sub in books.getSubjects():
                for level in ['novices', 'advanced']:
                    key = '%s_%s_%s' % (grade, sub.tag, level)
                    if key not in keys:
                        keys[key] = 0
        
        # setup some more books
        math1 = db.Book(title='Maths A', isbn='000-001', price=2495,
            publisher=db.Publisher[1], inGrade=11, outGrade=12,
            subject=sub_ma, novices=True)
        math2 = db.Book(title='Maths B', isbn='001-021', price=2999,
            publisher=db.Publisher[1], inGrade=11, outGrade=12,
            subject=sub_ma, advanced=True)
        math3 = db.Book(title='Maths B', isbn='001-022', price=2999,
            publisher=db.Publisher[1], inGrade=5, outGrade=7,
            subject=sub_ma)
        
        de = db.Book(title='Literatur', isbn='400-001', price=2495,
            publisher=db.Publisher[1], inGrade=11, outGrade=12,
            subject=sub_de, novices=True, advanced=True)
        
        fr = db.Book(title='French 101', isbn='000-002', price=1234,
            publisher=db.Publisher[1], inGrade=5, outGrade=6,
            subject=sub_fr)
        
        # create demand manager
        d = DemandManager(grade_size.__getitem__)
        d.parse(keys.__getitem__)
        
        # @TODO für Klassensätze nutzen?!
        """
        # test student number queries
        self.assertEqual(d.getStudentNumber(5, sub_la), 19)
        self.assertEqual(d.getStudentNumber(5, sub_fr), 27)
        self.assertEqual(d.getStudentNumber(5, sub_ru), 13)
        self.assertEqual(d.getStudentNumber(5, sub_ma), 73)
        self.assertEqual(d.getStudentNumber(6, sub_fr), 8)
        self.assertEqual(d.getStudentNumber(6, sub_ru), 0)
        self.assertEqual(d.getStudentNumber(8, sub_ma), 0)
        self.assertEqual(d.getStudentNumber(11, sub_ma, 'novices'), 20)
        self.assertEqual(d.getStudentNumber(12, sub_ma, 'advanced'), 7)
        self.assertEqual(d.getStudentNumber(11, sub_de, 'novices'), 18)

        # test demands for some books
        self.assertEqual(d.getMaxDemand(math1), 20+13) # both novices courses
        self.assertEqual(d.getMaxDemand(math2), 17+7) # both advanced courses
        self.assertEqual(d.getMaxDemand(math3), 73+67+55) # grade 5,6,8        
        self.assertEqual(d.getMaxDemand(de), 18+22+13+12) # all 11th/12th grade course use it
        self.assertEqual(d.getMaxDemand(fr), 27+8) # 27 from 5th grade + 8 from 6th grade
        """
        
        # test saving and loading
        import io
        handle = io.StringIO()
        d.save_to(handle)
        handle.seek(0) # rewind
        
        d2 = DemandManager()
        d2.load_from(handle)
    
    @db_session
    def test_getBooksCounts(self):
        Tests.prepare()
        
        # prepare book
        b = db.Book(title='Example', isbn='000-001', price=2495,
            publisher=db.Publisher[1], inGrade=5, outGrade=7,
            subject=db.Subject[1])
        b.stock = 30
        
        # prepare addition classes
        c_new  = db.Class(grade=5, tag='a')
        c_cont = db.Class(grade=6, tag='c')
        c_ret  = db.Class(grade=7, tag='b')
        
        # add 8 books for request (5th grade)
        for i in range(8):
            s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_new)
            db.Request(person=s.person, book=b)
        
        # add 2 books as loan (5th grade)
        for i in range(2):
            s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_new)
            db.Loan(person=s.person, book=b, given=date.today())
        
        # add 7 books for continued use (6th grade)
        s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_cont)
        db.Loan(person=s.person, book=b, given=date.today(), count=2)
        s2 = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_cont)
        db.Loan(person=s2.person, book=b, given=date.today(), count=2)
        for i in range(3):
            s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_cont)
            db.Loan(person=s.person, book=b, given=date.today())

        # add 3 books to be returned (7th grade)
        for i in range(3):
            s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_ret)
            db.Loan(person=s.person, book=b, given=date.today())
        
        d = DemandManager()
        
        in_use = d.countBooksInUse(b)
        # 2 (5th loan) + 7 (6th loan)
        self.assertEqual(in_use, 9)



