#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pony.orm import *
from decimal import Decimal
import unittest
import json
import math
from datetime import date

from app.db import loan_queries, db
from app.db import book_queries as books, orga

__author__ = "Christian Glöckner"


# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------


class Tests(unittest.TestCase):

    @staticmethod
    @db_session
    def prepare():
        import db.orga
        import db.books

        db.orga.Tests.prepare()
        db.books.Tests.prepare()

    def setUp(self):
        db.create_tables()

    def tearDown(self):
        db.drop_all_tables(with_all_data=True)

    @db_session
    def test_is_requested(self):
        Tests.prepare()

        db.Request(person=db.Student[3].person, book=db.Book[3])

        self.assertTrue(is_requested(db.Student[3], db.Book[3]))
        self.assertFalse(is_requested(db.Student[3], db.Book[5]))
        self.assertFalse(is_requested(db.Student[1], db.Book[3]))

    @db_session
    def test_update_request(self):
        Tests.prepare()

        self.assertEqual(len(db.Student[3].person.request), 0)

        # register book 3
        update_request(db.Student[3], db.Book[3], True)
        self.assertEqual(len(db.Student[3].person.request), 1)
        self.assertTrue(is_requested(db.Student[3], db.Book[3]))

        # double-register book 3
        update_request(db.Student[3], db.Book[3], True)
        self.assertEqual(len(db.Student[3].person.request), 1)

        # double-unregister book 5
        update_request(db.Student[3], db.Book[5], False)
        self.assertEqual(len(db.Student[3].person.request), 1)

        # register book 5
        update_request(db.Student[3], db.Book[5], True)
        self.assertEqual(len(db.Student[3].person.request), 2)
        self.assertTrue(is_requested(db.Student[3], db.Book[5]))

        # unregister book 3
        update_request(db.Student[3], db.Book[3], False)
        self.assertEqual(len(db.Student[3].person.request), 1)
        self.assertFalse(is_requested(db.Student[3], db.Book[3]))

        # unregister book 5
        update_request(db.Student[3], db.Book[5], False)
        self.assertEqual(len(db.Student[3].person.request), 0)
        self.assertFalse(is_requested(db.Student[3], db.Book[5]))

    @db_session
    def test_update_loan(self):
        Tests.prepare()

        s = db.Student[3]
        self.assertEqual(len(s.person.loan), 0)

        # register book 3
        update_loan(s.person, db.Book[3], 1)
        self.assertEqual(len(s.person.loan), 1)
        self.assertEqual(get_loan_count(s.person, db.Book[3]), 1)

        # register 2nd book 3
        update_loan(s.person, db.Book[3], 2)
        self.assertEqual(len(s.person.loan), 1)
        self.assertEqual(get_loan_count(s.person, db.Book[3]), 2)

        # return book 5 (not loaned yet)
        update_loan(s.person, db.Book[5], 0)
        self.assertEqual(len(s.person.loan), 1)

        # register book 5
        update_loan(s.person, db.Book[5], 1)
        self.assertEqual(len(s.person.loan), 2)
        self.assertEqual(get_loan_count(s.person, db.Book[5]), 1)

        # return book 3
        update_loan(s.person, db.Book[3], 0)
        self.assertEqual(len(s.person.loan), 1)
        self.assertEqual(get_loan_count(s.person, db.Book[3]), 0)

        # return book 5
        update_loan(s.person, db.Book[5], 0)
        self.assertEqual(len(s.person.loan), 0)
        self.assertEqual(get_loan_count(s.person, db.Book[5]), 0)

    @db_session
    def test_get_loan_count_without_person(self):
        Tests.prepare()

        # register some books
        update_loan(db.Student[3].person, db.Book[3], 2)
        update_loan(db.Student[1].person, db.Book[3], 1)
        update_loan(db.Student[2].person, db.Book[3], 4)
        update_loan(db.Teacher[2].person, db.Book[3], 30)

        # query total loan count without specifying a single person
        n = get_loan_count(person=None, book=db.Book[3])
        self.assertEqual(n, 37)

    @db_session
    def test_add_loans(self):
        Tests.prepare()

        # regular usecase
        db.Loan(
            person=db.Student[3].person,
            book=db.Book[3],
            given=date.today())
        db.Loan(
            person=db.Student[3].person,
            book=db.Book[5],
            given=date.today())
        db.Loan(
            person=db.Student[3].person,
            book=db.Book[8],
            given=date.today())

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
        db.Loan(
            person=db.Student[1].person,
            book=db.Book[3],
            given=date.today(),
            count=2)
        db.Loan(
            person=db.Student[1].person,
            book=db.Book[5],
            given=date.today(),
            count=2)
        db.Loan(
            person=db.Student[1].person,
            book=db.Book[8],
            given=date.today(),
            count=2)

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
        db.Loan(
            person=db.Teacher[1].person,
            book=db.Book[3],
            given=date.today(),
            count=30)

        ln = list(db.Teacher[1].person.loan)
        self.assertEqual(len(ln), 1)
        self.assertEqual(ln[0].book, db.Book[3])
        self.assertEqual(ln[0].count, 30)
        self.assertEqual(ln[0].given, date.today())

    @db_session
    def test_get_expected_returns(self):
        Tests.prepare()

        # give away some books to 12th grade student
        db.Loan(
            person=db.Student[3].person,
            book=db.Book[3],
            given=date.today())
        db.Loan(
            person=db.Student[3].person,
            book=db.Book[5],
            given=date.today())
        db.Loan(
            person=db.Student[3].person,
            book=db.Book[8],
            given=date.today())

        # expected returns for 12th grade
        ln = list(get_expected_returns(db.Student[3]))
        self.assertEqual(len(ln), 3)
        bs = set()
        for l in ln:
            bs.add(l.book)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[8], bs)

        # expected returns for 11th
        db.Student[3].class_.grade = 11

        ln = list(get_expected_returns(db.Student[3]))
        self.assertEqual(len(ln), 1)
        self.assertEqual(ln[0].book, db.Book[3])  # yet outdated (ends at 10)

        # give away some books to 8th grade student
        db.Loan(
            person=db.Student[1].person,
            book=db.Book[2],
            given=date.today())
        db.Loan(
            person=db.Student[1].person,
            book=db.Book[6],
            given=date.today())
        db.Loan(
            person=db.Student[1].person,
            book=db.Book[8],
            given=date.today())

        # expected returns for 8th grade
        ln = list(get_expected_returns(db.Student[1]))
        self.assertEqual(len(ln), 1)
        self.assertEqual(ln[0].book, db.Book[2])

        # expected returns for 7th grade
        db.Student[1].class_.grade = 7
        ln = list(get_expected_returns(db.Student[1]))
        self.assertEqual(len(ln), 1)

    @db_session
    def test_query_loans_by_book(self):
        Tests.prepare()

        # modify db to have two students in one class
        db.Student[2].class_ = db.Class[2]

        # setup some loans
        update_loan(db.Student[2].person, db.Book[2], 2)
        update_loan(db.Teacher[2].person, db.Book[2], 3)
        update_loan(db.Student[1].person, db.Book[2], 1)
        update_loan(db.Student[3].person, db.Book[2], 6)

        # query loans
        loans = query_loans_by_book(db.Book[1])
        self.assertEqual(len(loans), 0)

        loans = query_loans_by_book(db.Book[2])
        self.assertEqual(len(loans), 4)
        self.assertEqual(
            db.Teacher[2].person,
            loans[0].person)  # teacher listed first
        self.assertEqual(
            db.Student[1].person,
            loans[1].person)  # 1st student in 8a
        self.assertEqual(
            db.Student[2].person,
            loans[2].person)  # 1st student in 12glö
        self.assertEqual(
            db.Student[3].person,
            loans[3].person)  # 2nd student in 12glö

    @db_session
    def test_DemandManager(self):
        Tests.prepare()

        # stub for grade sizes
        grade_size = {  # become 5th, 6th, ..., 12th grade next year
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
        # this demand is based on the NEW year (so the current 4th is then 5th
        # etc.)
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
        for grade in orga.get_secondary_level1_range():
            for sub in books.get_subjects(elective=True):
                key = '%s_%s' % (grade, sub.tag)
                if key not in keys:
                    keys[key] = 0
        for grade in orga.get_secondary_level2_range():
            for sub in books.get_subjects():
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
        self.assertEqual(d.get_student_number(5, sub_la), 19)
        self.assertEqual(d.get_student_number(5, sub_fr), 27)
        self.assertEqual(d.get_student_number(5, sub_ru), 13)
        self.assertEqual(d.get_student_number(5, sub_ma), 73)
        self.assertEqual(d.get_student_number(6, sub_fr), 8)
        self.assertEqual(d.get_student_number(6, sub_ru), 0)
        self.assertEqual(d.get_student_number(8, sub_ma), 0)
        self.assertEqual(d.get_student_number(11, sub_ma, 'novices'), 20)
        self.assertEqual(d.get_student_number(12, sub_ma, 'advanced'), 7)
        self.assertEqual(d.get_student_number(11, sub_de, 'novices'), 18)

        # test demands for some books
        self.assertEqual(d.get_max_demand(math1), 20+13) # both novices courses
        self.assertEqual(d.get_max_demand(math2), 17+7) # both advanced courses
        self.assertEqual(d.get_max_demand(math3), 73+67+55) # grade 5,6,8
        self.assertEqual(d.get_max_demand(de), 18+22+13+12) # all 11th/12th grade course use it
        self.assertEqual(d.get_max_demand(fr), 27+8) # 27 from 5th grade + 8 from 6th grade
        """

        # test saving and loading
        import io
        handle = io.StringIO()
        d.save_to(handle)
        handle.seek(0)  # rewind

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
        c_new = db.Class(grade=5, tag='a')
        c_cont = db.Class(grade=6, tag='c')
        c_ret = db.Class(grade=7, tag='b')

        # add 8 books for request (5th grade)
        for i in range(8):
            s = db.Student(
                person=db.Person(
                    name='Foo',
                    firstname='Bar'),
                class_=c_new)
            db.Request(person=s.person, book=b)

        # add 2 books as loan (5th grade)
        for i in range(2):
            s = db.Student(
                person=db.Person(
                    name='Foo',
                    firstname='Bar'),
                class_=c_new)
            db.Loan(person=s.person, book=b, given=date.today())

        # add 7 books for continued use (6th grade)
        s = db.Student(
            person=db.Person(
                name='Foo',
                firstname='Bar'),
            class_=c_cont)
        db.Loan(person=s.person, book=b, given=date.today(), count=2)
        s2 = db.Student(
            person=db.Person(
                name='Foo',
                firstname='Bar'),
            class_=c_cont)
        db.Loan(person=s2.person, book=b, given=date.today(), count=2)
        for i in range(3):
            s = db.Student(
                person=db.Person(
                    name='Foo',
                    firstname='Bar'),
                class_=c_cont)
            db.Loan(person=s.person, book=b, given=date.today())

        # add 3 books to be returned (7th grade)
        for i in range(3):
            s = db.Student(
                person=db.Person(
                    name='Foo',
                    firstname='Bar'),
                class_=c_ret)
            db.Loan(person=s.person, book=b, given=date.today())

        d = DemandManager()

        in_use = d.count_books_in_use(b)
        # 2 (5th loan) + 7 (6th loan)
        self.assertEqual(in_use, 9)
