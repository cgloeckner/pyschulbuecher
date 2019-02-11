#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, json
from datetime import datetime

from bottle import *
from pony import orm
from latex import build_pdf

from db.orm import db, db_session, Currency
from db import orga, books
from utils import errorhandler


__author__ = "Christian Glöckner"


@get('/admin/subjects')
@view('admin/subjects_index')
def subjects_index():
	return dict()

@post('/admin/subjects/add')
@errorhandler
@view('success')
def subjects_add_post():
	for line in request.forms.data.split('\n'):
		if len(line) > 0:
			tag, name = line.split('\t')
			db.Subject(name=name, tag=tag)
	return dict()

@get('/admin/subjects/edit/<id:int>')
@errorhandler
@view('admin/subjects_edit')
def subjects_edit_form(id):
	return dict(s=db.Subject[id])

@post('/admin/subjects/edit/<id:int>')
@errorhandler
@view('success')
def subjects_edit_post(id):
	s = db.Subject[id]
	s.tag = request.forms.tag
	s.name = request.forms.name
	return dict()

@post('/admin/subjects/delete/<id:int>')
@errorhandler
@view('success')
def subjects_delete(id):
	db.Subject[id].delete()
	return dict()

# -----------------------------------------------------------------------------

@get('/admin/publishers')
@view('admin/publishers_index')
def publishers_index():
	return dict()

@post('/admin/publishers/add')
@errorhandler
@view('success')
def publishers_add_post():
	for name in request.forms.data.split('\n'):
		if len(name) > 0:
			db.Publisher(name=name)
	return dict()

@get('/admin/publishers/edit/<id:int>')
@errorhandler
@view('admin/publishers_edit')
def publishers_edit_form(id):
	return dict(p=db.Publisher[id])

@post('/admin/publishers/edit/<id:int>')
@errorhandler
@view('success')
def publishers_edit_post(id):
	p = db.Publisher[id]
	p.name = request.forms.name
	return dict()

@post('/admin/publishers/delete/<id:int>')
@errorhandler
@view('success')
def publishers_delete(id):
	db.Publisher[id].delete()
	return dict()

# -----------------------------------------------------------------------------

@get('/admin/books')
@view('admin/books_index')
def books_index():
	return dict()

@post('/admin/books/add')
@errorhandler
@view('success')
def books_add_post():
	books.addBooks(request.forms.data)
	return dict()

@get('/admin/books/edit/<id:int>')
@errorhandler
@view('admin/books_edit')
def books_edit_form(id):
	return dict(b=db.Book[id])

@post('/admin/books/edit/<id:int>')
@errorhandler
@view('success')
def books_edit_post(id):
	b = db.Book[id]
	b.title   = request.forms.title
	b.isbn    = request.forms.isbn
	b.price   = Currency.fromString(request.forms.price)
	b.publisher = db.Publisher[int(request.forms.publisher_id)]
	b.stock     = int(request.forms.stock)
	b.inGrade   = int(request.forms.inGrade)
	b.outGrade  = int(request.forms.outGrade)
	b.subject   = db.Subject[int(request.forms.subject_id)] if request.forms.subject_id != "" else None
	b.novices   = True if request.forms.novices   == 'on' else False
	b.advanced  = True if request.forms.advnaced  == 'on' else False
	b.workbook  = True if request.forms.workbook  == 'on' else False
	b.classsets = True if request.forms.classsets == 'on' else False
	b.comment   = request.forms.comment
	return dict()

@post('/admin/books/delete/<id:int>')
@errorhandler
@view('success')
def books_delete(id):
	db.Book[id].delete()
	return dict()

# -----------------------------------------------------------------------------

def loadSettings():
	try:
		with open('settings.json') as h:
			return json.load(h)
	except FileNotFoundError:
		return {
			'year': 2019,
			'planner_price': 600,
			'deadline_changes': '19.06.2017',
			'deadline_booklist': '17.03.2017'
		}

@get('/admin/settings')
@view('admin/settings')
def settings_form():
	return dict(settings=loadSettings())

@post('/admin/settings')
@view('success')
def settings_form_post():
	settings = {
		'year'              : int(request.forms.year),
		'planner_price'     : Currency.fromString(request.forms.planner_price),
		'deadline_changes'  : request.forms.deadline_changes,
		'deadline_booklist' : request.forms.deadline_booklist
	}
	with open('settings.json', 'w') as h:
		json.dump(settings, h)
	return dict()

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
		self.settings = loadSettings()
	
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
		tex += template(self.planner, grade=grade, settings=self.settings)
		tex += template(self.footer)
		
		# export PDF
		fname = os.path.join('export', 'Bücherzettel%d%s.pdf' % (grade, suffix))
		pdf = build_pdf(tex)
		pdf.save_to(fname)


@get('/admin/booklist/download/<fname>')
def admin_booklist_download(fname):
	return static_file(fname, root='./export')

@get('/admin/booklist')
@view('admin/booklist_index')
def booklist_index():
	# fetch data
	data = list()
	for f in os.listdir('export'):
		grade = int(f.split('Bücherzettel')[1].split('_')[0].split('.pdf')[0])
		stat  = os.stat(os.path.join('export', f))
		data.append({
			"grade" : grade,
			"name"  : f,
			"new"   : '_Neuzugänge' in f,
			"size"  : stat.st_size,
			"date"  : datetime.utcfromtimestamp(int(stat.st_mtime)).strftime('%Y-%m-%d %H:%M:%S')
		})
	# sort by grade
	data.sort(key=lambda d: d["grade"])
	return dict(data=data)

@get('/admin/booklist/generate')
def booklist_generate():
	booklist = BooklistPdf()
	
	#for g in orga.getClassGrades():
	for g in [5, 6]:#, 7, 8, 9, 10, 11, 12]:
		booklist(g)
		if g > 5:
			booklist(g, new_students=True)
		yield '.'
	
	yield 'Abgeschlossen'

# -----------------------------------------------------------------------------


import unittest, webtest

class Tests(unittest.TestCase):

	@staticmethod
	@db_session
	def prepare():
		# create subjects
		db.Subject(name='Mathematics', tag='Ma')
		db.Subject(name='Russian',     tag='Ru')
		db.Subject(name='English',     tag='En')
		
		# create publishers
		db.Publisher(name='Cornelsen')
		db.Publisher(name='Klett')
		
		# create maths books
		db.Book(title='Maths I', isbn='000-001', price=2495,
			publisher=db.Publisher[1], inGrade=5, outGrade=6,
			subject=db.Subject[1])
		db.Book(title='Maths II', isbn='001-021', price=2999,
			publisher=db.Publisher[1], inGrade=7, outGrade=8,
			subject=db.Subject[1])
		db.Book(title='Maths III', isbn='914-721', price=3499,
			publisher=db.Publisher[1], inGrade=9, outGrade=10,
			subject=db.Subject[1])
		db.Book(title='Basic Maths', publisher=db.Publisher[1], inGrade=11,
			outGrade=12, subject=db.Subject[1], novices=True)
		db.Book(title='Advanced Maths', publisher=db.Publisher[1], inGrade=11,
			outGrade=12, subject=db.Subject[1], advanced=True)
		
		# create russian books
		db.Book(title='Privjet', isbn='49322-6346', price=5999,
			publisher=db.Publisher[2], inGrade=5, outGrade=10,
			subject=db.Subject[2])
		db.Book(title='Dialog', isbn='43623-8485', price=7999,
			publisher=db.Publisher[2], inGrade=11, outGrade=12,
			subject=db.Subject[2], novices=True, advanced=True)
		
		# create subject-independent books
		db.Book(title='Formulary', isbn='236-7634-62', price=2295,
			publisher=db.Publisher[1], inGrade=7, outGrade=12)
			
		# create english book
		db.Book(title='English 5th grade', publisher=db.Publisher[2],
			inGrade=5, outGrade=5, subject=db.Subject[3])

	
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
	
	@db_session
	def test_subjects_add_invalid(self):
		Tests.prepare()
	
		# add subjects (Ma-tag already used)
		args = {
			"data": "Fr\tFranzösisch\nMa\tMathematik\nDe\tDeutsch"
		}
		ret = self.app.post('/admin/subjects/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show subjects list
		ret = self.app.get('/admin/subjects')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_subjects_add_ignore_empty_lines(self):
		Tests.prepare()
	
		# add subjects
		args = { "data": "Fr\tFranzösisch\n\nDe\tDeutsch\n" }
		ret = self.app.post('/admin/subjects/add', args)
		self.assertEqual(ret.status_int, 200)
		
		# show subjects gui
		ret = self.app.get('/admin/subjects')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_subjects_edit_gui(self):
		Tests.prepare()
		
		# show valid subject's edit gui
		ret = self.app.get('/admin/subjects/edit/1')
		self.assertEqual(ret.status_int, 200)
		
		# show invalid subject's edit gui
		ret = self.app.get('/admin/subjects/edit/1337', expect_errors=True)
		self.assertEqual(ret.status_int, 400)
	
	@db_session
	def test_subjects_edit_post(self):
		Tests.prepare()
		
		# edit subject
		args = { 'tag' : 'Sk', 'name': 'Sozialkunde' }
		ret = self.app.post('/admin/subjects/edit/1', args)
		self.assertEqual(ret.status_int, 200)
		
		# show subjects gui
		ret = self.app.get('/admin/subjects')
		self.assertEqual(ret.status_int, 200)

	@db_session
	def test_subjects_edit_invalid_post(self):
		Tests.prepare()
		
		# edit subject (tag is used by #1)
		args = { 'tag' : 'Ma', 'name': 'Sozialkunde' }
		ret = self.app.post('/admin/subjects/edit/2', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show subjects gui
		ret = self.app.get('/admin/subjects')
		self.assertEqual(ret.status_int, 200)
		
		# edit subject (invalid target id)
		args = { 'tag' : 'Sk', 'name': 'Sozialkunde' }
		ret = self.app.post('/admin/subjects/edit/1337', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show subjects gui (once again)
		ret = self.app.get('/admin/subjects')
		self.assertEqual(ret.status_int, 200)

	@db_session
	def test_subjects_delete(self):
		Tests.prepare()
		
		# delete subject
		ret = self.app.post('/admin/subjects/delete/1')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_subjects_delete_invalid(self):
		Tests.prepare()
		
		# delete subject
		ret = self.app.post('/admin/subjects/delete/1337', expect_errors=True)
		self.assertEqual(ret.status_int, 400)

	# -------------------------------------------------------------------------
	
	@db_session
	def test_publishers_gui(self):
		Tests.prepare()
		
		# show publishers gui
		ret = self.app.get('/admin/publishers')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_publishers_add_new(self):
		Tests.prepare()
	
		# add subjects
		args = {
			"data": "C. C. Buchner\nWestermann"
		}
		ret = self.app.post('/admin/publishers/add', args)
		self.assertEqual(ret.status_int, 200)
		
		# show subjects list
		ret = self.app.get('/admin/publishers')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_publishers_add_invalid(self):
		Tests.prepare()
	
		# add subjects (2nd already used)
		args = {
			"data": "C. C. Buchner\nKlett\nWestermann"
		}
		ret = self.app.post('/admin/publishers/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show publishers list
		ret = self.app.get('/admin/publishers')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_publishers_add_ignore_empty_lines(self):
		Tests.prepare()
	
		# add subjects
		args = { "data": "C. C. Buchner\n\nWestermann\n" }
		ret = self.app.post('/admin/publishers/add', args)
		self.assertEqual(ret.status_int, 200)
		
		# show subjects gui
		ret = self.app.get('/admin/publishers')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_publishers_edit_gui(self):
		Tests.prepare()
		
		# show valid publisher's edit gui
		ret = self.app.get('/admin/publishers/edit/1')
		self.assertEqual(ret.status_int, 200)
		
		# show invalid publisher's edit gui
		ret = self.app.get('/admin/publishers/edit/1337', expect_errors=True)
		self.assertEqual(ret.status_int, 400)
	
	@db_session
	def test_publishers_edit_post(self):
		Tests.prepare()
		
		# edit subject
		args = { 'name': 'Volk und Wissen' }
		ret = self.app.post('/admin/publishers/edit/1', args)
		self.assertEqual(ret.status_int, 200)
		
		# show publishers gui
		ret = self.app.get('/admin/publishers')
		self.assertEqual(ret.status_int, 200)

	@db_session
	def test_publishers_edit_invalid_post(self):
		Tests.prepare()
		
		# edit publisher (name is used by #1)
		args = { 'name': 'Cornelsen' }
		ret = self.app.post('/admin/publishers/edit/2', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show publishers gui
		ret = self.app.get('/admin/publishers')
		self.assertEqual(ret.status_int, 200)
		
		# edit publisher (invalid target id)
		args = { 'name' : 'Volk und Wissen' }
		ret = self.app.post('/admin/publishers/edit/1337', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show publishers gui (once again)
		ret = self.app.get('/admin/publishers')
		self.assertEqual(ret.status_int, 200)

	@db_session
	def test_publishers_delete(self):
		Tests.prepare()
		
		p = db.Publisher(name='dummy to delete')
		db.flush()
		
		# delete publisher
		ret = self.app.post('/admin/publishers/delete/{0}'.format(p.id))
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_publishers_delete_invalid(self):
		Tests.prepare()
		
		# delete publisher
		ret = self.app.post('/admin/publishers/delete/1337', expect_errors=True)
		self.assertEqual(ret.status_int, 400)

	# -------------------------------------------------------------------------
	
	@db_session
	def test_books_gui(self):
		Tests.prepare()
		
		# show books gui
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_books_add_new(self):
		Tests.prepare()
	
		# add books
		args = { "data": """Titel\t0815-000\t1234\tKlett\t39\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\t
Titel2\t0815-001\t1234\tKlett\t39\t10\t12\tEn\tTrue\tFalse\tFalse\tFalse\t
Titel3\t0815-002\t1234\tKlett\t39\t10\t12\tRu\tTrue\tFalse\tFalse\tFalse\t"""
		}
		ret = self.app.post('/admin/books/add', args)
		self.assertEqual(ret.status_int, 200)
		
		# show books list
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_books_add_ignore_newlines(self):
		Tests.prepare()
	
		# add books
		args = { "data": """Titel\t0815-000\t1234\tKlett\t39\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\t


Titel2\t0815-001\t1234\tKlett\t39\t10\t12\tEn\tTrue\tFalse\tFalse\tFalse\t

Titel3\t0815-002\t1234\tKlett\t39\t10\t12\tRu\tTrue\tFalse\tFalse\tFalse\t
"""
		}
		ret = self.app.post('/admin/books/add', args)
		self.assertEqual(ret.status_int, 200)
		
		# show books list
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_books_add_minimal_data(self):
		Tests.prepare()
	
		# add book (invalid publisher)
		args = { "data": "Titel\t\t\tKlett\t39\t10\t12" }
		ret = self.app.post('/admin/books/add', args)
		self.assertEqual(ret.status_int, 200)
		
		# show books list
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_books_add_invalid_data(self):
		Tests.prepare()
	
		# add book (invalid publisher)
		args = { "data": "Titel\t0815-000\t1234\tUnbekannt\t39\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\t" }
		ret = self.app.post('/admin/books/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show books list
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
		# add book (invalid subject)
		args = { "data": "Titel\t0815-000\t1234\tKlett\t39\t10\t12\tFoo\tTrue\tFalse\tFalse\tFalse\t" }
		ret = self.app.post('/admin/books/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# add book (invalid price)
		args = { "data": "Titel\t0815-000\tabc\tKlett\t39\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\t" }
		ret = self.app.post('/admin/books/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# add books (invalid inGrade)
		args = { "data": "Titel\t0815-000\t1234\tKlett\t39\tZehn\t12\tMa\tTrue\tFalse\tFalse\tFalse\t" }
		ret = self.app.post('/admin/books/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# add books (invalid outGrade)
		args = { "data": "Titel\t0815-000\t1234\tKlett\t39\t10\tAbi\tMa\tTrue\tFalse\tFalse\tFalse\t" }
		ret = self.app.post('/admin/books/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show books list (again)
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_books_edit_gui(self):
		Tests.prepare()
		
		# show valid book's edit gui
		ret = self.app.get('/admin/books/edit/1')
		self.assertEqual(ret.status_int, 200)
		
		# show invalid book's edit gui
		ret = self.app.get('/admin/books/edit/1337', expect_errors=True)
		self.assertEqual(ret.status_int, 400)
	
	@db_session
	def test_books_edit_post(self):
		Tests.prepare()
		
		# edit book
		args = {
			"title"        : "Biologie Hautnah",
			"isbn"         : "0815-346465-7-346",
			"price"        : "1234",
			"publisher_id" : "1",
			"stock"        : "39",
			"inGrade"      : "10",
			"outGrade"     : "12",
			"subject_id"   : "2",
			"novices"      : "on",
			"advanced"     : "off", # @NOTE: empty str?
			"workbook"     : "off", # @NOTE: empty str?
			"classsets"    : "off",
			"comment"      : ""
		}
		ret = self.app.post('/admin/books/edit/1', args)
		self.assertEqual(ret.status_int, 200)
		
		# show books gui
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)

	@db_session
	def test_books_edit_invalid_post(self):
		Tests.prepare()
		
		# edit book (invalid publisher, invalid subject)
		args = {
			"title"        : "Biologie Hautnah",
			"isbn"         : "0815-346465-7-346",
			"price"        : "1234",
			"publisher_id" : "1337",
			"stock"        : "39",
			"inGrade"      : "10",
			"outGrade"     : "12",
			"subject_id"   : "2346345",
			"novices"      : "on",
			"advanced"     : "off", # @NOTE: empty str?
			"workbook"     : "off", # @NOTE: empty str?
			"classsets"    : "off",
			"comment"      : ""
		}
		ret = self.app.post('/admin/books/edit/2', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show books gui
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
		
		# edit book (invalid target id)
		args = {
			"title"        : "Biologie Hautnah",
			"isbn"         : "0815-346465-7-346",
			"price"        : "1234",
			"publisher_id" : "1",
			"stock"        : "39",
			"inGrade"      : "10",
			"outGrade"     : "12",
			"subject_id"   : "2",
			"novices"      : "on",
			"advanced"     : "off", # @NOTE: empty str?
			"workbook"     : "off", # @NOTE: empty str?
			"classsets"    : "off",
			"comment"      : ""
		}
		ret = self.app.post('/admin/books/edit/1337', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show books gui (once again)
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)

	@db_session
	def test_books_delete(self):
		Tests.prepare()
		
		# delete book
		ret = self.app.post('/admin/books/delete/1')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_books_delete_invalid(self):
		Tests.prepare()
		
		# delete book
		ret = self.app.post('/admin/books/delete/1337', expect_errors=True)
		self.assertEqual(ret.status_int, 400)


