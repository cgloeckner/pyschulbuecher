#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, configparser, datetime
import PyPDF2, xlsxwriter

from bottle import template
from latex import build_pdf

from db import books, orga, loans
from db.orm import Currency


def shortName(firstname):
	"""Abbreviate first name by reducing secondary first names to a single
	letter."""
	parts = firstname.split(' ')
	more = parts[0].split('-')
	out = more[0]
	for i in range(1, len(more)):
		out += '-%s.' % more[i][0]
	for i in range(1, len(parts)):
		out += ' %s.' % parts[i][0]
	return out


class Settings(object):

	def __init__(self):
		self.data = configparser.ConfigParser()
		self.data['general'] = {
			'school_year': '2019'
		}
		self.data['deadline'] = {
			'booklist_return'  : '17.03.2017',
			'booklist_changes' : '19.06.2017',
			'bookreturn_noexam': '17.03.2017'
		}

	def load_from(self, fhandle):
		tmp = configparser.ConfigParser()
		tmp.read_file(fhandle)
		# overwrite internal data
		self.data = tmp
	
	def save_to(self, fhandle):
		self.data.write(fhandle)

# -----------------------------------------------------------------------------

class SubjectCouncilXls(object):
	def __init__(self, settings_handle, export='export'):
		# prepare output directory
		if not os.path.isdir(export): # base dir
			os.mkdir(export)
		self.export = os.path.join(export, 'councils')
		if not os.path.isdir(self.export): # councils dir
			os.mkdir(self.export)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.data = None

	def __call__(self, subject):
		path = os.path.join(self.export, '%s.xlsx' % subject.tag)
		self.data = xlsxwriter.Workbook(path)
		
		"""
		# create sheets
		sheets = [
			{'name': 'Lehrbücher', 'items': books.getRealBooksBySubject(subject, False)},
			{'name': 'Arbeitshefte', 'items': books.getWorkbooksBySubject(subject)},
			{'name': 'Klassensätze', 'items': books.getClasssetsBySubject(subject)},
		]
		"""

		items = {
			'Leihbuch'   : books.getRealBooksBySubject(subject, False),
			'AH'         : books.getWorkbooksBySubject(subject),
			'Klassensatz': books.getClasssetsBySubject(subject)
		}
		
		title_format = self.data.add_format()
		title_format.set_bold()
		
		euro_format = self.data.add_format({'num_format': '#,##0.00€'})
		
		center_format = self.data.add_format()
		center_format.set_align('center')

		"""		
		for s in sheets:
			tab = self.data.add_worksheet(s['name'])
		
			tab.set_column(0, 0, 40)
			tab.set_column(1, 1, 25)
			tab.set_column(2, 2, 20)
			tab.set_column(3, 3, 8, euro_format)
			tab.set_column(4, 4, 15, grade_format)
			tab.set_column(5, 5, 30)
			
			for col, caption in enumerate(['Titel', 'Verlag', 'ISBN', 'Preis', 'Klassenstufe', 'Bemerkungen']):
				tab.write(0, col, caption, title_format)
		
			for row, b in enumerate(s['items']):
				tab.write(row+1, 0, b.title)
				if b.publisher is not None:
					tab.write(row+1, 1, b.publisher.name)
				if b.isbn is not None:
					tab.write(row+1, 2, b.isbn)
				if b.price is not None:
					tab.write(row+1, 3, b.price / 100.0)
				if b.inGrade == b.outGrade:
					tab.write(row+1, 4, b.inGrade)
				else:
					tab.write(row+1, 4, '%d-%d' % (b.inGrade, b.outGrade))
				
				comments = list()
				if b.comment != '':
					comments.append(b.comment)
				if b.novices:
					comments.append('gA')
				if b.advanced:
					comments.append('eA')
				tab.write(row+1, 5, ' '.join(comments))
		"""

		tab = self.data.add_worksheet(subject.tag)
		tab.set_landscape()
		tab.set_footer('Bücherbedarf &A (Stand &D)')
		tab.set_margins(top=1.25)
		
		tab.set_column(0, 0, 25)
		tab.set_column(1, 1, 20)
		tab.set_column(2, 2, 20)
		tab.set_column(3, 3, 8, euro_format)
		tab.set_column(4, 4, 8, center_format)
		tab.set_column(5, 5, 10, center_format)
		tab.set_column(6, 6, 25)
			
		for col, caption in enumerate(['Titel', 'Verlag', 'ISBN', 'Preis', 'Klasse', 'Art', 'Bemerkungen']):
			tab.write(0, col, caption, title_format)
		
		row = 0
		for kind in ['Leihbuch', 'AH', 'Klassensatz']:
			for b in items[kind]:
				tab.write(row+1, 0, b.title)
				if b.publisher is not None:
					tab.write(row+1, 1, b.publisher.name)
				if b.isbn is not None:
					tab.write(row+1, 2, b.isbn)
				if b.price is not None:
					tab.write(row+1, 3, b.price / 100.0)
				if b.inGrade == b.outGrade:
					tab.write(row+1, 4, b.inGrade)
				else:
					tab.write(row+1, 4, '%d-%d' % (b.inGrade, b.outGrade))
				tab.write(row+1, 5, kind)
				
				comments = list()
				if b.comment != '':
					comments.append(b.comment)
				if b.novices:
					comments.append('gA')
				if b.advanced:
					comments.append('eA')
				tab.write(row+1, 6, ' '.join(comments))

				row += 1
		
	def saveToFile(self):
		assert(self.data is not None)
		self.data.close()

# -----------------------------------------------------------------------------

class DatabaseDumpXls(object):
	def __init__(self, settings_handle, export='export'):
		# prepare output directory
		if not os.path.isdir(export): # base dir
			os.mkdir(export)
		self.export = export
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		# setup xlsx file
		path = os.path.join(self.export, '%s.xlsx' % self.s.data['general']['school_year'])		
		self.data = xlsxwriter.Workbook(path)

	def __call__(self, class_, bks):
		# local import to avoid cycles
		from db import loans
		
		# pre-order students abd books
		bks = books.orderBooksList(bks)
		students = list(class_.student)
		orga.sortStudents(students)
		
		title_format = self.data.add_format()
		title_format.set_bold()
		
		rotate_format = self.data.add_format()
		rotate_format.set_rotation(90)
		
		# create tab sheet for this class
		tab = self.data.add_worksheet(class_.toString())
		tab.set_column(0, 1, 12)
		tab.set_column(2, 2+len(bks), 4)
		tab.set_row(0, 150, rotate_format)
		
		fields = ['Name', 'Vorname']
		for col, b in enumerate(bks):
			fields.append(b.subject.tag if b.subject is not None else '')
			tab.write(0, col+2, b.title) # todo: 90° rotated format
		for col, caption in enumerate(fields):
			tab.write(1, col, caption, title_format)
		
		# fill students in
		for row, s in enumerate(students):
			tab.write(row+2, 0, s.person.name)
			tab.write(row+2, 1, shortName(s.person.firstname))
			for col, b in enumerate(bks):
				n = loans.getLoanCount(s.person, b)
				tab.write(row+2, col+2, n if n > 0 else '')
		
	def saveToFile(self):
		assert(self.data is not None)
		self.data.close()

# -----------------------------------------------------------------------------

class LoanReportPdf(object):
	def __init__(self, prefix, settings_handle, export='export'):
		# load LaTeX templates
		with open('docs/loanreport/header.tpl') as f:
			self.header = f.read()
		with open('docs/loanreport/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/loanreport/content.tpl') as f:
			self.content = f.read()
		# prepare output directory
		self.prefix = prefix
		self.export = export
		self.texdir = os.path.join(export, 'tex')
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.tex  = template(self.header)
	
	def __call__(self, person):
		"""Generate loan report pdf file for the given person. This will contain
		all books that are currently given to this person
		"""
		lns = loans.orderLoanOverview(person.loan)
		self.tex += template(self.content, s=self.s, p=person, lns=lns)
	
	def saveToFile(self):
		self.tex += template(self.footer)
		
		# export tex (debug purpose)
		dbg_fname = os.path.join(self.texdir, 'Leihübersicht_%s.tex' % self.prefix)
		with open(dbg_fname, 'w') as h:
			h.write(self.tex)
		
		# export PDF
		fname = os.path.join(self.export, 'Leihübersicht_%s.pdf' % self.prefix)
		pdf = build_pdf(self.tex)
		pdf.save_to(fname)
		
# -----------------------------------------------------------------------------

class LoanContractPdf(object):
	def __init__(self, prefix, settings_handle, export='export', advance=False):
		# load LaTeX templates
		with open('docs/loancontract/header.tpl') as f:
			self.header = f.read()
		with open('docs/loancontract/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/loancontract/content.tpl') as f:
			self.content = f.read()
		# prepare output directory
		self.prefix = prefix
		if not os.path.isdir(export): # base dir
			os.mkdir(export)
		self.export = os.path.join(export, 'contracts')
		self.texdir = os.path.join(export, 'tex')
		if not os.path.isdir(self.export): # specific dir
			os.mkdir(self.export)
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.tex     = template(self.header)
		self.advance = advance
	
	def __call__(self, student, include_requests=False, loan_report=False):
		"""Generate loan contract pdf file for the given student. This contains
		all books that are currently given to him or her. With 'loan_report'
		all books are listed as "you loan these books"
		"""
		lns = loans.orderLoanOverview(student.person.loan)
		rqs = list()
		if include_requests:
			rqs = loans.orderRequestOverview(student.person.request)
		self.tex += template(self.content, s=self.s, student=student, lns=lns, rqs=rqs, advance=self.advance, loan_report=loan_report)
	
	def saveToFile(self):
		self.tex += template(self.footer)
		
		# export tex (debug purpose)
		dbg_fname = os.path.join(self.texdir, 'Leihverträge_%s.tex' % self.prefix)
		with open(dbg_fname, 'w') as h:
			h.write(self.tex)
		
		# export PDF
		fname = os.path.join(self.export, 'Leihverträge_%s.pdf' % self.prefix)
		pdf = build_pdf(self.tex)
		pdf.save_to(fname)
		
# -----------------------------------------------------------------------------

class BooklistPdf(object):
	def __init__(self, settings_handle, export='export'):
		# load LaTeX templates
		with open('docs/booklist/header.tpl') as f:
			self.header = f.read()
		with open('docs/booklist/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/booklist/info.tpl') as f:
			self.info = f.read()
		with open('docs/booklist/select.tpl') as f:
			self.select = f.read()
		with open('docs/booklist/empty.tpl') as f:
			self.empty = f.read()
		with open('docs/booklist/special.tpl') as f:
			self.special = f.read()
		# prepare output directory
		if not os.path.isdir(export): # base dr
			os.mkdir(export)
		self.export = os.path.join(export, 'booklists')
		self.texdir = os.path.join(export, 'tex')
		if not os.path.isdir(self.export): # specific dir
			os.mkdir(self.export)
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		# merged pdf
		self.merger = PyPDF2.PdfFileMerger()
	
	def __call__(self, grade: int, exclude: set, new_students: bool=False):
		"""Generate booklist pdf file for the given grade. A separate booklist
		can be generated for new_students, which include additional books other
		students already have from earlier classes.
		The provided exclude set can be used to exclude books from the
		booklist. The keys are built from <grade>_<bookid>, if excluded this
		key's value is set to false.
		"""
		# fetch special books
		spec_bks = books.getBooksUsedIn(0, True)
		
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
		# render pure books
		if num_books > 0:
			tex += template(self.select, grade=grade, bs=bks, workbook=False, exclude=exclude)
		else:
			tex += template(self.empty, workbook=False)
		# render pure workbooks
		if num_books < len(bks):
			tex += template(self.select, grade=grade, bs=bks, workbook=True, exclude=exclude)
		else:
			tex += template(self.empty, workbook=True)
		tex += template(self.special, grade=grade, s=self.s, spec_bks=spec_bks)
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
		fname = os.path.join(self.export, 'Bücherzettel_Komplett.pdf')
		
		with open(fname, 'wb') as h:
			self.merger.write(h)

# -----------------------------------------------------------------------------

class RequestlistPdf(object):

	def __init__(self, settings_handle, export='export'):
		# load LaTeX templates
		with open('docs/requestlist/header.tpl') as f:
			self.header = f.read()
		with open('docs/requestlist/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/requestlist/content.tpl') as f:
			self.content = f.read()
		# prepare output directory
		self.export = export
		self.texdir = os.path.join(export, 'tex')
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.tex  = template(self.header)
	
	def __call__(self, class_):
		"""Generate requestlist pdf file for the given class.
		"""
		# fetch specific books
		spec_bks = books.getBooksUsedIn(0, True)
		
		# fetch and order books that are used next year by this class
		bks = books.getBooksStartedIn(class_.grade + 1)
		bks = books.orderBooksList(bks)
		
		# query students
		students = orga.getStudentsIn(class_.grade, class_.tag)
		
		# render template
		self.tex += template(self.content, s=self.s, class_=class_, bks=bks, students=students, spec_bks=spec_bks)
	
	def saveToFile(self):
		self.tex += template(self.footer)
		
		# export tex (debug purpose)
		dbg_fname = os.path.join(self.texdir, 'Erfassungsliste.tex')
		with open(dbg_fname, 'w') as h:
			h.write(self.tex)
		
		# export PDF
		fname = os.path.join(self.export, 'Bücherzettel_Erfassungsliste.pdf')
		pdf = build_pdf(self.tex)
		pdf.save_to(fname)

# -----------------------------------------------------------------------------

class BookreturnPdf(object):

	def __init__(self, settings_handle, export='export'):
		# load LaTeX templates
		with open('docs/bookreturn/header.tpl') as f:
			self.header = f.read()
		with open('docs/bookreturn/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/bookreturn/content.tpl') as f:
			self.content = f.read()
		with open('docs/bookreturn/overview.tpl') as f:
			self.overview = f.read()
		# prepare output directory
		self.export = export
		self.texdir = os.path.join(export, 'tex')
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.tex  = template(self.header)
	
	def addOverview(self, grade):
		"""Generate overviews for class teachers about returning books.
		"""
		# fetch and order books that are used next year by this class
		bks = books.getBooksFinishedIn(grade)
		bks = books.orderBooksList(bks)
		
		# render template
		self.tex += template(self.overview, s=self.s, grade=grade, bks=bks)
	
	def __call__(self, class_):
		"""Generate requestlist pdf file for the given class.
		"""
		# fetch and order books that are used next year by this class
		bks = books.getBooksFinishedIn(class_.grade)
		bks = books.orderBooksList(bks)
		
		# query students
		students = orga.getStudentsIn(class_.grade, class_.tag)
		
		# render template
		self.tex += template(self.content, s=self.s, class_=class_, bks=bks, students=students)
	
	def saveToFile(self):
		self.tex += template(self.footer)
		
		# export tex (debug purpose)
		dbg_fname = os.path.join(self.texdir, 'Rückgaben.tex')
		with open(dbg_fname, 'w') as h:
			h.write(self.tex)
		
		# export PDF
		fname = os.path.join(self.export, 'Rückgaben.pdf')
		pdf = build_pdf(self.tex)
		pdf.save_to(fname)


# -----------------------------------------------------------------------------

class BookloanPdf(object):

	def __init__(self, settings_handle, export='export'):
		# load LaTeX templates
		with open('docs/bookloan/header.tpl') as f:
			self.header = f.read()
		with open('docs/bookloan/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/bookloan/content.tpl') as f:
			self.content = f.read()
		# prepare output directory
		self.export = export
		self.texdir = os.path.join(export, 'tex')
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.tex  = template(self.header)
	
	def __call__(self, class_, request=False):
		"""Generate requestlist pdf file for the given class. If `requests` is
		provided with true, the request list for this year is used.
		"""
		grade = class_.grade
		
		# fetch and order books that were requested by this class
		bks = books.getBooksUsedIn(grade)
		bks = books.orderBooksList(bks)
		
		# fetch special books
		spec_bks = books.getBooksUsedIn(0, True)
		
		# query students
		students = orga.getStudentsIn(class_.grade, class_.tag)
		
		if request:
			query_func = loans.getRequestCount
		else:
			query_func = loans.getLoanCount
		
		# render template
		self.tex += template(self.content, s=self.s, class_=class_, bks=bks, students=students, spec_bks=spec_bks, query_func=query_func)
	
	def saveToFile(self):
		self.tex += template(self.footer)
		
		# export tex (debug purpose)
		dbg_fname = os.path.join(self.texdir, 'Ausgaben.tex')
		with open(dbg_fname, 'w') as h:
			h.write(self.tex)
		
		# export PDF
		fname = os.path.join(self.export, 'Ausgaben.pdf')
		pdf = build_pdf(self.tex)
		pdf.save_to(fname)

# -----------------------------------------------------------------------------

class BookpendingPdf(object):

	def __init__(self, settings_handle, export='export'):
		# load LaTeX templates
		with open('docs/bookpending/header.tpl') as f:
			self.header = f.read()
		with open('docs/bookpending/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/bookpending/content.tpl') as f:
			self.content = f.read()
		with open('docs/bookpending/perbook.tpl') as f:
			self.perbook = f.read()
		# prepare output directory
		self.export = export
		self.texdir = os.path.join(export, 'tex')
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.tex = template(self.header)

		self.n = 0
	
	def addPerson(self, person):
		"""Generate pending books pdf page for the given person
		"""
		count = len(person.loan)
		if count > 0:
			self.n += 1
			self.tex += template(self.content, s=self.s, person=person, n=self.n)
		
		return count
	
	def addPersons(self, book):
		"""Generate pending books pdf page for the given book
		"""
		lns = loans.queryLoansByBook(book)
		self.tex += template(self.perbook, s=self.s, book=book, loans=lns)

	def saveToFile(self, suffix, with_date=False):
		self.tex += template(self.footer)
		
		ext = ''
		if with_date:
			ext = '_%s' % datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
		pdfname = 'AusstehendeBücher_%s%s' % (suffix, ext)
		
		# export tex (debug purpose)
		dbg_fname = os.path.join(self.texdir, '%s.tex' % pdfname)
		with open(dbg_fname, 'w') as h:
			h.write(self.tex)
		
		# export PDF
		fname = os.path.join(self.export, '%s.pdf' % pdfname)
		pdf = build_pdf(self.tex)
		pdf.save_to(fname)
		
		return pdfname

# -----------------------------------------------------------------------------

class ClassListPdf(object):
	def __init__(self, settings_handle, export='export'):
		# load LaTeX templates
		with open('docs/classlist/header.tpl') as f:
			self.header = f.read()
		with open('docs/classlist/footer.tpl') as f:
			self.footer = f.read()
		with open('docs/classlist/content.tpl') as f:
			self.content = f.read()
		# prepare output directory
		self.export = export
		self.texdir = os.path.join(export, 'tex')
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.tex  = template(self.header)
	
	def __call__(self, classes):
		"""Add classes to the listing
		"""
		self.tex += template(self.content, s=self.s, classes=classes)
	
	def saveToFile(self):
		self.tex += template(self.footer)
		
		# export tex (debug purpose)
		dbg_fname = os.path.join(self.texdir, 'Klassenliste.tex')
		with open(dbg_fname, 'w') as h:
			h.write(self.tex)
		
		# export PDF
		fname = os.path.join(self.export, 'Klassenliste.pdf')
		pdf = build_pdf(self.tex)
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
	def test_create_custom_booklist(self):
		# create custom database content (real world example)
		books.addSubjects("Mathematik	Ma\nDeutsch	De\nEnglisch	En\nPhysik	Ph")
		books.addPublishers("Klett\nCornelsen")
		books.addBooks("""Ein Mathe-Buch	978-3-7661-5000-4	32,80 €	Cornelsen	5	12	Ma	True	True	False	False	True
Mathe AH	978-3-7661-5007-3	8,80 €	Cornelsen	5	12	Ma	True	True	True	False	True
Deutsch-Buch mit sehr langam Titel und damit einigen Zeilenumbrüchen .. ach und Umlaute in größeren Mengen öÖäÄüÜß sowie Sonderzeichen !"§$%&/()=?.:,;-_@	978-3-12-104104-6	35,95 €	Klett	11	12	De	True	True	False	False	True
Old English Book			Klett	5	12	En	True	True	False	True	True
Grundlagen der Physik			Cornelsen	5	12	Ph	True	True	False	False	True
Tafelwerk	978-3-06-001611-2	13,50 €	Cornelsen	7	12		False	False	False	False	True""")

		exclude = set()
		exclude.add('11_1') # "Ein Mathe-Buch"
		
		# create booklist
		with open('settings.ini') as h:
			booklist = BooklistPdf(h, export='/tmp/export')
		booklist(11, new_students=True, exclude=exclude)
		print('PLEASE MANUALLY VIEW /tmp/export/Buecherzettel11.pdf')

	@db_session
	def test_create_custom_requestlist(self):
		Tests.prepare()
		
		# create custom database content (real world example)
		books.addSubjects("Deutsch	De\nPhysik	Ph")
		books.addBooks("""Ein Mathe-Buch	978-3-7661-5000-4	32,80 €	Cornelsen	5	12	Ma	True	True	False	False	True
Mathe AH	978-3-7661-5007-3	8,80 €	Cornelsen	5	12	Ma	True	True	True	False	True
Deutsch-Buch mit sehr langam Titel und damit einigen Zeilenumbrüchen .. ach und Umlaute in größeren Mengen öÖäÄüÜß sowie Sonderzeichen !"§$%&/()=?.:,;-_@	978-3-12-104104-6	35,95 €	Klett	11	12	De	True	True	False	False	True
Old English Book			Klett	5	12	En	True	True	False	True	False
Grundlagen der Physik			Cornelsen	5	12	Ph	True	True	False	False	True
Tafelwerk	978-3-06-001611-2	13,50 €	Cornelsen	7	12		False	False	False	False	True""")

		# create requestlists
		with open('settings.ini') as h:
			requestlist = RequestlistPdf(h, export='/tmp/export')
		for c in select(c for c in db.Class):
			requestlist(c)
		requestlist.saveToFile()
		
		print('PLEASE MANUALLY VIEW /tmp/export/Erfassungsliste.pdf')

