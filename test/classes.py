#!/usr/bin/python3
# -*- coding: utf-8 -*-

import webtest
import unittest
import os
import time
from datetime import datetime

from bottle import *
from pony import orm

from app.db import db, db_session
from app.db import orga_queries
from app.db import book_queries
from app.db import loan_queries
from app.utils import errorhandler


__author__ = "Christian Glöckner"



class Tests(unittest.TestCase):

    @staticmethod
    @db_session
    def prepare():
        import db.orga
        import db.books

        db.orga_queries.Tests.prepare()
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
    def test_class_index(self):
        Tests.prepare()

        # show class index
        ret = self.app.get('/classes')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_grade_index(self):
        Tests.prepare()

        # show grade index
        ret = self.app.get('/classes/8')
        self.assertEqual(ret.status_int, 200)

        # show grade index (empty because 7th grade not present)
        ret = self.app.get('/classes/7')
        self.assertEqual(ret.status_int, 200)

        # show grade index
        ret = self.app.get('/classes/12')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_class_overview(self):
        Tests.prepare()

        # show class overview
        ret = self.app.get('/classes/8/a')
        self.assertEqual(ret.status_int, 200)

        # show class overview (7th grade not present)

        ret = self.app.get('/classes/8/b', expect_errors=True)
        self.assertEqual(ret.status_int, 404)  # 404=not found

        # show class overview
        ret = self.app.get('/classes/12/lip')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_requests_overview(self):
        Tests.prepare()

        # show requests overview
        ret = self.app.get('/classes/requests/8/a/full')
        self.assertEqual(ret.status_int, 200)

        # show requests overview (7th grade not present)
        ret = self.app.get('/classes/requests/8/b/full', expect_errors=True)
        self.assertEqual(ret.status_int, 404)  # 404=not found

        # show requests overview
        ret = self.app.get('/classes/requests/12/lip/full')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_requests_post(self):
        Tests.prepare()

        ma = db.Subject.get(tag='Ma')
        eng = db.Subject.get(tag='Eng')

        # add some books for 8th grade
        b1 = db.Book(title='Math 8', publisher=db.Publisher[1], inGrade=8,
                     outGrade=8, subject=ma)
        b2 = db.Book(title='English B', publisher=db.Publisher[1], inGrade=7,
                     outGrade=8, subject=eng)

        # show requests overview
        ret = self.app.get('/classes/requests/8/a/full')
        self.assertEqual(ret.status_int, 200)

        # post requests
        args = {}
        for b in [b1, b2]:
            for s in db.Class.get(grade=8, tag='a').student:
                key = '%d_%d' % (s.id, b.id)
                args[key] = 'on'

        ret = self.app.post('/classes/requests/8/a/full', args)
        self.assertEqual(ret.status_int, 302)  # 302=redirect

        # show requests overview (again)
        ret = self.app.get('/classes/requests/8/a/full')
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_loans_post(self):
        Tests.prepare()

        ma = db.Subject.get(tag='Ma')
        eng = db.Subject.get(tag='Eng')

        # add some books for 8th grade
        b1 = db.Book(title='Math 8', publisher=db.Publisher[1], inGrade=8,
                     outGrade=8, subject=ma)
        b2 = db.Book(title='English B', publisher=db.Publisher[1], inGrade=7,
                     outGrade=8, subject=eng)

        # show class overview
        ret = self.app.get('/classes/8/a')
        self.assertEqual(ret.status_int, 200)

        # post requests
        args = {}
        for b in [b1, b2]:
            for s in db.Class.get(grade=8, tag='a').student:
                key = '%d_%d' % (s.id, b.id)
                args[key] = '1'

        ret = self.app.post('/classes/loans/8/a', args)
        self.assertEqual(ret.status_int, 302)  # redirect

        # show class overview (again)
        ret = self.app.get('/classes/8/a')
        self.assertEqual(ret.status_int, 200)
