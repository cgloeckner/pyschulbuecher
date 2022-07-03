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

from db.orm import db, db_session
from db import orga, books, loans
from utils import errorhandler


__author__ = "Christian Glöckner"


@get('/loan/person/<id:int>')
@view('loan/person_listing')
def loan_person_overview(id):
    person = db.Person[id]
    loan = loans.orderLoanOverview(person.loan)
    request = loans.orderRequestOverview(person.request)
    return dict(person=person, loan=loan, request=request)


@get('/loan/person/<person_id:int>/add')
@view('loan/person_add')
def loan_person_add(person_id):
    return dict(id=person_id)


@post('/loan/person/<person_id:int>/add')
@errorhandler
def loan_person_add(person_id):
    person = db.Person[person_id]

    for b in db.Book.select():
        raw = request.forms.get(str(b.id), '')
        if raw.isnumeric():
            value = int(raw)
            if value > 0:
                loans.addLoan(person, b, value)

    db.commit()
    redirect('/loan/person/%d' % person_id)


@post('/loan/person/<person_id:int>/back')
@errorhandler
def loan_person_add(person_id):
    person = db.Person[person_id]

    for l in person.loan:
        if request.forms.get(str(l.book.id)) == 'on':
            loans.updateLoan(person, db.Book[l.book.id], 0)

    db.commit()
    redirect('/loan/person/%d' % person_id)


@get('/loan/ajax/books')
@view('loan/book_list')
def loan_ajax_queryBooks():
    classsets = request.query.classsets != "false"
    value = request.query.value
    if value != '':
        value = int(value)
    else:
        value = None

    person = db.Person[int(request.query.person_id)]
    if request.query.by == 'subject':
        subject = db.Subject[value] if value is not None else None
        bks = books.getRealBooksBySubject(subject, classsets)
    else:
        bks = books.getRealBooksByGrade(value, classsets)

    bks = books.orderBooksIndex(bks)
    return dict(person=person, bks=bks)


@get('/loan/book/<book_id:int>')
@view('loan/book_loan')
def loan_book_queryLoan(book_id):
    book = db.Book[book_id]
    l = loans.queryLoansByBook(book)

    return dict(book=book, loans=l)

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
    def test_loan_person_overview_request_unrequest_borrow_return(self):
        Tests.prepare()

        s = db.Student[3]

        # show person's loan overview without any
        ret = self.app.get('/loan/person/%d' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

        # request books
        loans.updateRequest(s, db.Book[3], True)
        loans.updateRequest(s, db.Book[5], True)

        # show person's loan overview (requests only)
        ret = self.app.get('/loan/person/%d' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

        # loan books
        loans.updateLoan(s.person, db.Book[2], True)
        loans.updateLoan(s.person, db.Book[1], True)
        loans.updateLoan(s.person, db.Book[4], True)

        # show person's loan overview (requests and loans)
        ret = self.app.get('/loan/person/%d' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

        # unregister requests
        loans.updateRequest(s, db.Book[3], False)
        loans.updateRequest(s, db.Book[5], False)

        # show person's loan overview (loans only)
        ret = self.app.get('/loan/person/%d' % (s.person.id))
        self.assertEqual(ret.status_int, 200)

        # return books
        loans.updateLoan(s.person, db.Book[2], False)
        loans.updateLoan(s.person, db.Book[1], False)
        loans.updateLoan(s.person, db.Book[4], False)

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
