#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, json
import PyPDF2

from bottle import template
from latex import build_pdf

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
	def __init__(self, settings_handle, export='export'):
		# load LaTeX templates
		with open('docs/header.tpl') as f:
			self.header = f.read()
		with open('docs/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/info.tpl') as f:
			self.info = f.read()
		with open('docs/select.tpl') as f:
			self.select = f.read()
		with open('docs/empty.tpl') as f:
			self.empty = f.read()
		with open('docs/planner.tpl') as f:
			self.planner = f.read()
		# prepare output directory
		self.export = export
		self.texdir = os.path.join(export, 'tex')
		if not os.path.isdir(self.export):
			os.mkdir(self.export)
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		# merged pdf
		self.merger = PyPDF2.PdfFileMerger()
	
	def __call__(self, grade: int, new_students: bool=False):
		"""Generate booklist pdf file for the given grade. A separate booklist
		can be generated for new_students, which include additional books other
		students already have from earlier classes.
		"""
		# fetch and order books
		if new_students:
			bks    = books.getBooksUsedIn(grade, booklist=True)
			suffix = '_Neuzugänge'
		else:
			bks    = books.getBooksStartedIn(grade, booklist=True)
			suffix = ''
		bks = books.orderBooksList(bks)
		
		# determine number of books
		num_books  = sum(1 for b in bks if not b.workbook)
		
		# render templates
		tex  = template(self.header, s=self.s, grade=grade, new_students=new_students)
		tex += template(self.info, grade=grade, new_students=new_students, s=self.s)
		if num_books > 0:
			tex += template(self.select, grade=grade, bs=bks, workbook=False)
		else:
			tex += template(self.empty, workbook=False)
		if num_books < len(bks):
			tex += template(self.select, grade=grade, bs=bks, workbook=True)
		else:
			tex += template(self.empty, workbook=True)
		tex += template(self.planner, grade=grade, s=self.s)
		tex += template(self.footer)
		
		# export tex (debug purpose)
		dbg_fname = os.path.join(self.texdir, '%d%s.tex' % (grade, suffix))
		with open(dbg_fname, 'w') as h:
			h.write(tex)
		
		# export PDF
		fname = os.path.join(self.export, 'Bücherzettel%d%s.pdf' % (grade, suffix))
		pdf = build_pdf(tex)
		pdf.save_to(fname)
		
		# add to merge-PDF
		self.merger.append(fname)

	def merge(self):
		# save merge-PDF
		fname = os.path.join(self.export, 'BücherzettelKomplett.pdf')
		
		with open(fname, 'wb') as h:
			self.merger.write(h)

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

	@db_session
	def test_create_custom_booklist(self):
		# create custom database content (real work example)
		books.addSubjects("Mathematik	Ma\nDeutsch	De\nEnglisch	En\nPhysik	Ph")
		books.addPublishers("Klett\nCornelsen")
		books.addBooks("""Ein Mathe-Buch	978-3-7661-5000-4	32,80 €	Cornelsen	5	12	Ma	True	True	False	False	True
Mathe AH	978-3-7661-5007-3	8,80 €	Cornelsen	5	12	Ma	True	True	True	False	True
Deutsch-Buch mit sehr langam Titel und damit einigen Zeilenumbrüchen .. ach und Umlaute in größeren Mengen öÖäÄüÜß sowie Sonderzeichen !"§$%&/()=?.:,;-_@	978-3-12-104104-6	35,95 €	Klett	11	12	De	True	True	False	False	True
Old English Book			Klett	5	12	En	True	True	False	True	False
Grundlagen der Physik			Cornelsen	5	12	Ph	True	True	False	False	True
Tafelwerk	978-3-06-001611-2	13,50 €	Cornelsen	7	12		False	False	False	False	True""")

		# create booklist
		with open('settings.json') as h:
			booklist = BooklistPdf(h, export='/tmp/export')
		booklist(11, new_students=True)
		print('PLEASE MANUALLY VIEW /tmp/export/Buecherzettel11.pdf')



