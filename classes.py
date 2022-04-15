#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, time
from datetime import datetime

from bottle import *
from pony import orm

from db.orm import db, db_session, Currency
from db import orga, books, loans
from utils import errorhandler


__author__ = "Christian Glöckner"


@get('/classes')
@view('classes/class_index')
def class_index():
    return dict()

@get('/classes/<grade:int>')
@view('classes/grade_index')
def classes_grade_index(grade):
    return dict(grade=grade)

@get('/classes/<grade:int>/<tag>')
@view('classes/students_index')
def classes_students_index(grade, tag):
    bks = books.getBooksUsedIn(grade)
    bks = books.orderBooksList(bks)
    bks.sort(key=lambda b: b.outGrade)
    c = orga.db.Class.get(grade=grade, tag=tag)
    if c is None:
        abort(404)
    return dict(grade=grade, tag=tag, books=bks, c=c)

# -----------------------------------------------------------------------------

@get('/classes/requests/<grade:int>/<tag>/<version>')
@view('classes/request_form')
def classes_requests_form(grade, tag, version):
    query_grade = grade
    if 'next' in version:
        query_grade += 1
    
    # query grade-specific books
    if tag.lower() == 'neu' or 'full' in version:
        bks = books.getBooksUsedIn(query_grade, True)
    else:
        bks = books.getBooksStartedIn(query_grade, True)
    # order queried books
    bks = books.orderBooksList(bks)
    
    # add misc books
    bks += list(books.getBooksUsedIn(0, True))
    c = orga.db.Class.get(grade=grade, tag=tag)
    if c is None:
        abort(404)
        
    return dict(grade=grade, tag=tag, books=bks, c=c, version=version)


@post('/classes/requests/<grade:int>/<tag>/<version>')
@errorhandler
def classes_requests_post(grade, tag, version):
    query_grade = grade
    if 'next' in version:
        query_grade += 1
    
    # query grade-specific books
    if tag.lower() == 'neu' or 'full' in version:
        bks = books.getBooksUsedIn(query_grade, True)
    else:
        bks = books.getBooksStartedIn(query_grade, True)
    # order queried books
    bks = books.orderBooksList(bks)
    
    # add misc books
    bks += list(books.getBooksUsedIn(0, True))
    for s in orga.getStudentsIn(grade, tag):
        for b in bks:
            key    = "%d_%d" % (s.id, b.id)
            status = request.forms.get(key) == 'on'
            loans.updateRequest(s, b, status)
    
    db.commit()
    redirect('/classes/%d' % (grade))

# -----------------------------------------------------------------------------

@post('/classes/loans/<grade:int>/<tag>')
@errorhandler
def classes_loans_post(grade, tag):
    bks = books.getBooksUsedIn(grade, True)
    for s in orga.getStudentsIn(grade, tag):
        for b in bks:
            key   = "%d_%d" % (s.id, b.id)
            count = request.forms.get(key)
            if count is None or count == "":
                count = 0
            else:
                count = int(count)
            loans.updateLoan(s.person, b, count)
    
    db.commit()
    redirect('/classes/%d' % (grade))

# -----------------------------------------------------------------------------

import unittest, webtest

class Tests(unittest.TestCase):

    @staticmethod
    @db_session
    def prepare():
        import db.orga, db.books
        
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
        self.assertEqual(ret.status_int, 404) # 404=not found
        
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
        self.assertEqual(ret.status_int, 404) # 404=not found
        
        # show requests overview
        ret = self.app.get('/classes/requests/12/lip/full')
        self.assertEqual(ret.status_int, 200)
    
    @db_session
    def test_requests_post(self):
        Tests.prepare()
        
        ma  = db.Subject.get(tag='Ma')
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
        self.assertEqual(ret.status_int, 302) # 302=redirect
    
        # show requests overview (again)
        ret = self.app.get('/classes/requests/8/a/full')
        self.assertEqual(ret.status_int, 200)
        
    @db_session
    def test_loans_post(self):
        Tests.prepare()
        
        ma  = db.Subject.get(tag='Ma')
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
        self.assertEqual(ret.status_int, 302) # redirect
    
        # show class overview (again)
        ret = self.app.get('/classes/8/a')
        self.assertEqual(ret.status_int, 200)
        
