#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, json

from db import books


class Settings(object):

	def __init__(self):
		self.school_year       = 2019
		self.planner_price     = 600
		self.deadline_booklist = '17.03.2017'
		self.deadline_changes  = '19.06.2017'

	def load_from(self, fhandle):
		tmp = json.load(fhandle)
		
		self.school_year       = tmp['school_year']
		self.planner_price     = tmp['planner_price']
		self.deadline_booklist = tmp['deadline_booklist']
		self.deadline_changes  = tmp['deadline_changes']
	
	def save_to(self, fhandle):
		tmp = {
			'school_year'        : self.school_year,
			'planner_price'      : self.planner_price,
			'deadline_booklist'  : self.deadline_booklist,
			'deadline_changes'   : self.deadline_changes
		}
	
		json.dump(tmp, fhandle)

# -----------------------------------------------------------------------------

class BooklistPdf(object):
	def __init__(self):
		# load LaTeX templates
		with open('docs/header.tpl') as f:
			self.header = f.read()
		with open('docs/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/info.tpl') as f:
			self.info = f.read()
		with open('docs/select.tpl') as f:
			self.select = f.read()
		with open('docs/planner.tpl') as f:
			self.planner = f.read()
		# prepare output directory
		if not os.path.isdir('export'):
			os.mkdir('export')
		# load settings
		self.s = Settings()
		self.s.load_from()
	
	def __call__(self, grade: int, new_students: bool=False):
		"""Generate booklist pdf file for the given grade. A separate booklist
		can be generated for new_students, which include additional books other
		students already have from earlier classes.
		"""
		# fetch and order books
		if new_students:
			bks    = books.getBooksUsedIn(grade)
			suffix = '_Neuzugänge'
		else:
			bks    = books.getBooksStartedIn(grade)
			suffix = ''
		bks = list(bks.order_by(db.Book.title).order_by(db.Book.subject))
		
		# render templates
		tex  = template(self.header)
		tex += template(self.info, grade=grade, new_students=new_students,
			settings=self.settings)
		tex += template(self.select, grade=grade, bs=bks, workbook=False)
		tex += template(self.select, grade=grade, bs=bks, workbook=True)
		tex += template(self.planner, grade=grade, s=self.s)
		tex += template(self.footer)
		
		# export PDF
		fname = os.path.join('export', 'Bücherzettel%d%s.pdf' % (grade, suffix))
		pdf = build_pdf(tex)
		pdf.save_to(fname)

# -----------------------------------------------------------------------------


import unittest
from io import StringIO

from pony.orm import *

from db.orm import db

class Tests(unittest.TestCase):

	@staticmethod
	@db_session
	def prepare():
		import db.orga, db.books, db.orga
		
		db.orga.Tests.prepare()
		db.books.Tests.prepare()

	def setUp(self):
		db.create_tables()
		
	def tearDown(self):
		db.drop_all_tables(with_all_data=True)

	@db_session
	def test_settings_save(self):
		s = Settings()
		s.school_year       = 1
		s.planner_price     = 2
		s.deadline_booklist = '3'
		s.deadline_changes  = '4'
		
		io = StringIO()
		s.save_to(io)
		
		self.assertEqual(io.getvalue(), '{"school_year": 1, "planner_price": 2, "deadline_booklist": "3", "deadline_changes": "4"}')
	
	@db_session
	def test_settings_load(self):
		io = StringIO()
		io.write('{"school_year": 1, "planner_price": 2, "deadline_booklist": "3", "deadline_changes": "4"}')
		io.seek(0)
		
		s = Settings()
		s.load_from(io)
		
		self.assertEqual(s.school_year      , 1)
		self.assertEqual(s.planner_price    , 2)
		self.assertEqual(s.deadline_booklist, '3')
		self.assertEqual(s.deadline_changes , '4')


