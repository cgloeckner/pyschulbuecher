#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, time
from datetime import datetime

from bottle import *
from pony import orm

from db.orm import db, db_session, Currency
from db import orga, books
from utils import errorhandler


__author__ = "Christian Glöckner"


@get('/classes/<grade:int>')
@view('classes/grade_index')
def classes_grade_index(grade):
	return dict(grade=grade)

@get('/classes/<grade:int>/<tag>')
@view('classes/students_index')
def classes_students_index(grade, tag):
	return dict(grade=grade, tag=tag)


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
