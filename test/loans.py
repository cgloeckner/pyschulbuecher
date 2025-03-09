#!/usr/bin/python3
# -*- coding: utf-8 -*-

import webtest
import unittest
import os
import time
import json
from datetime import datetime

from bottle import *
from pony import orm

from app import db, db_session
from app.db import orga_queries
from app.db import book_queries
from app.db import loan_queries

from app.utils import errorhandler


__author__ = "Christian Glöckner"




# -----------------------------------------------------------------------------


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
    def test_loan_person_overview_request_unrequest_borrow_return(self):
        Tests.prepare()

        s = db.Student[3]

        # show person's loan overview without any
        ret = self.app.get('/loan/person/%d' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

        # request books
        loan_queries.update_request(s, db.Book[3], True)
        loan_queries.update_request(s, db.Book[5], True)

        # show person's loan overview (requests only)
        ret = self.app.get('/loan/person/%d' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

        # loan books
        loan_queries.update_loan(s.person, db.Book[2], True)
        loan_queries.update_loan(s.person, db.Book[1], True)
        loan_queries.update_loan(s.person, db.Book[4], True)

        # show person's loan overview (requests and loans)
        ret = self.app.get('/loan/person/%d' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

        # unregister requests
        loan_queries.update_request(s, db.Book[3], False)
        loan_queries.update_request(s, db.Book[5], False)

        # show person's loan overview (loans only)
        ret = self.app.get('/loan/person/%d' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

        # return books
        loan_queries.update_loan(s.person, db.Book[2], False)
        loan_queries.update_loan(s.person, db.Book[1], False)
        loan_queries.update_loan(s.person, db.Book[4], False)

        # show person's loan overview without any
        ret = self.app.get('/loan/person/%d' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

    @db_session
    def test_loan_person_loan_adding_form(self):
        Tests.prepare()

        s = db.Student[3]

        # show person's loan add ui
        ret = self.app.get('/loan/person/%d/add' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

        # query books by subject #1
        args = {}
        args["classsets"] = "true"
        args["value"] = 1
        args["person_id"] = s.person.id
        args["by"] = "subject"
        ret = self.app.get('/loan/ajax/books', args)
        self.assertEqual(ret.status_int, 200)

        # query books by 7th grade
        args = {}
        args["classsets"] = "true"
        args["value"] = 7
        args["person_id"] = s.person.id
        args["by"] = "grade"
        ret = self.app.get('/loan/ajax/books', args)
        self.assertEqual(ret.status_int, 200)

        # borrow some books
        args = {}
        args[3] = '5'
        args[3] = 'foo'  # should be ignored
        ret = self.app.post('/loan/person/%d/add' % (s.person.id), args)
        self.assertEqual(ret.status_int, 302)  # redirect
