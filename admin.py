#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, time, math
from datetime import datetime

from bottle import *
from pony import orm

from db.orm import db, db_session, Currency
from db import orga, books, loans
from db.utils import Settings, BooklistPdf, RequestlistPdf, BookreturnPdf, BookloanPdf
from utils import errorhandler


__author__ = "Christian Glöckner"



# this global variable is changed during unit testing
demand_json = 'demand.json'


@get('/admin/subjects')
@view('admin/subjects_index')
def subjects_index():
	return dict()

@post('/admin/subjects/add')
@errorhandler
def subjects_add_post():
	for line in request.forms.data.split('\n'):
		if len(line) > 0:
			tag, name = line.split('\t')
			db.Subject(name=name, tag=tag)
	
	db.commit()
	redirect('/admin/subjects')

@get('/admin/subjects/edit/<id:int>')
@errorhandler
@view('admin/subjects_edit')
def subjects_edit_form(id):
	return dict(s=db.Subject[id])

@post('/admin/subjects/edit/<id:int>')
@errorhandler
def subjects_edit_post(id):
	s = db.Subject[id]
	s.tag = request.forms.tag
	s.name = request.forms.name
	s.elective = request.forms.elective == 'on'
	
	db.commit()
	redirect('/admin/subjects')

@post('/admin/subjects/delete/<id:int>')
@errorhandler
def subjects_delete(id):
	db.Subject[id].delete()
	
	db.commit()
	redirect('/admin/subjects')

# -----------------------------------------------------------------------------

@get('/admin/publishers')
@view('admin/publishers_index')
def publishers_index():
	return dict()

@post('/admin/publishers/add')
@errorhandler
def publishers_add_post():
	for name in request.forms.data.split('\n'):
		if len(name) > 0:
			db.Publisher(name=name)

	db.commit()
	redirect('/admin/publishers')

@get('/admin/publishers/edit/<id:int>')
@errorhandler
@view('admin/publishers_edit')
def publishers_edit_form(id):
	return dict(p=db.Publisher[id])

@post('/admin/publishers/edit/<id:int>')
@errorhandler
def publishers_edit_post(id):
	p = db.Publisher[id]
	p.name = request.forms.name
	
	db.commit()
	redirect('/admin/publishers')

@post('/admin/publishers/delete/<id:int>')
@errorhandler
def publishers_delete(id):
	db.Publisher[id].delete()
	
	db.commit()
	redirect('/admin/publishers')

# -----------------------------------------------------------------------------

@get('/admin/books')
@view('admin/books_index')
def books_index():
	return dict()

@post('/admin/books/add')
@errorhandler
def books_add_post():
	books.addBooks(request.forms.data)
	
	db.commit()
	redirect('/admin/books')

@get('/admin/books/edit/<id:int>')
@errorhandler
@view('admin/books_edit')
def books_edit_form(id):
	return dict(b=db.Book[id])

@post('/admin/books/edit/<id:int>')
@errorhandler
def books_edit_post(id):
	b = db.Book[id]
	b.title   = request.forms.title
	b.isbn    = request.forms.isbn
	b.price   = Currency.fromString(request.forms.price) if request.forms.price is not '' else 0
	b.publisher = db.Publisher[int(request.forms.publisher_id)]
	b.stock     = int(request.forms.stock)
	b.inGrade   = int(request.forms.inGrade)
	b.outGrade  = int(request.forms.outGrade)
	b.subject   = db.Subject[int(request.forms.subject_id)] if request.forms.subject_id != "" else None
	b.novices   = True if request.forms.novices   == 'on' else False
	b.advanced  = True if request.forms.advanced  == 'on' else False
	b.workbook  = True if request.forms.workbook  == 'on' else False
	b.classsets = True if request.forms.classsets == 'on' else False
	b.for_loan  = True if request.forms.for_loan  == 'on' else False
	b.comment   = request.forms.comment
	
	db.commit()
	redirect('/admin/books')

@post('/admin/books/delete/<id:int>')
@errorhandler
def books_delete(id):
	db.Book[id].delete()
	
	db.commit()
	redirect('/admin/books')

@get('/admin/demand')
@view('admin/demand_form')
def demand_form():
	s = Settings()
	try:
		with open('settings.ini') as h:
			s.load_from(h)
	except FileNotFoundError:
		# keep default values
		pass

	# load student numbers from file
	demand = loans.DemandManager()
	with open(demand_json, 'r') as h:
		demand.load_from(h)
	
	return dict(s=s, demand=demand)

@post('/admin/demand')
@view('admin/demand_report')
def demand_report():
	s = Settings()
	try:
		with open('settings.ini') as h:
			s.load_from(h)
	except FileNotFoundError:
		# keep default values
		pass
	
	# percentage of lowering the actual stock to gain buffer
	lowering = int(request.forms.lowering)

	# fetch demand from UI input
	demand = loans.DemandManager()
	demand.parse(request.forms.get)
	
	# save total student numbers
	print(demand_json)
	with open(demand_json, 'w') as h:
		demand.save_to(h)

	# create book demand report
	bks = books.orderBooksList(books.getAllBooks())
	total = 0
	data = dict()
	for b in bks:
		free = demand.getNeededBooks(b)
		required = demand.getMaxDemand(b)
		required = max(required, free) # to fix problems with more books marked as free
		
		lower_stock = math.floor(b.stock * (100.0 - lowering) / 100.0)
		
		# number of acquire books (to fulfill free books)
		acquire = free - lower_stock
		if acquire < 0:
			acquire = 0
		
		# number of left over books
		left = lower_stock - free
		if left < 0:
			left = '0(!)'
		
		# total number of parents (gap between number of free and total required)
		parents = required - free
		if parents < 0:
			parents = 0
			
		if b.classsets:
			# no books by parents if classsets
			parents = 0
		
		# total number of pending free books (acquisition by school)
		school = acquire - parents
		
		# total price
		if school > 0:
			price = b.price * school
		else:
			price = 0
			school = "&mdash;"
		
		data[b.id] = {
			'acquire': acquire,
			'free': free,
			'required': required,
			'left': left,
			'parents': parents,
			'school': school,
			'price': price,
			'stock': lower_stock
		}
		total += price
	
	return dict(bks=bks, data=data, total=total, s=s)

# -----------------------------------------------------------------------------

@get('/admin/classes')
@view('admin/classes_index')
def classes_index():
	return dict()

@post('/admin/classes/add')
@errorhandler
def classes_add_post():
	orga.addClasses(request.forms.data)
	
	db.commit()
	redirect('/admin/classes')

@get('/admin/classes/edit/<id:int>')
@view('admin/classes_edit')
def classes_edit(id):
	return dict(c=db.Class[id])

@post('/admin/classes/edit/<id:int>')
@errorhandler
def classes_edit_post(id):
	orga.updateClass(id, int(request.forms.grade), request.forms.tag,
		int(request.forms.teacher_id))
	
	db.commit()
	redirect('/admin/classes')

@get('/admin/classes/move/<id:int>')
@view('admin/classes_move')
def classes_edit(id):
	return dict(c=db.Class[id])

@post('/admin/classes/move/<id:int>')
@errorhandler
def classes_move_post(id):
	# fetch target class
	new_id = int(request.forms.class_id)
	new_class = db.Class[new_id]
	
	# move students to new class
	students = list()
	for s in db.Class[id].student:
		# note that form names are always strings
		key = str(s.id)
		if request.forms.get(key) == 'on':
			s.class_ = new_class
	
	db.commit()
	redirect('/admin/classes/move/%d' % new_id)

@post('/admin/classes/delete/<id:int>')
@errorhandler
def classes_delete_post(id):
	db.Class[id].delete()
	
	db.commit()
	redirect('/admin/classes')

# -----------------------------------------------------------------------------

@get('/admin/students')
@view('admin/students_index')
def students_index():
	return dict()

@post('/admin/students/add')
@errorhandler
def students_add_post():
	orga.addStudents(request.forms.data)
	
	db.commit()
	redirect('/admin/students')

@post('/admin/students/search')
@errorhandler
@view('admin/students_search')
def students_search_post():
	data = orga.getStudentsLike(request.forms.name, request.forms.firstname)
	return dict(data=data)

@get('/admin/students/edit/<id:int>')
@view('admin/students_edit')
def students_edit(id):
	return dict(s=db.Student[id])

@post('/admin/students/edit/<id:int>')
@errorhandler
def students_edit_post(id):
	s = db.Student[id]
	s.person.name = request.forms.name
	s.person.firstname = request.forms.firstname
	s.class_ = db.Class[request.forms.class_id]
	
	db.commit()
	redirect('/admin/students')

@post('/admin/students/delete/<id:int>')
@errorhandler
def students_delete_post(id):
	db.Student[id].delete()	
	
	db.commit()
	redirect('/admin/students')

# -----------------------------------------------------------------------------

@get('/admin/teachers')
@view('admin/teachers_index')
def teachers_index():
	return dict()

@post('/admin/teachers/add')
@errorhandler
def teachers_add_post():
	orga.addTeachers(request.forms.data)
	
	db.commit()
	redirect('/admin/teachers')

@get('/admin/teachers/edit/<id:int>')
@view('admin/teachers_edit')
def students_edit(id):
	return dict(t=db.Teacher[id])

@post('/admin/teachers/edit/<id:int>')
@errorhandler
def teachers_edit_post(id):
	s = db.Teacher[id]
	s.person.name = request.forms.name
	s.person.firstname = request.forms.firstname
	s.tag = request.forms.tag.lower()
	
	db.commit()
	redirect('/admin/teachers')

@post('/admin/teachers/delete/<id:int>')
@errorhandler
def teachers_delete_post(id):
	db.Teacher[id].delete()	
	
	db.commit()
	redirect('/admin/teachers')

# -----------------------------------------------------------------------------

@get('/admin/settings')
@view('admin/settings')
def settings_form():
	s = Settings()
	try:
		with open('settings.ini') as h:
			s.load_from(h)
	except FileNotFoundError:
		# keep default values
		pass
	
	return dict(s=s)

@post('/admin/settings')
def settings_form_post():
	s = Settings()
	s.data['general']['school_year']         = request.forms.school_year
	s.data['general']['planner_price']       = str(Currency.fromString(request.forms.planner_price))
	s.data['deadline']['booklist_changes']   = request.forms.deadline_booklist_changes
	s.data['deadline']['booklist_return']    = request.forms.deadline_booklist_return
	s.data['deadline']['bookreturn_noexam'] = request.forms.deadline_bookreturn_noexam
	
	with open('settings.ini', 'w') as h:
		s.save_to(h)
	
	db.commit()
	redirect('/admin/settings')

# -----------------------------------------------------------------------------

@get('/admin/lists/download/<fname>')
def admin_lists_download(fname):
	"""Note that this callback is NOT covered by the test suite.
	"""
	return static_file(fname, root='./export')

@get('/admin/lists')
@view('admin/lists_index')
def lists_index():
	# fetch data
	data = list()
	full = False
	for fname in os.listdir('export'):
		if not fname.endswith('.pdf'):
			# ignore everything else (including tex/ subdir)
			continue
		else:
			stat  = os.stat(os.path.join('export', fname))
			data.append({
				"name"  : fname,
				"title" : fname.split('.pdf')[0],
				"size"  : stat.st_size,
				"date"  : datetime.utcfromtimestamp(int(stat.st_mtime)).strftime('%Y-%m-%d %H:%M:%S')
			})
	# sort by name
	data.sort(key=lambda d: d["name"])
	return dict(data=data, full=full)

@get('/admin/lists/generate/booklist')
def booklist_generate():
	with open('settings.ini') as h:
		booklist = BooklistPdf(h)
	
	print('Generating Booklists')
	d = time.time()
	yield 'Bitte warten...'
	#for g in orga.getClassGrades():
	for g in range(5, 12+1):
		yield '<br>Klasse %d' % g
		booklist(g)
		if g > 5:
			yield ' und Neuzugänge'
			booklist(g, new_students=True)
	
	# merging booklists
	booklist.merge()
	
	print('Done')
	d = time.time() - d
	
	yield '<hr /><br />Erledigt in %f Sekunden' % (d)

@get('/admin/lists/generate/requestlist')
def requestlist_generate():
	with open('settings.ini') as h:
		requestlist = RequestlistPdf(h)
	
	# exclude 12th grade (last grade)
	for grade in range(5, 11+1):
		for c in orga.getClassesByGrade(grade):
			requestlist(c)
	requestlist.saveToFile()

	return 'Fertig'

@get('/admin/lists/generate/bookreturn')
def bookreturn_generate():
	with open('settings.ini') as h:
		bookreturn = BookreturnPdf(h)
	
	# generate overview lists for all grades
	for grade in range(5, 12+1):
		bookreturn.addOverview(grade)
	
	# generate return lists for all grades
	for grade in range(5, 12+1):
		for c in orga.getClassesByGrade(grade):
			bookreturn(c)
	bookreturn.saveToFile()

	return 'Fertig'

@get('/admin/lists/generate/bookloan')
def bookreturn_generate():
	with open('settings.ini') as h:
		bookreturn = BookloanPdf(h)
	
	# generate return lists for all new grades (for next year)
	for grade in range(4, 11+1):
		for c in orga.getClassesByGrade(grade):
			bookreturn(c)
	bookreturn.saveToFile()

	return 'Fertig'

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
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
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
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
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
		args = { 'tag' : 'Sk', 'name': 'Sozialkunde', 'elective': 'on' }
		ret = self.app.post('/admin/subjects/edit/1', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		sj = db.Subject[1]
		self.assertEqual(sj.tag,  args['tag'])
		self.assertEqual(sj.name, args['name'])
		self.assertEqual(sj.elective, True)
		
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
		self.assertEqual(ret.status_int, 302) # 302=redirect
	
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
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		self.assertEqual(db.Publisher[3].name, 'C. C. Buchner')
		self.assertEqual(db.Publisher[4].name, 'Westermann')
		
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
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
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
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		self.assertEqual(db.Publisher[1].name, args['name'])
		
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
		self.assertEqual(ret.status_int, 302) # 302=redirect
	
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
		args = { "data": """Titel\t0815-000\t1234\tKlett\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t
Titel2\t0815-001\t1234\tKlett\t10\t12\tEng\tTrue\tFalse\tFalse\tFalse\tTrue\t
Titel3\t0815-002\t1234\tKlett\t10\t12\tRu\tTrue\tFalse\tFalse\tFalse\tTrue\tBla"""
		}
		ret = self.app.post('/admin/books/add', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# shhhh, I'm to lazy to test all three books completely .__.
		self.assertEqual(db.Book[10].title, 'Titel')
		self.assertEqual(db.Book[11].subject.tag, 'Eng')
		self.assertEqual(db.Book[12].comment, 'Bla')
		
		# show books list
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_books_add_ignore_newlines(self):
		Tests.prepare()
	
		# add books
		args = { "data": """Titel\t0815-000\t1234\tKlett\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t


Titel2\t0815-001\t1234\tKlett\t10\t12\tEng\tTrue\tFalse\tFalse\tFalse\tTrue\t

Titel3\t0815-002\t1234\tKlett\t10\t12\tRu\tTrue\tFalse\tFalse\tFalse\tTrue\t
"""
		}
		ret = self.app.post('/admin/books/add', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# show books list
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_books_add_minimal_data(self):
		Tests.prepare()
	
		# add book (invalid publisher)
		args = { "data": "Titel\t\t\tKlett\t10\t12" }
		ret = self.app.post('/admin/books/add', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		bk = db.Book[10]
		self.assertEqual(bk.title, 'Titel')
		self.assertEqual(bk.publisher.name, 'Klett')
		self.assertEqual(bk.inGrade, 10)
		self.assertEqual(bk.outGrade, 12)
		self.assertTrue(bk.for_loan)
		
		# show books list
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_books_add_invalid_data(self):
		Tests.prepare()
	
		# add book (invalid publisher)
		args = { "data": "Titel\t0815-000\t1234\tUnbekannt\t39\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t" }
		ret = self.app.post('/admin/books/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# show books list
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)
	
		# add book (invalid subject)
		args = { "data": "Titel\t0815-000\t1234\tKlett\t39\t10\t12\tFoo\tTrue\tFalse\tFalse\tFalse\tTrue\t" }
		ret = self.app.post('/admin/books/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# add book (invalid price)
		args = { "data": "Titel\t0815-000\tabc\tKlett\t39\t10\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t" }
		ret = self.app.post('/admin/books/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# add books (invalid inGrade)
		args = { "data": "Titel\t0815-000\t1234\tKlett\t39\tZehn\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t" }
		ret = self.app.post('/admin/books/add', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)
		
		# add books (invalid outGrade)
		args = { "data": "Titel\t0815-000\t1234\tKlett\t39\t10\tAbi\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t" }
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
			"price"        : "123",
			"publisher_id" : "1",
			"stock"        : "39",
			"inGrade"      : "10",
			"outGrade"     : "12",
			"subject_id"   : "2",
			"novices"      : "on",
			"advanced"     : "on", # @NOTE: empty str?
			"workbook"     : "on", # @NOTE: empty str?
			"classsets"    : "on",
			"for_loan"     : "off",
			"comment"      : ""
		}
		ret = self.app.post('/admin/books/edit/1', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		bk = db.Book[1]
		self.assertEqual(bk.title,        args['title'])
		self.assertEqual(bk.isbn,         args['isbn'])
		self.assertEqual(bk.price,        12300) # as cents
		self.assertEqual(bk.publisher.id, 1)
		self.assertEqual(bk.stock,        39)
		self.assertEqual(bk.inGrade,      10)
		self.assertEqual(bk.outGrade,     12)
		self.assertEqual(bk.subject.id,   2)
		self.assertTrue(bk.novices)
		self.assertTrue(bk.advanced)
		self.assertTrue(bk.workbook)
		self.assertTrue(bk.classsets)
		self.assertFalse(bk.for_loan)
		self.assertEqual(bk.comment, args['comment'])
		
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
			"for_loan"     : "off",
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
			"for_loan"     : "off",
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
		self.assertEqual(ret.status_int, 302) # 302=redirect
	
	@db_session
	def test_books_delete_invalid(self):
		Tests.prepare()
		
		# delete book
		ret = self.app.post('/admin/books/delete/1337', expect_errors=True)
		self.assertEqual(ret.status_int, 400)

	# -------------------------------------------------------------------------
	
	@db_session
	def test_classes_gui(self):
		Tests.prepare()
		
		# show classes gui
		ret = self.app.get('/admin/classes')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_classes_add(self):
		Tests.prepare()
		
		# add classes
		args = {"data": "09a\n05c\n\n11foo\n\n"}
		ret = self.app.post('/admin/classes/add', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# test new classes
		self.assertEqual(db.Class[4].grade, 9)
		self.assertEqual(db.Class[5].grade, 5)
		self.assertEqual(db.Class[6].grade, 11)
		self.assertEqual(db.Class[4].tag, 'a')
		self.assertEqual(db.Class[5].tag, 'c')
		self.assertEqual(db.Class[6].tag, 'foo')
		
		# show classes gui
		ret = self.app.get('/admin/books')
		self.assertEqual(ret.status_int, 200)

	@db_session
	def test_classes_edit(self):
		Tests.prepare()
		
		# edit class
		args = {"grade": 5, "tag": "d", "teacher_id": 1}
		ret = self.app.post('/admin/classes/edit/1', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# test changed class
		cs = db.Class[1]
		self.assertEqual(cs.grade, 5)
		self.assertEqual(cs.tag, "d")
		self.assertEqual(cs.teacher, db.Teacher[1])
	
	@db_session
	def test_classes_edit_can_reset_teacher(self):
		Tests.prepare()
		
		# edit class
		args = {"grade": 5, "tag": "d", "teacher_id": 0}
		ret = self.app.post('/admin/classes/edit/1', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# test changed class
		cs = db.Class[1]
		self.assertEqual(cs.grade, 5)
		self.assertEqual(cs.tag, "d")
		self.assertEqual(cs.teacher, None)
	
	@db_session
	def test_classes_edit_invalid_class(self):
		Tests.prepare()
		
		# edit class
		args = {"grade": 8, "tag": "a", "teacher_id": 0}
		ret = self.app.post('/admin/classes/edit/2', args, expect_errors=True)
		self.assertEqual(ret.status_int, 400)

	@db_session
	def test_classes_edit_can_keep_class_name(self):
		Tests.prepare()
		
		# edit class
		args = {"grade": 8, "tag": "a", "teacher_id": 0}
		ret = self.app.post('/admin/classes/edit/1', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect

	@db_session
	def test_classes_delete(self):
		Tests.prepare()
		
		# add empty class
		args = {"data": "09a"}
		ret = self.app.post('/admin/classes/add', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# delete class
		ret = self.app.post('/admin/classes/delete/4')
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# try access deleted class
		with self.assertRaises(orm.core.ObjectNotFound):
			cs = db.Class[4]
	
	# -----------------------------------------------------------------------------
	
	@db_session
	def test_students_gui(self):
		Tests.prepare()
		
		# show students gui
		ret = self.app.get('/admin/students')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_students_add(self):
		Tests.prepare()
		
		# add students
		args = {"data": "08a\tMustermann\tJürgen\n\n12glö\ta\tb\n"}
		ret = self.app.post('/admin/students/add', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# test new students
		self.assertEqual(db.Student[4].person.name,      "Mustermann")
		self.assertEqual(db.Student[4].person.firstname, "Jürgen")
		self.assertEqual(db.Student[4].class_, db.Class.get(grade=8, tag='a'))
		self.assertEqual(db.Student[5].person.name,      "a")
		self.assertEqual(db.Student[5].person.firstname, "b")
		self.assertEqual(db.Student[5].class_, db.Class.get(grade=12, tag='glö'))
		
		# show students gui
		ret = self.app.get('/admin/students')
		self.assertEqual(ret.status_int, 200)

	@db_session
	def test_students_search(self):
		Tests.prepare()
		
		# search for all students
		args = {"name": "", "firstname": ""}
		ret = self.app.post('/admin/students/search', args)
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_students_edit(self):
		Tests.prepare()
		
		# edit student
		args = {"name": "A", "firstname": "B", "class_id": 2}
		ret = self.app.post('/admin/students/edit/1', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# test changed student
		st = db.Student[1]
		self.assertEqual(st.person.name, 'A')
		self.assertEqual(st.person.firstname, 'B')
		self.assertEqual(st.class_, db.Class[2])
	
	@db_session
	def test_students_delete(self):
		Tests.prepare()
		
		# delete class
		ret = self.app.post('/admin/students/delete/1')
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# tra access deleted student
		with self.assertRaises(orm.core.ObjectNotFound):
			cs = db.Student[1]
	
	# -----------------------------------------------------------------------------
	
	@db_session
	def test_teachers_gui(self):
		Tests.prepare()
		
		# show teachers gui
		ret = self.app.get('/admin/teachers')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_teachers_add(self):
		Tests.prepare()
		
		# add teachers
		args = {"data": "tei\tTeichert\tHolger\n"}
		ret = self.app.post('/admin/teachers/add', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# test new students
		self.assertEqual(db.Teacher[3].tag,              "tei")
		self.assertEqual(db.Teacher[3].person.name,      "Teichert")
		self.assertEqual(db.Teacher[3].person.firstname, "Holger")
		
		# show students gui
		ret = self.app.get('/admin/teachers')
		self.assertEqual(ret.status_int, 200)

	@db_session
	def test_teachers_edit(self):
		Tests.prepare()
		
		# edit teacher
		args = {"name": "A", "firstname": "B", "tag": "C"}
		ret = self.app.post('/admin/teachers/edit/1', args)
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# test changed teacher
		tr = db.Teacher[1]
		self.assertEqual(tr.person.name, 'A')
		self.assertEqual(tr.person.firstname, 'B')
		self.assertEqual(tr.tag, 'c')
	
	@db_session
	def test_teachers_delete(self):
		Tests.prepare()
		
		# delete class
		ret = self.app.post('/admin/teachers/delete/1')
		self.assertEqual(ret.status_int, 302) # 302=redirect
		
		# tra access deleted student
		with self.assertRaises(orm.core.ObjectNotFound):
			cs = db.Teacher[1]
	
	# -----------------------------------------------------------------------------

	@db_session
	def test_settings_ui(self):
		ret = self.app.get('/admin/settings')
		self.assertEqual(ret.status_int, 200)
	
	@db_session
	def test_settings_post(self):
		s = Settings()
		with open('settings.ini') as h:
			s.load_from(h)
		
		args = {
			'school_year'       : '2018',
			'planner_price'     : '5,00€',
			'deadline_changes'  : '19.06.2017',
			'deadline_booklist' : '23.03.2017',
			'bookreturn_noexam' : '23.03.2017'
		}
		ret = self.app.post('/admin/settings', args)
		
		# override test-settings with original settings
		with open('settings.ini', 'w') as h:
			s.save_to(h)
		
		self.assertEqual(ret.status_int, 302) # 302=redirect
	
		# show settings gui
		ret = self.app.get('/admin/settings')
		self.assertEqual(ret.status_int, 200)

	# -------------------------------------------------------------------------
	
	@db_session
	def test_booklist_creation(self):
		Tests.prepare()
		
		# create all booklists (some even without books)
		# note: this may take some seconds
		ret = self.app.get('/admin/lists/generate/booklist')
		self.assertEqual(ret.status_code, 200)
		
		# show lists index
		ret = self.app.get('/admin/lists')
		self.assertEqual(ret.status_code, 200)

	@db_session
	def test_requestlist_creation(self):
		Tests.prepare()
		
		# create requestlists (some even without books)
		ret = self.app.get('/admin/lists/generate/requestlist')
		self.assertEqual(ret.status_code, 200)
		
		# show lists index
		ret = self.app.get('/admin/lists')
		self.assertEqual(ret.status_code, 200)

	@db_session
	def test_bookreturn_creation(self):
		Tests.prepare()
		
		# create bookreturn
		ret = self.app.get('/admin/lists/generate/bookreturn')
		self.assertEqual(ret.status_code, 200)
		
		# show lists index
		ret = self.app.get('/admin/lists')
		self.assertEqual(ret.status_code, 200)

	# -------------------------------------------------------------------------
	
	@db_session
	def test_demand_generation(self):
		Tests.prepare()
		
		# show demand form
		ret = self.app.get('/admin/demand')
		self.assertEqual(ret.status_code, 200)

		# build random demand post (and change path)
		global demand_json
		demand_json = '/tmp/demand.json'
		
		args = dict()
		
		for grade in range(5, 10+1):
			for sub in books.getSubjects(elective=True):
				key = "%s_%s" % (grade, sub.tag)
				args[key] = 63
		for grade in [11, 12]:
			for level in ['novices', 'advanced']:
				for sub in books.getSubjects():
					key = "%s_%s_%s" % (grade, sub.tag, level)
					args[key] = 23

		# post demand
		ret = self.app.post('/admin/demand', args)
		self.assertEqual(ret.status_code, 200)
			
		# show demand form (again)
		ret = self.app.get('/admin/demand')
		self.assertEqual(ret.status_code, 200)
	

