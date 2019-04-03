#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, time
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
		
		
