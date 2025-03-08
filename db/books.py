#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pony.orm import *
import unittest
from pony import orm

from app.db import db, book_queries


__author__ = "Christian Glöckner"


class Tests(unittest.TestCase):

    @staticmethod
    @db_session
    def prepare():
        # create subjects
        db.Subject(name='Mathematics', tag='Ma')
        db.Subject(name='Russian', tag='Ru')
        db.Subject(name='English', tag='Eng')
        db.Subject(name='Spanish', tag='Spa')
        db.Subject[2].elective = True
        db.Subject[4].elective = True

        # create publishers
        db.Publisher(name='Cornelsen')
        db.Publisher(name='Klett')

        # create maths books
        db.Book(title='Maths II', isbn='001-021', price=2999,
                publisher=db.Publisher[1], inGrade=7, outGrade=8,
                subject=db.Subject[1])
        db.Book(title='Maths I', isbn='000-001', price=2495,
                publisher=db.Publisher[1], inGrade=5, outGrade=6,
                subject=db.Subject[1])
        db.Book(title='Maths III', isbn='914-721', price=3499,
                publisher=db.Publisher[1], inGrade=9, outGrade=10,
                subject=db.Subject[1])
        db.Book(
            title='Basic Maths',
            publisher=db.Publisher[1],
            inGrade=11,
            outGrade=12,
            subject=db.Subject[1],
            novices=True,
            classsets=True,
            for_loan=False)
        db.Book(
            title='Advanced Maths',
            publisher=db.Publisher[1],
            inGrade=11,
            outGrade=12,
            subject=db.Subject[1],
            advanced=True,
            classsets=True)

        # create russian books
        db.Book(title='Privjet', isbn='49322-6346', price=5999,
                publisher=db.Publisher[2], inGrade=5, outGrade=10,
                subject=db.Subject[2])
        db.Book(title='Dialog', isbn='43623-8485', price=7999,
                publisher=db.Publisher[2], inGrade=11, outGrade=12,
                subject=db.Subject[2], novices=True, advanced=True)

        # create subject-independent books
        db.Book(title='Formulary', isbn='236-7634-62', price=2295,
                publisher=db.Publisher[1], inGrade=7, outGrade=12)

        # create english book
        db.Book(title='English 5th grade', publisher=db.Publisher[2],
                inGrade=5, outGrade=5, subject=db.Subject[3], classsets=True,
                for_loan=False)

    def setUp(self):
        db.create_tables()

    def tearDown(self):
        db.drop_all_tables(with_all_data=True)

    @db_session
    def test_get_publishers(self):
        Tests.prepare()

        ps = get_publishers()
        self.assertEqual(len(ps), 2)
        self.assertIn(db.Publisher[1], ps)
        self.assertIn(db.Publisher[2], ps)

    @db_session
    def test_get_subjects(self):
        Tests.prepare()

        sb = get_subjects()
        self.assertEqual(len(sb), 4)
        self.assertIn(db.Subject[1], sb)
        self.assertIn(db.Subject[3], sb)
        self.assertIn(db.Subject[2], sb)
        self.assertIn(db.Subject[4], sb)

        sb = get_subjects(elective=False)
        self.assertEqual(len(sb), 2)
        self.assertIn(db.Subject[1], sb)
        self.assertIn(db.Subject[3], sb)

        sb = get_subjects(elective=True)
        self.assertEqual(len(sb), 2)
        self.assertIn(db.Subject[2], sb)
        self.assertIn(db.Subject[4], sb)

    @db_session
    def test_order_books_index(self):
        Tests.prepare()

        bks = db.Book.select()
        bks = order_books_index(bks)
        self.assertEqual(bks[0], db.Book[8])
        self.assertEqual(bks[1], db.Book[9])
        self.assertEqual(bks[2], db.Book[2])
        self.assertEqual(bks[3], db.Book[1])
        self.assertEqual(bks[4], db.Book[3])
        self.assertEqual(bks[5], db.Book[5])
        self.assertEqual(bks[6], db.Book[4])
        self.assertEqual(bks[7], db.Book[6])
        self.assertEqual(bks[8], db.Book[7])

    @db_session
    def test_order_books_list(self):
        Tests.prepare()

        bks = db.Book.select()
        bks = order_books_list(bks)
        self.assertEqual(bks[0], db.Book[8])
        self.assertEqual(bks[1], db.Book[9])
        self.assertEqual(bks[2], db.Book[5])
        self.assertEqual(bks[3], db.Book[4])
        self.assertEqual(bks[4], db.Book[2])
        self.assertEqual(bks[5], db.Book[1])
        self.assertEqual(bks[6], db.Book[3])
        self.assertEqual(bks[7], db.Book[7])
        self.assertEqual(bks[8], db.Book[6])

    @db_session
    def test_get_all_books(self):
        Tests.prepare()

        bs = set(get_all_books())
        self.assertEqual(len(bs), 9)
        self.assertIn(db.Book[8], bs)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[1], bs)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)
        self.assertIn(db.Book[9], bs)

    @db_session
    def test_get_books_without_subject(self):
        Tests.prepare()

        bs = get_books_without_subject()
        self.assertEqual(len(bs), 1)
        self.assertIn(db.Book[8], bs)

    @db_session
    def test_get_books_used_in(self):
        Tests.prepare()

        bs = get_books_used_in(5)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[9], bs)

        bs = get_books_used_in(5, booklist=True)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)

        bs = get_books_used_in(6)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)

        bs = get_books_used_in(7)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[1], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[8], bs)

        bs = get_books_used_in(10)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[8], bs)

        bs = get_books_used_in(11)
        self.assertEqual(len(bs), 4)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

        bs = get_books_used_in(11, booklist=True)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

        bs = get_books_used_in(13)
        self.assertEqual(len(bs), 0)

    @db_session
    def test_get_books_started_in(self):
        Tests.prepare()

        bs = get_books_started_in(5)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[9], bs)

        bs = get_books_started_in(5, booklist=True)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)

        bs = get_books_started_in(6)
        self.assertEqual(len(bs), 0)

        bs = get_books_started_in(7)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[1], bs)
        self.assertIn(db.Book[8], bs)

        bs = get_books_started_in(11)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)

        bs = get_books_started_in(11, booklist=True)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)

    @db_session
    def test_get_books_finished_in(self):
        Tests.prepare()

        bs = get_books_finished_in(5)
        self.assertEqual(len(bs), 1)
        self.assertIn(db.Book[9], bs)

        bs = get_books_finished_in(5, booklist=True)
        self.assertEqual(len(bs), 0)

        bs = get_books_finished_in(6)
        self.assertEqual(len(bs), 1)
        self.assertIn(db.Book[2], bs)

        bs = get_books_finished_in(10)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[6], bs)

        bs = get_books_finished_in(12)
        self.assertEqual(len(bs), 4)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

        bs = get_books_finished_in(12, booklist=True)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

    @db_session
    def test_get_books_by_title(self):
        Tests.prepare()

        bs = get_books_by_title('Maths')
        self.assertEqual(len(bs), 5)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[1], bs)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)

    @db_session
    def test_get_books_by_isbn(self):
        Tests.prepare()

        # single book
        bs = get_books_by_isbn('236-7634-62')
        self.assertEqual(len(bs), 1)
        self.assertIn(db.Book[8], bs)

        # all not yet available books
        bs = get_books_by_isbn('')
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[9], bs)

    @db_session
    def test_get_real_books(self):
        Tests.prepare()

        # make some books become workbooks / classsets
        db.Book[2].workbook = True
        db.Book[7].workbook = True
        db.Book[4].classsets = True
        db.Book[5].classsets = False

        # query real books
        bs = get_real_books()
        self.assertEqual(len(bs), 7)
        self.assertIn(db.Book[1], bs)
        self.assertNotIn(db.Book[2], bs)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[6], bs)
        self.assertNotIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)
        self.assertIn(db.Book[9], bs)

        # query real books by subject (including classsets)
        bs = get_real_books_by_subject(db.Subject[1], True)
        self.assertEqual(len(bs), 4)
        self.assertIn(db.Book[1], bs)
        self.assertNotIn(db.Book[2], bs)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)

        # query real books by subject (without classsets)
        bs = get_real_books_by_subject(db.Subject[1], False)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[1], bs)
        self.assertNotIn(db.Book[2], bs)
        self.assertIn(db.Book[3], bs)
        self.assertNotIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)

        # query real books by grade (with classets)
        bs = get_real_books_by_grade(11, True)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertNotIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

        # query real books by grade (without classets)
        bs = get_real_books_by_grade(11, False)
        self.assertEqual(len(bs), 2)
        self.assertNotIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertNotIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

    @db_session
    def test_getWorkbooks(self):
        Tests.prepare()

        # make some books become workbooks / classsets
        db.Book[2].workbook = True
        db.Book[3].workbook = True

        # query math workbooks
        wb = get_workbooks_by_subject(db.Subject[1])
        self.assertEqual(len(wb), 2)
        self.assertIn(db.Book[2], wb)
        self.assertIn(db.Book[3], wb)

    @db_session
    def test_getClassSets(self):
        Tests.prepare()

        # query math classets
        cb = get_classsets_by_subject(db.Subject[1])
        self.assertEqual(len(cb), 2)
        self.assertIn(db.Book[4], cb)
        self.assertIn(db.Book[5], cb)

    @db_session
    def test_add_subjects(self):
        raw = """Mathematik\tMa
Englisch\tEng
Deutsch\tDe
Sport\tSp"""
        add_subjects(raw)

        s = select(s.name for s in db.Subject)
        self.assertEqual(len(s), 4)
        self.assertIn("Mathematik", s)
        self.assertIn("Englisch", s)
        self.assertIn("Deutsch", s)
        self.assertIn("Sport", s)

    @db_session
    def test_add_publishers(self):
        raw = """Cornelsen
Klett
Volk & Wissen
C.C. Buchner"""
        add_publishers(raw)

        p = select(s.name for s in db.Publisher)
        self.assertEqual(len(p), 4)
        self.assertIn("Cornelsen", p)
        self.assertIn("Klett", p)
        self.assertIn("Volk & Wissen", p)
        self.assertIn("C.C. Buchner", p)

    @db_session
    def test_canadd_bookWithFullInformation(self):
        add_subjects("Mathematik\tMa")
        add_publishers("Klett")

        raw = "Mathematik Live\t0815-1234\t23,95 €\tKlett\t11\t12\tMa\tTrue\tFalse\tFalse\tFalse\tFalse\tLehrbuch"
        add_book(raw)

        b = db.Book[1]
        self.assertEqual(b.title, "Mathematik Live")
        self.assertEqual(b.isbn, "0815-1234")
        self.assertEqual(b.price, 2395)
        self.assertEqual(b.publisher, db.Publisher[1])
        self.assertEqual(b.inGrade, 11)
        self.assertEqual(b.outGrade, 12)
        self.assertEqual(b.subject, db.Subject[1])
        self.assertTrue(b.novices)
        self.assertFalse(b.advanced)
        self.assertFalse(b.workbook)
        self.assertFalse(b.classsets)
        self.assertFalse(b.for_loan)
        self.assertEqual(b.comment, "Lehrbuch")

    @db_session
    def test_canadd_bookWithMinimalInformation(self):
        add_publishers("Klett")

        raw = "Das Große Tafelwerk\t\t\tKlett\t7\t12\t\t\t\t\t\t\t"
        add_book(raw)

        b = db.Book[1]
        self.assertEqual(b.title, "Das Große Tafelwerk")
        self.assertEqual(b.isbn, "")
        self.assertEqual(b.price, None)
        self.assertEqual(b.publisher, db.Publisher[1])
        self.assertEqual(b.inGrade, 7)
        self.assertEqual(b.outGrade, 12)
        self.assertFalse(b.novices)
        self.assertFalse(b.advanced)
        self.assertTrue(b.for_loan)

    @db_session
    def test_add_books(self):
        add_publishers("Klett\nCornelsen")
        add_subjects("Mathemati\tMa\nEnglisch\tEng")

        ma = db.Subject.get(tag="Ma")
        eng = db.Subject.get(tag="Eng")

        raw = """Mathematik Live\t0815-1234\t23,95\tKlett\t11\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t
Tafelwerk\t12-52-6346\t19,99\tKlett\t7\t12\t\tFalse\tFalse\tFalse\tFalse\tfächerübergreifend
Englisch Oberstufe\t433-5213-6246\t49,95\tCornelsen\t11\t12\tEng\tTrue\tTrue\tFalse\tFalse\tTrue\t
Das Große Tafelwerk\t\t\tKlett\t7\t12\t\tFalse\tFalse\tFalse\tFalse\tTrue\tfächerübergreifend"""

        add_books(raw)

        b1 = db.Book[1]
        b2 = db.Book[2]
        b3 = db.Book[3]
        b4 = db.Book[4]

        self.assertEqual(b1.title, "Mathematik Live")
        self.assertEqual(b2.title, "Tafelwerk")
        self.assertEqual(b3.title, "Englisch Oberstufe")
        self.assertEqual(b4.title, "Das Große Tafelwerk")
        self.assertEqual(b1.subject, ma)
        self.assertEqual(b2.subject, None)
        self.assertEqual(b3.subject, eng)
        self.assertTrue(b3.novices)
        self.assertTrue(b3.advanced)
