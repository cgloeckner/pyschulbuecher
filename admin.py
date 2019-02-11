#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

@get('/admin/booklist/generate')
def booklist_generate():
	with open('docs/header.tpl') as f:
		header = f.read()
	
	with open('docs/footer.tpl') as f:
		footer = f.read()

	with open('docs/book_select.tpl') as f:
		book_select = f.read()
	
	#for g in orga.getClassGrades():
	for g in [11]:#, 6, 7, 8, 9, 10, 11, 12]:
		bs=list(books.getBooksStartedIn(g).order_by(db.Book.title).order_by(db.Book.subject))
		
		tex =  header
		tex += template(book_select, grade=g, bs=bs, workbook=False)
		tex += template(book_select, grade=g, bs=bs, workbook=True)
		tex += footer
		with open('/tmp/test.tex', 'w') as h:
			h.write(tex)
		
		pdf = build_pdf(tex)
		pdf.save_to('export/Bücherzettel{0}.pdf'.format(g))

		print('PDF rendered')	

	return "erledigt"

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
	
		# add subjects
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

