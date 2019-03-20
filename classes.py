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


@get('/classes/<grade:int>')
@view('classes/grade_index')
def classes_grade_index(grade):
	return dict(grade=grade)

@get('/classes/<grade:int>/<tag>')
@view('classes/students_index')
def classes_students_index(grade, tag):
	bks = books.getBooksStartedIn(grade)
	bks = books.orderBooksList(bks)
	return dict(grade=grade, tag=tag, books=bks)

# -----------------------------------------------------------------------------

@get('/classes/requests/<grade:int>/<tag>')
@view('classes/request_form')
def classes_requests_form(grade, tag):
	bks = books.getBooksStartedIn(grade+1, True)
	bks = books.orderBooksList(bks)
	return dict(grade=grade, tag=tag, books=bks)

@post('/classes/requests/<grade:int>/<tag>')
@errorhandler
def classes_requests_post(grade, tag):
	bks = books.getBooksStartedIn(grade+1, True)
	for s in orga.getStudentsIn(grade, tag):
		for b in bks:
			key    = "%d_%d" % (s.id, b.id)
			status = request.forms.get(key) == 'on'
			loans.updateRequest(s, b, status)
	
	db.commit()
	redirect('/classes/%d/%s' % (grade, tag))

# -----------------------------------------------------------------------------

@post('/classes/loans/<grade:int>/<tag>')
@errorhandler
def classes_loans_post(grade, tag):
	bks = books.getBooksStartedIn(grade, True)
	for s in orga.getStudentsIn(grade, tag):
		for b in bks:
			key   = "%d_%d" % (s.id, b.id)
			count = request.forms.get(key)
			if count is None or count is "":
				count = 0
			else:
				count = int(count)
			loans.updateLoan(s.person, b, count)
	
	db.commit()
	redirect('/classes/%d/%s' % (grade, tag))

# -----------------------------------------------------------------------------

"""

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
		self.assertEqual(ret.status_int, 200)
		
		# show subjects list
		ret = self.app.get('/admin/subjects')
		self.assertEqual(ret.status_int, 200)
"""
