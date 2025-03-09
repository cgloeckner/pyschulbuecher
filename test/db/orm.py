#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from datetime import date

from pony.orm import *

from app.db import db


__author__ = "Christian Glöckner"


class Tests(unittest.TestCase):

    def setUp(self):
        db.create_tables()

    def tearDown(self):
        db.drop_all_tables(with_all_data=True)

    @db_session
    def test_canDeletePerson(self):
        p = db.Person(name='Foo', firstname='Bar')

        p.delete()

    @db_session
    def test_canDeleteStudentThroughPerson(self):
        p = db.Person(name='Foo', firstname='Bar')
        db.Student(person=p, class_=db.Class(grade=7, tag='b'))

        p.delete()
        s = select(s for s in db.Student)
        self.assertEqual(len(s), 0)

    @db_session
    def test_canDeletePersonThroughStudent(self):
        s = db.Student(
            person=db.Person(
                name='Foo', firstname='Bar'), class_=db.Class(
                grade=7, tag='b'))

        s.delete()
        p = select(p for p in db.Person)
        self.assertEqual(len(p), 0)

    @db_session
    def test_canDeleteTeacherThroughPerson(self):
        p = db.Person(name='Foo', firstname='Bar')
        db.Teacher(person=p, tag='FooB')

        p.delete()
        s = select(s for s in db.Teacher)
        self.assertEqual(len(s), 0)

    @db_session
    def test_canDeletePersonThroughThrough(self):
        t = db.Teacher(
            person=db.Person(
                name='Foo',
                firstname='Bar'),
            tag='FooB')

        t.delete()
        p = select(p for p in db.Person)
        self.assertEqual(len(p), 0)

    @db_session
    def test_cannotDeletePersonWithLoans(self):
        p = db.Person(name='Foo', firstname='Bar')

        db.Loan(
            person=p, given=date.today(), book=db.Book(
                title='spam', publisher=db.Publisher(
                    name='lol'), inGrade=7, outGrade=9, subject=db.Subject(
                    name='rofl', tag='xD')))

        with self.assertRaises(core.ConstraintError):
            p.delete()

    @db_session
    def test_canDeletePersonAfterLoans(self):
        p = db.Person(name='Foo', firstname='Bar')

        db.Loan(
            person=p, given=date.today(), book=db.Book(
                title='spam', publisher=db.Publisher(
                    name='lol'), inGrade=7, outGrade=9, subject=db.Subject(
                    name='rofl', tag='xD')))

        for l in p.loan:
            l.delete()

        p.delete()

    @db_session
    def test_canDeletePersonWithRequest(self):
        p = db.Person(name='Foo', firstname='Bar')

        db.Request(
            person=p, book=db.Book(
                title='spam', publisher=db.Publisher(
                    name='lol'), inGrade=7, outGrade=9, subject=db.Subject(
                    name='rofl', tag='xD')))

        p.delete()

        r = select(r for r in db.Request)
        self.assertEqual(len(r), 0)

    @db_session
    def test_canDeleteEmptyClass(self):
        c = db.Class(grade=5, tag='c')

        c.delete()

    @db_session
    def test_cannotDeleteNonEmptyClass(self):
        c = db.Class(grade=5, tag='c')
        db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c)

        with self.assertRaises(core.ConstraintError):
            c.delete()

    @db_session
    def test_canDeleteClassAfterClearing(self):
        c = db.Class(grade=5, tag='c')
        s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c)

        s.delete()
        c.delete()

    @db_session
    def test_canDeleteTeacherWithoutClass(self):
        t = db.Teacher(
            person=db.Person(
                name='Foo',
                firstname='Bar'),
            tag='FoB')

        t.person.delete()

    @db_session
    def test_canDeleteTeacherWithClass(self):
        t = db.Teacher(
            person=db.Person(
                name='Foo',
                firstname='Bar'),
            tag='FoB')
        c = db.Class(grade=5, tag='c', teacher=t)

        t.person.delete()

        self.assertEqual(c.teacher, None)

    @db_session
    def test_canDeleteSubjectWithoutBook(self):
        s = db.Subject(name='Foo', tag='Fo')

        s.delete()

    @db_session
    def test_canDeleteSubjectWithBook(self):
        s = db.Subject(name='Foo', tag='Fo')
        b = db.Book(title='Bar', publisher=db.Publisher(name='lol'),
                    subject=s, inGrade=5, outGrade=6
                    )

        s.delete()

        self.assertEqual(b.subject, None)

    @db_session
    def test_canDeleteSubjectWithWorkook(self):
        s = db.Subject(name='Foo', tag='Fo')
        w = db.Book(title='Bar', publisher=db.Publisher(name='lol'),
                    subject=s, inGrade=5, outGrade=6, workbook=True
                    )

        s.delete()

        self.assertEqual(w.subject, None)

    @db_session
    def test_canDeletePublisherWithoutBook(self):
        p = db.Publisher(name='Foo')

        p.delete()

    @db_session
    def test_cannotDeletePublisherWithBook(self):
        p = db.Publisher(name='Foo')
        b = db.Book(
            title='Bar',
            publisher=p,
            subject=db.Subject(
                name='Foo',
                tag='Fo'),
            inGrade=5,
            outGrade=6)

        with self.assertRaises(core.ConstraintError):
            p.delete()

    @db_session
    def test_cannotDeletePublisherWithWorkbook(self):
        p = db.Publisher(name='Foo')
        w = db.Book(
            title='Bar',
            publisher=p,
            subject=db.Subject(
                name='Foo',
                tag='Fo'),
            inGrade=5,
            outGrade=6,
            workbook=True)

        with self.assertRaises(core.ConstraintError):
            p.delete()

    @db_session
    def test_canDeletePublisherAfterBook(self):
        p = db.Publisher(name='Foo')
        b = db.Book(
            title='Bar',
            publisher=p,
            subject=db.Subject(
                name='Foo',
                tag='Fo'),
            inGrade=5,
            outGrade=6)

        b.delete()
        p.delete()

    @db_session
    def test_canDeleteBookWithoutLoan(self):
        b = db.Book(
            title='Bar', publisher=db.Publisher(
                name='Foo'), subject=db.Subject(
                name='Foo', tag='Fo'), inGrade=5, outGrade=6)

        b.delete()

    @db_session
    def test_cannotDeleteBookWithLoan(self):
        b = db.Book(
            title='Bar', publisher=db.Publisher(
                name='Foo'), subject=db.Subject(
                name='Foo', tag='Fo'), inGrade=5, outGrade=6)
        l = db.Loan(person=db.Person(name='lol', firstname='Bar'), book=b,
                    given=date.today()
                    )

        with self.assertRaises(core.ConstraintError):
            b.delete()

    @db_session
    def test_canDeleteBookAfterLoan(self):
        b = db.Book(
            title='Bar', publisher=db.Publisher(
                name='Foo'), subject=db.Subject(
                name='Foo', tag='Fo'), inGrade=5, outGrade=6)
        l = db.Loan(person=db.Person(name='lol', firstname='Bar'), book=b,
                    given=date.today()
                    )

        l.delete()
        b.delete()

    @db_session
    def test_canDeleteBookWithoutRequest(self):
        b = db.Book(
            title='Bar', publisher=db.Publisher(
                name='Foo'), subject=db.Subject(
                name='Foo', tag='Fo'), inGrade=5, outGrade=6)

        b.delete()

    @db_session
    def test_cannotDeleteBookWithRequest(self):
        b = db.Book(
            title='Bar', publisher=db.Publisher(
                name='Foo'), subject=db.Subject(
                name='Foo', tag='Fo'), inGrade=5, outGrade=6)
        r = db.Request(person=db.Person(name='lol', firstname='Bar'), book=b)

        with self.assertRaises(core.ConstraintError):
            b.delete()

    @db_session
    def test_canDeleteBookAfterRequest(self):
        b = db.Book(
            title='Bar', publisher=db.Publisher(
                name='Foo'), subject=db.Subject(
                name='Foo', tag='Fo'), inGrade=5, outGrade=6)
        r = db.Request(person=db.Person(name='lol', firstname='Bar'), book=b)

        r.delete()
        b.delete()

    def test_canStringifyCurrency(self):
        s = Currency.to_string(0)
        self.assertEqual(s, '0,00€')

        s = Currency.to_string(1)
        self.assertEqual(s, '0,01€')

        s = Currency.to_string(12)
        self.assertEqual(s, '0,12€')

        s = Currency.to_string(10)
        self.assertEqual(s, '0,10€')

        s = Currency.to_string(123)
        self.assertEqual(s, '1,23€')

        s = Currency.to_string(1234)
        self.assertEqual(s, '12,34€')

        s = Currency.to_string(12345)
        self.assertEqual(s, '123,45€')

        s = Currency.to_string(895)
        self.assertEqual(s, '8,95€')

        s = Currency.to_string(895, addSymbol=False)
        self.assertEqual(s, '8,95')

    def test_canParseCurrencyString(self):
        i = Currency.from_string('123,45 €')
        self.assertEqual(i, 12345)

        i = Currency.from_string('12,34€')
        self.assertEqual(i, 1234)

        i = Currency.from_string('1,23€')
        self.assertEqual(i, 123)

        i = Currency.from_string('0,12€')
        self.assertEqual(i, 12)

        i = Currency.from_string('0,10€')
        self.assertEqual(i, 10)

        i = Currency.from_string('0,01€')
        self.assertEqual(i, 1)

        i = Currency.from_string('0,00€')
        self.assertEqual(i, 0)

        i = Currency.from_string('12€')
        self.assertEqual(i, 1200)

        i = Currency.from_string('8,95€')
        self.assertEqual(i, 895)

    @db_session
    def test_Loan_isPending(self):
        b = db.Book(
            title='Bar', publisher=db.Publisher(
                name='Foo'), subject=db.Subject(
                name='Foo', tag='Fo'), inGrade=5, outGrade=6)
        s = db.Student(
            person=db.Person(
                name='Foo', firstname='Bar'), class_=db.Class(
                grade=7, tag='b'))
        l = db.Loan(person=s.person, book=b, given=date.today())
        self.assertFalse(l.is_pending())

        s = db.Student(
            person=db.Person(
                name='Foo', firstname='Bar'), class_=db.Class(
                grade=6, tag='b'))
        l = db.Loan(person=s.person, book=b, given=date.today())
        self.assertTrue(l.is_pending())

        s = db.Student(
            person=db.Person(
                name='Foo', firstname='Bar'), class_=db.Class(
                grade=5, tag='b'))
        l = db.Loan(person=s.person, book=b, given=date.today())
        self.assertFalse(l.is_pending())

        l = db.Loan(
            person=db.Person(
                name='Foo',
                firstname='Bar'),
            book=b,
            given=date.today())
        self.assertFalse(l.is_pending())

    @db_session
    def test_Loan_tooLate(self):
        b = db.Book(
            title='Bar', publisher=db.Publisher(
                name='Foo'), subject=db.Subject(
                name='Foo', tag='Fo'), inGrade=5, outGrade=6)
        s = db.Student(
            person=db.Person(
                name='Foo', firstname='Bar'), class_=db.Class(
                grade=7, tag='b'))
        l = db.Loan(person=s.person, book=b, given=date.today())
        self.assertTrue(l.too_late())

        s = db.Student(
            person=db.Person(
                name='Foo', firstname='Bar'), class_=db.Class(
                grade=6, tag='b'))
        l = db.Loan(person=s.person, book=b, given=date.today())
        self.assertFalse(l.too_late())

        l = db.Loan(
            person=db.Person(
                name='Foo',
                firstname='Bar'),
            book=b,
            given=date.today())
        self.assertFalse(l.too_late())
