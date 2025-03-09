#!/usr/bin/python3
# -*- coding: utf-8 -*-

import webtest
import unittest
import os
import time
import math
import sys
import shutil
from datetime import datetime

from bottle import *
from pony import orm

from app.db import db, db_session, DemandManager
from app.db import orga_queries as orga
from app.db import book_queries as books
from app.db import loan_queries as loans
from app import Settings
from app.tex import *
from app.xls import *
from app.utils import errorhandler


__author__ = "Christian Glöckner"



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
        bottleapp = default_app()
        bottleapp.catchall = False
        self.app = webtest.TestApp(bottleapp)

    def tearDown(self):
        self.app = None
        db.drop_all_tables(with_all_data=True)

    # -------------------------------------------------------------------------

    @db_session
    def test_subjects_gui(self):
        Tests.prepare()

        # show subjects gui
        ret = self.app.get('/admin/subjects')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_subjects_add_new(self):
        Tests.prepare()

        # add subjects
        args = {
            "data": "Fr\tFranzösisch\nDe\tDeutsch"
        }
        ret = self.app.post('/admin/subjects/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # show subjects list
        ret = self.app.get('/admin/subjects')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_subjects_add_invalid(self):
        Tests.prepare()

        # add subjects (Ma-tag already used)
        args = {
            "data": "Fr\tFranzösisch\nMa\tMathematik\nDe\tDeutsch"
        }
        ret = self.app.post('/admin/subjects/add', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show subjects list
        ret = self.app.get('/admin/subjects')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_subjects_add_ignore_empty_lines(self):
        Tests.prepare()

        # add subjects
        args = {"data": "Fr\tFranzösisch\n\nDe\tDeutsch\n"}
        ret = self.app.post('/admin/subjects/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # show subjects gui
        ret = self.app.get('/admin/subjects')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_subjects_edit_gui(self):
        Tests.prepare()

        # show valid subject's edit gui
        ret = self.app.get('/admin/subjects/edit/1')
        self.assertEqual(ret.status_int, 200)

        # show invalid subject's edit gui
        ret = self.app.get('/admin/subjects/edit/1337', expect_errors=True)
        self.assertEqual(ret.status_int, 400)

    @db_session
    def test_subjects_edit_post(self):
        Tests.prepare()

        # edit subject
        args = {'tag': 'Sk', 'name': 'Sozialkunde', 'elective': 'on'}
        ret = self.app.post('/admin/subjects/edit/1', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        sj = db.Subject[1]
        self.assertEqual(sj.tag, args['tag'])
        self.assertEqual(sj.name, args['name'])
        self.assertEqual(sj.elective, True)

        # show subjects gui
        ret = self.app.get('/admin/subjects')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_subjects_edit_invalid_post(self):
        Tests.prepare()

        # edit subject (tag is used by #1)
        args = {'tag': 'Ma', 'name': 'Sozialkunde'}
        ret = self.app.post('/admin/subjects/edit/2', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show subjects gui
        ret = self.app.get('/admin/subjects')
        self.assertEqual(ret.status_int, 200)

        # edit subject (invalid target id)
        args = {'tag': 'Sk', 'name': 'Sozialkunde'}
        ret = self.app.post(
            '/admin/subjects/edit/1337',
            args,
            expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show subjects gui (once again)
        ret = self.app.get('/admin/subjects')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_subjects_delete(self):
        Tests.prepare()

        # delete subject
        ret = self.app.post('/admin/subjects/delete/1')
        self.assertEqual(ret.status_int, 302)  # 302=redirect

    @db_session
    def test_subjects_delete_invalid(self):
        Tests.prepare()

        # delete subject
        ret = self.app.post('/admin/subjects/delete/1337', expect_errors=True)
        self.assertEqual(ret.status_int, 400)

    # -------------------------------------------------------------------------

    @db_session
    def test_publishers_gui(self):
        Tests.prepare()

        # show publishers gui
        ret = self.app.get('/admin/publishers')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_publishers_add_new(self):
        Tests.prepare()

        # add subjects
        args = {
            "data": "C. C. Buchner\nWestermann"
        }
        ret = self.app.post('/admin/publishers/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        self.assertEqual(db.Publisher[3].name, 'C. C. Buchner')
        self.assertEqual(db.Publisher[4].name, 'Westermann')

        # show subjects list
        ret = self.app.get('/admin/publishers')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_publishers_add_invalid(self):
        Tests.prepare()

        # add subjects (2nd already used)
        args = {
            "data": "C. C. Buchner\nKlett\nWestermann"
        }
        ret = self.app.post('/admin/publishers/add', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show publishers list
        ret = self.app.get('/admin/publishers')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_publishers_add_ignore_empty_lines(self):
        Tests.prepare()

        # add subjects
        args = {"data": "C. C. Buchner\n\nWestermann\n"}
        ret = self.app.post('/admin/publishers/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # show subjects gui
        ret = self.app.get('/admin/publishers')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_publishers_edit_gui(self):
        Tests.prepare()

        # show valid publisher's edit gui
        ret = self.app.get('/admin/publishers/edit/1')
        self.assertEqual(ret.status_int, 200)

        # show invalid publisher's edit gui
        ret = self.app.get('/admin/publishers/edit/1337', expect_errors=True)
        self.assertEqual(ret.status_int, 400)

    @db_session
    def test_publishers_edit_post(self):
        Tests.prepare()

        # edit subject
        args = {'name': 'Volk und Wissen'}
        ret = self.app.post('/admin/publishers/edit/1', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        self.assertEqual(db.Publisher[1].name, args['name'])

        # show publishers gui
        ret = self.app.get('/admin/publishers')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_publishers_edit_invalid_post(self):
        Tests.prepare()

        # edit publisher (name is used by #1)
        args = {'name': 'Cornelsen'}
        ret = self.app.post(
            '/admin/publishers/edit/2',
            args,
            expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show publishers gui
        ret = self.app.get('/admin/publishers')
        self.assertEqual(ret.status_int, 200)

        # edit publisher (invalid target id)
        args = {'name': 'Volk und Wissen'}
        ret = self.app.post(
            '/admin/publishers/edit/1337',
            args,
            expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show publishers gui (once again)
        ret = self.app.get('/admin/publishers')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_publishers_delete(self):
        Tests.prepare()

        p = db.Publisher(name='dummy to delete')
        db.flush()

        # delete publisher
        ret = self.app.post('/admin/publishers/delete/{0}'.format(p.id))
        self.assertEqual(ret.status_int, 302)  # 302=redirect

    @db_session
    def test_publishers_delete_invalid(self):
        Tests.prepare()

        # delete publisher
        ret = self.app.post(
            '/admin/publishers/delete/1337',
            expect_errors=True)
        self.assertEqual(ret.status_int, 400)

    # -------------------------------------------------------------------------

    @db_session
    def test_books_gui(self):
        Tests.prepare()

        # show books gui
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_books_add_new(self):
        Tests.prepare()

        # add books
        args = {
            "data": """Titel\t0815-000\t1234\tKlett\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t
Titel2\t0815-001\t1234\tKlett\t10\t12\tEng\tTrue\tFalse\tFalse\tFalse\tTrue\t
Titel3\t0815-002\t1234\tKlett\t10\t12\tRu\tTrue\tFalse\tFalse\tFalse\tTrue\tBla"""}
        ret = self.app.post('/admin/books/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # shhhh, I'm to lazy to test all three books completely .__.
        self.assertEqual(db.Book[10].title, 'Titel')
        self.assertEqual(db.Book[11].subject.tag, 'Eng')
        self.assertEqual(db.Book[12].comment, 'Bla')

        # show books list
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_books_add_ignore_newlines(self):
        Tests.prepare()

        # add books
        args = {
            "data": """Titel\t0815-000\t1234\tKlett\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t


Titel2\t0815-001\t1234\tKlett\t10\t12\tEng\tTrue\tFalse\tFalse\tFalse\tTrue\t

Titel3\t0815-002\t1234\tKlett\t10\t12\tRu\tTrue\tFalse\tFalse\tFalse\tTrue\t
"""}
        ret = self.app.post('/admin/books/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # show books list
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_books_add_minimal_data(self):
        Tests.prepare()

        # add book (invalid publisher)
        args = {"data": "Titel\t\t\tKlett\t10\t12"}
        ret = self.app.post('/admin/books/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        bk = db.Book[10]
        self.assertEqual(bk.title, 'Titel')
        self.assertEqual(bk.publisher.name, 'Klett')
        self.assertEqual(bk.inGrade, 10)
        self.assertEqual(bk.outGrade, 12)
        self.assertTrue(bk.for_loan)

        # show books list
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_books_add_invalid_data(self):
        Tests.prepare()

        # add book (invalid publisher)
        args = {
            "data": "Titel\t0815-000\t1234\tUnbekannt\t39\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t"}
        ret = self.app.post('/admin/books/add', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show books list
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

        # add book (invalid subject)
        args = {
            "data": "Titel\t0815-000\t1234\tKlett\t39\t10\t12\tFoo\tTrue\tFalse\tFalse\tFalse\tTrue\t"}
        ret = self.app.post('/admin/books/add', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # add book (invalid price)
        args = {
            "data": "Titel\t0815-000\tabc\tKlett\t39\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t"}
        ret = self.app.post('/admin/books/add', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # add books (invalid inGrade)
        args = {
            "data": "Titel\t0815-000\t1234\tKlett\t39\tZehn\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t"}
        ret = self.app.post('/admin/books/add', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # add books (invalid outGrade)
        args = {
            "data": "Titel\t0815-000\t1234\tKlett\t39\t10\tAbi\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t"}
        ret = self.app.post('/admin/books/add', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show books list (again)
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_books_edit_gui(self):
        Tests.prepare()

        # show valid book's edit gui
        ret = self.app.get('/admin/books/edit/1')
        self.assertEqual(ret.status_int, 200)

        # show invalid book's edit gui
        ret = self.app.get('/admin/books/edit/1337', expect_errors=True)
        self.assertEqual(ret.status_int, 400)

    @db_session
    def test_books_edit_post(self):
        Tests.prepare()

        # edit book
        args = {
            "title": "Biologie Hautnah",
            "isbn": "0815-346465-7-346",
            "price": "123",
            "publisher_id": "1",
            "stock": "39",
            "inGrade": "10",
            "outGrade": "12",
            "subject_id": "2",
            "novices": "on",
            "advanced": "on",  # @NOTE: empty str?
            "workbook": "on",  # @NOTE: empty str?
            "classsets": "on",
            "for_loan": "off",
            "comment": ""
        }
        ret = self.app.post('/admin/books/edit/1', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        bk = db.Book[1]
        self.assertEqual(bk.title, args['title'])
        self.assertEqual(bk.isbn, args['isbn'])
        self.assertEqual(bk.price, 12300)  # as cents
        self.assertEqual(bk.publisher.id, 1)
        self.assertEqual(bk.stock, 39)
        self.assertEqual(bk.inGrade, 10)
        self.assertEqual(bk.outGrade, 12)
        self.assertEqual(bk.subject.id, 2)
        self.assertTrue(bk.novices)
        self.assertTrue(bk.advanced)
        self.assertTrue(bk.workbook)
        self.assertTrue(bk.classsets)
        self.assertFalse(bk.for_loan)
        self.assertEqual(bk.comment, args['comment'])

        # show books gui
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_books_edit_invalid_post(self):
        Tests.prepare()

        # edit book (invalid publisher, invalid subject)
        args = {
            "title": "Biologie Hautnah",
            "isbn": "0815-346465-7-346",
            "price": "1234",
            "publisher_id": "1337",
            "stock": "39",
            "inGrade": "10",
            "outGrade": "12",
            "subject_id": "2346345",
            "novices": "on",
            "advanced": "off",  # @NOTE: empty str?
            "workbook": "off",  # @NOTE: empty str?
            "classsets": "off",
            "for_loan": "off",
            "comment": ""
        }
        ret = self.app.post('/admin/books/edit/2', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show books gui
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

        # edit book (invalid target id)
        args = {
            "title": "Biologie Hautnah",
            "isbn": "0815-346465-7-346",
            "price": "1234",
            "publisher_id": "1",
            "stock": "39",
            "inGrade": "10",
            "outGrade": "12",
            "subject_id": "2",
            "novices": "on",
            "advanced": "off",  # @NOTE: empty str?
            "workbook": "off",  # @NOTE: empty str?
            "classsets": "off",
            "for_loan": "off",
            "comment": ""
        }
        ret = self.app.post('/admin/books/edit/1337', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

        # show books gui (once again)
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_books_delete(self):
        Tests.prepare()

        # delete book
        ret = self.app.post('/admin/books/delete/1')
        self.assertEqual(ret.status_int, 302)  # 302=redirect

    @db_session
    def test_books_delete_invalid(self):
        Tests.prepare()

        # delete book
        ret = self.app.post('/admin/books/delete/1337', expect_errors=True)
        self.assertEqual(ret.status_int, 400)

    # -------------------------------------------------------------------------

    @db_session
    def test_classes_gui(self):
        Tests.prepare()

        # show classes gui
        ret = self.app.get('/admin/classes')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_classes_add(self):
        Tests.prepare()

        # add classes
        args = {"data": "09a\n05c\n\n11foo\n\n"}
        ret = self.app.post('/admin/classes/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # test new classes
        self.assertEqual(db.Class[4].grade, 9)
        self.assertEqual(db.Class[5].grade, 5)
        self.assertEqual(db.Class[6].grade, 11)
        self.assertEqual(db.Class[4].tag, 'a')
        self.assertEqual(db.Class[5].tag, 'c')
        self.assertEqual(db.Class[6].tag, 'foo')

        # show classes gui
        ret = self.app.get('/admin/books')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_classes_edit(self):
        Tests.prepare()

        # edit class
        args = {"grade": 5, "tag": "d", "teacher_id": 1}
        ret = self.app.post('/admin/classes/edit/1', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # test changed class
        cs = db.Class[1]
        self.assertEqual(cs.grade, 5)
        self.assertEqual(cs.tag, "d")
        self.assertEqual(cs.teacher, db.Teacher[1])

    @db_session
    def test_classes_edit_can_reset_teacher(self):
        Tests.prepare()

        # edit class
        args = {"grade": 5, "tag": "d", "teacher_id": 0}
        ret = self.app.post('/admin/classes/edit/1', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # test changed class
        cs = db.Class[1]
        self.assertEqual(cs.grade, 5)
        self.assertEqual(cs.tag, "d")
        self.assertEqual(cs.teacher, None)

    @db_session
    def test_classes_edit_invalid_class(self):
        Tests.prepare()

        # edit class
        args = {"grade": 8, "tag": "a", "teacher_id": 0}
        ret = self.app.post('/admin/classes/edit/2', args, expect_errors=True)
        self.assertEqual(ret.status_int, 400)

    @db_session
    def test_classes_edit_can_keep_class_name(self):
        Tests.prepare()

        # edit class
        args = {"grade": 8, "tag": "a", "teacher_id": 0}
        ret = self.app.post('/admin/classes/edit/1', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

    @db_session
    def test_classes_delete(self):
        Tests.prepare()

        # add empty class
        args = {"data": "09a"}
        ret = self.app.post('/admin/classes/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # delete class --> prompt
        ret = self.app.post('/admin/classes/delete/4')
        self.assertEqual(ret.status_int, 200)  # 302=redirect

        # delete class --> prompt
        ret = self.app.get('/admin/classes/delete/4/confirm')
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # try access deleted class
        with self.assertRaises(orm.core.ObjectNotFound):
            cs = db.Class[4]

    # -----------------------------------------------------------------------------

    @db_session
    def test_students_gui(self):
        Tests.prepare()

        # show students gui
        ret = self.app.get('/admin/students')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_students_add(self):
        Tests.prepare()

        # add students
        args = {"data": "08a\tMustermann\tJürgen\n\n12glö\ta\tb\n"}
        ret = self.app.post('/admin/students/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # test new students
        self.assertEqual(db.Student[4].person.name, "Mustermann")
        self.assertEqual(db.Student[4].person.firstname, "Jürgen")
        self.assertEqual(db.Student[4].class_, db.Class.get(grade=8, tag='a'))
        self.assertEqual(db.Student[5].person.name, "a")
        self.assertEqual(db.Student[5].person.firstname, "b")
        self.assertEqual(
            db.Student[5].class_,
            db.Class.get(
                grade=12,
                tag='glö'))

        # show students gui
        ret = self.app.get('/admin/students')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_students_search(self):
        Tests.prepare()

        # search for all students
        args = {"name": "", "firstname": ""}
        ret = self.app.post('/admin/students/search', args)
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_students_edit(self):
        Tests.prepare()

        # edit student
        args = {"name": "A", "firstname": "B", "class_id": 2}
        ret = self.app.post('/admin/students/edit/1', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # test changed student
        st = db.Student[1]
        self.assertEqual(st.person.name, 'A')
        self.assertEqual(st.person.firstname, 'B')
        self.assertEqual(st.class_, db.Class[2])

    @db_session
    def test_students_delete(self):
        Tests.prepare()

        # delete class
        ret = self.app.post('/admin/students/delete/1')
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # tra access deleted student
        with self.assertRaises(orm.core.ObjectNotFound):
            cs = db.Student[1]

    # -----------------------------------------------------------------------------

    @db_session
    def test_teachers_gui(self):
        Tests.prepare()

        # show teachers gui
        ret = self.app.get('/admin/teachers')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_teachers_add(self):
        Tests.prepare()

        # add teachers
        args = {"data": "tei\tTeichert\tHolger\n"}
        ret = self.app.post('/admin/teachers/add', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # test new students
        self.assertEqual(db.Teacher[3].tag, "tei")
        self.assertEqual(db.Teacher[3].person.name, "Teichert")
        self.assertEqual(db.Teacher[3].person.firstname, "Holger")

        # show students gui
        ret = self.app.get('/admin/teachers')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_teachers_edit(self):
        Tests.prepare()

        # edit teacher
        args = {"name": "A", "firstname": "B", "tag": "C"}
        ret = self.app.post('/admin/teachers/edit/1', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # test changed teacher
        tr = db.Teacher[1]
        self.assertEqual(tr.person.name, 'A')
        self.assertEqual(tr.person.firstname, 'B')
        self.assertEqual(tr.tag, 'c')

    @db_session
    def test_teachers_delete(self):
        Tests.prepare()

        # delete class
        ret = self.app.post('/admin/teachers/delete/1')
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # tra access deleted student
        with self.assertRaises(orm.core.ObjectNotFound):
            cs = db.Teacher[1]

    # -----------------------------------------------------------------------------

    @db_session
    def test_settings_ui(self):
        ret = self.app.get('/admin/settings')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_settings_post(self):
        s = Settings()
        s.load_from(s)

        args = {
            'school_year': s.data['general']['school_year'],
            'deadline_changes': '19.06.',
            'deadline_booklist': '23.03.',
            'bookreturn_graduate': '23.03.'
        }
        ret = self.app.post('/admin/settings', args)

        # override test-settings with original settings
        s.save()

        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # show settings gui
        ret = self.app.get('/admin/settings')
        self.assertEqual(ret.status_int, 200)

    # -------------------------------------------------------------------------

    @db_session
    def test_booklist_creation(self):
        Tests.prepare()

        # create all booklists (some even without books)
        # note: this may take some seconds
        ret = self.app.post('/admin/lists/generate/booklist')
        self.assertEqual(ret.status_code, 200)

        # show lists index
        ret = self.app.get('/admin/lists')
        self.assertEqual(ret.status_code, 200)

    @db_session
    def test_requestlist_creation(self):
        Tests.prepare()

        # create requestlists (some even without books)
        ret = self.app.get('/admin/lists/generate/requestlist')
        self.assertEqual(ret.status_code, 200)

        # show lists index
        ret = self.app.get('/admin/lists')
        self.assertEqual(ret.status_code, 200)

    @db_session
    def test_bookreturn_creation(self):
        Tests.prepare()

        # create bookreturn
        ret = self.app.get('/admin/lists/generate/bookreturn')
        self.assertEqual(ret.status_code, 200)

        # show lists index
        ret = self.app.get('/admin/lists')
        self.assertEqual(ret.status_code, 200)

    # -------------------------------------------------------------------------

    @db_session
    def test_demand_generation(self):
        Tests.prepare()

        # show demand form
        ret = self.app.get('/admin/demand')
        self.assertEqual(ret.status_code, 200)

        # build random demand post (and change path)
        global demand_json
        demand_json = '/tmp/demand.json'

        args = dict()
        args["lowering"] = '10'
        for grade in orga.get_secondary_level1_range():
            for sub in books.get_subjects(elective=True):
                key = "%s_%s" % (grade, sub.tag)
                args[key] = 63
        for grade in [11, 12]:
            for level in ['novices', 'advanced']:
                for sub in books.get_subjects():
                    key = "%s_%s_%s" % (grade, sub.tag, level)
                    args[key] = 23

        # post demand
        ret = self.app.post('/admin/demand', args)
        self.assertEqual(ret.status_code, 200)

        # show demand form (again)
        ret = self.app.get('/admin/demand')
        self.assertEqual(ret.status_code, 200)
