#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pony.orm import *
import unittest
from pony import orm
import locale

from app.db import db


__author__ = "Christian Glöckner"

# -----------------------------------------------------------------------------


class Tests(unittest.TestCase):

    @staticmethod
    @db_session
    def prepare():
        # create teachers
        t1 = db.Teacher(
            person=db.Person(name='Glöckner', firstname='Christian'),
            tag='glö'
        )
        t2 = db.Teacher(
            person=db.Person(name='Thiele', firstname='Felix'),
            tag='thi'
        )

        # create some classes
        c1 = db.Class(grade=8, tag='a', teacher=t2)
        c2 = db.Class(grade=12, tag=t1.tag, teacher=t1)
        c3 = db.Class(grade=12, tag='lip')

        # create students
        s1 = db.Student(
            person=db.Person(name='Mustermann', firstname='Florian'),
            class_=c1
        )
        s2 = db.Student(
            person=db.Person(name='Schmidt', firstname='Fabian'),
            class_=c1
        )
        s3 = db.Student(
            person=db.Person(name='Schneider', firstname='Max'),
            class_=c2
        )

    def setUp(self):
        db.create_tables()

    def tearDown(self):
        db.drop_all_tables(with_all_data=True)

    @db_session
    def test_get_classes_count(self):
        Tests.prepare()

        n = get_classes_count()
        self.assertEqual(n, 3)

    @db_session
    def test_add_classes_regular_case(self):
        Tests.prepare()

        raw = "10b\n05a\n12Foo\n\n"
        add_classes(raw)

        sds = list(db.Class.select())
        self.assertEqual(len(sds), 6)
        self.assertEqual(sds[3].grade, 10)
        self.assertEqual(sds[4].grade, 5)
        self.assertEqual(sds[5].grade, 12)
        self.assertEqual(sds[3].tag, 'b')
        self.assertEqual(sds[4].tag, 'a')
        self.assertEqual(sds[5].tag, 'foo')

    @db_session
    def test_add_classes_already_existing(self):
        Tests.prepare()

        raw = "10B\n08a\n12Foo\n\n"
        with self.assertRaises(orm.core.ConstraintError):
            add_classes(raw)

    @db_session
    def test_get_student_count(self):
        Tests.prepare()

        n = get_student_count()
        self.assertEqual(n, 3)

    @db_session
    def test_add_students_for_existing_classes(self):
        Tests.prepare()

        raw = """08A\tSchneider\tPetra
12LIP\tMustermann\tThomas
"""
        add_students(raw)

        sds = list(db.Student.select())
        self.assertEqual(len(sds), 5)
        self.assertEqual(sds[3].class_, db.Class.get(grade=8, tag='a'))
        self.assertEqual(sds[4].class_, db.Class.get(grade=12, tag='lip'))
        self.assertEqual(sds[3].person.name, 'Schneider')
        self.assertEqual(sds[3].person.firstname, 'Petra')
        self.assertEqual(sds[4].person.name, 'Mustermann')
        self.assertEqual(sds[4].person.firstname, 'Thomas')

    @db_session
    def test_add_students_for_invalid_class(self):
        Tests.prepare()

        raw = """08A\tSchneider\tPetra
10C\tSonstwer\tBeispiel
12LIP\tMustermann\tThomas
"""
        with self.assertRaises(orm.core.ConstraintError):
            add_students(raw)

    @db_session
    def test_get_teacher_count(self):
        Tests.prepare()

        n = get_teacher_count()
        self.assertEqual(n, 2)

    @db_session
    def test_add_teachers_for_existing_classes(self):
        Tests.prepare()

        raw = """LIP\tLippmann\tIris
bsp\tBeispiel\tPeter

Mus\tMustermann\tMax
"""
        add_teachers(raw)

        ts = list(db.Teacher.select())
        self.assertEqual(len(ts), 5)
        self.assertEqual(ts[2].tag, 'lip')
        self.assertEqual(ts[3].tag, 'bsp')
        self.assertEqual(ts[4].tag, 'mus')
        self.assertEqual(ts[2].person.name, 'Lippmann')
        self.assertEqual(ts[2].person.firstname, 'Iris')
        self.assertEqual(ts[3].person.name, 'Beispiel')
        self.assertEqual(ts[3].person.firstname, 'Peter')
        self.assertEqual(ts[4].person.name, 'Mustermann')
        self.assertEqual(ts[4].person.firstname, 'Max')

    @db_session
    def test_add_teachers_with_invalid_tag(self):
        Tests.prepare()

        raw = "glö\tA\tB"
        with self.assertRaises(orm.core.CacheIndexError):
            add_teachers(raw)

    @db_session
    def test_get_class_grades(self):
        Tests.prepare()

        gs = get_class_grades()
        self.assertEqual(len(gs), 2)
        self.assertIn(8, gs)
        self.assertIn(12, gs)

    @db_session
    def test_get_class_tags(self):
        Tests.prepare()

        tgs = get_class_tags(12)
        self.assertEqual(len(tgs), 2)
        self.assertIn('glö', tgs)
        self.assertIn('lip', tgs)

        tgs = get_class_tags(8)
        self.assertEqual(len(tgs), 1)
        self.assertIn('a', tgs)

    @db_session
    def test_get_classes(self):
        Tests.prepare()

        cs = get_classes()
        self.assertEqual(len(cs), 3)
        self.assertIn(db.Class[1], cs)
        self.assertIn(db.Class[2], cs)
        self.assertIn(db.Class[3], cs)

    @db_session
    def test_get_classes_by_grade(self):
        Tests.prepare()

        # single class
        cs = get_classes_by_grade(8)
        self.assertEqual(len(cs), 1)
        self.assertIn(db.Class[1], cs)

        # multiple classes
        cs = get_classes_by_grade(12)
        self.assertEqual(len(cs), 2)
        self.assertIn(db.Class[2], cs)
        self.assertIn(db.Class[3], cs)

        # no classes
        cs = get_classes_by_grade(9)
        self.assertEqual(len(cs), 0)

    @db_session
    def test_sort_students(self):
        Tests.prepare()

        db.Student(
            person=db.Person(
                name='Öbla',
                firstname='Cäsar'),
            class_=db.Class[3])
        db.Student(
            person=db.Person(
                name='Öbla',
                firstname='Carl'),
            class_=db.Class[3])
        db.Student(
            person=db.Person(
                name='Ober',
                firstname='Unter'),
            class_=db.Class[3])
        db.Student(
            person=db.Person(
                name='Daumen',
                firstname='Zehe'),
            class_=db.Class[3])

        # query and sort all students
        students = list(db.Class[3].student)
        sort_students(students)

        self.assertEqual(len(students), 4)
        self.assertEqual(students[0].person.name, 'Daumen')
        self.assertEqual(students[1].person.name, 'Ober')
        self.assertEqual(students[2].person.name, 'Öbla')
        self.assertEqual(students[2].person.firstname, 'Carl')
        self.assertEqual(students[3].person.name, 'Öbla')
        self.assertEqual(students[3].person.firstname, 'Cäsar')

    @db_session
    def test_get_students_like(self):
        Tests.prepare()

        # by name
        st = get_students_like(name='ch')
        self.assertEqual(len(st), 2)
        self.assertIn(db.Student[2], st)
        self.assertIn(db.Student[3], st)

        # by firstname
        st = get_students_like(firstname='ia')
        self.assertEqual(len(st), 2)
        self.assertIn(db.Student[1], st)
        self.assertIn(db.Student[2], st)

        # using both
        st = get_students_like(name='ch', firstname='ia')
        self.assertEqual(len(st), 1)
        self.assertIn(db.Student[2], st)

        # search should ignore cases
        st = get_students_like(name='sch', firstname='A')
        self.assertEqual(len(st), 2)
        self.assertIn(db.Student[2], st)
        self.assertIn(db.Student[3], st)

    @db_session
    def test_advance_school_year(self):
        Tests.prepare()

        db.Class(grade=7, tag='a')
        db.Class(grade=9, tag='a')

        # delete 12th grade students to avoid delete restriction
        delete(s for s in db.Class[2].student)
        delete(s for s in db.Class[3].student)

        # advance to a new year with three 5th grades
        advance_school_year(12, 5, ['a', 'b', 'c'])

        # check existing classes
        c9a = db.Class[1]
        c8a = db.Class[4]
        c10a = db.Class[5]
        c5a = db.Class[6]
        c5b = db.Class[7]
        c5c = db.Class[8]

        self.assertEqual(c9a.grade, 9)
        self.assertEqual(c8a.grade, 8)
        self.assertEqual(c10a.grade, 10)
        self.assertEqual(c5a.grade, 5)
        self.assertEqual(c5b.grade, 5)
        self.assertEqual(c5c.grade, 5)
        self.assertEqual(c5a.tag, 'a')
        self.assertEqual(c5b.tag, 'b')
        self.assertEqual(c5c.tag, 'c')

        cs = get_classes()
        self.assertEqual(len(cs), 6)

        # check existing students
        self.assertEqual(db.Student[1].class_, c9a)
        self.assertEqual(db.Student[2].class_, c9a)

    @db_session
    def test_advanceMultipleSchoolYears(self):
        Tests.prepare()

        # clear students to avoid delete restriction
        delete(s for s in db.Student)

        # 8a; 12glö, 12lip

        advance_school_year(12, 5, ['a', 'b', 'c'])

        cs = get_classes()
        self.assertEqual(len(cs), 4)

        # 5a, 5b, 5c; 9a

        advance_school_year(12, 5, ['a', 'b', 'c', 'd'])

        cs = get_classes()
        self.assertEqual(len(cs), 8)

        # 5a, 5b, 5c, 5d; 6a, 6b, 6c; 10a

        advance_school_year(12, 5, ['a', 'b'])

        cs = get_classes()
        self.assertEqual(len(cs), 10)

        # 5a, 5b; 6a, 6b, 6c, 6d; 7a, 7b, 7c; 11a

        advance_school_year(12, 5, ['a', 'b', 'c'])

        cs = get_classes()
        self.assertEqual(len(cs), 13)

        # 5a, 5b, 5c; 6a, 6b; 7a, 7b, 7c, 7d; 8a, 8b, 8c; 12a

        advance_school_year(12, 5, ['a', 'b', 'c'])

        cs = get_classes()
        self.assertEqual(len(cs), 15)

        # 5a, 5b, 5c; 6a, 6b, 6c; 7a, 7b; 8a, 8b, 8c, 8d; 9a, 9b, 9c
