#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, time, json
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
	person  = db.Person[id]
	loan    = loans.orderLoanOverview(person.loan)
	request = loans.orderRequestOverview(person.request)
	return dict(person=person, loan=loan, request=request)


@get('/loan/person/<person_id:int>/add')
@view('loan/person_add')
def loan_person_add(person_id):
	bks = books.getPureBooksByGradeAndSubject(None, None)
	return dict(id=person_id, bks=bks)


@post('/loan/person/<person_id:int>/add')
@errorhandler
def loan_person_add(person_id):
	person = db.Person[person_id]
	book   = db.Book[int(request.forms.book_id)]
	count  = int(request.forms.count)
	
	loans.updateLoan(person, book, count)
	
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
@get('/loan/ajax/books/grade/<grade:int>')
@get('/loan/ajax/books/subject/<subject_id:int>')
@get('/loan/ajax/books/grade/<grade:int>/subject/<subject_id:int>')
def loan_ajax_queryBooks(grade=None, subject_id=None):
	subject = db.Subject[subject_id] if subject_id is not None else None
	bks = books.getPureBooksByGradeAndSubject(grade, subject)
	
	# copy relevant data
	data = dict()
	for b in bks:
		data[b.id] = b.toString()

	return json.dumps(data)


@get('/loan/ajax/count/<person_id:int>/<book_id:int>')
def loan_ajax_queryBookCount(person_id, book_id):
	person = db.Person[person_id]
	book   = db.Book[book_id]
	
	return str(loans.getLoanCount(person, book))


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
	def test_loan_person_overview(self):
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
		
		
