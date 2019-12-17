#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, configparser, datetime
import PyPDF2, xlsxwriter

from bottle import template
from latex import build_pdf

from db import books, orga, loans
from db.orm import Currency

class Settings(object):

	def __init__(self):
		self.data = configparser.ConfigParser()
		self.data['general'] = {
			'school_year': '2019',
			'planner_price': '600'
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
		
		# create sheets
		sheets = [
			{'name': 'Lehrbücher', 'items': books.getRealBooksBySubject(subject, False)},
			{'name': 'Arbeitshefte', 'items': books.getWorkbooksBySubject(subject)},
			{'name': 'Klassensätze', 'items': books.getClasssetsBySubject(subject)},
		]
		
		for s in sheets:
			tab = self.data.add_worksheet(s['name'])
		
			for col, caption in enumerate(['Titel', 'Verlag', 'ISBN', 'Preis', 'Klassenstufe']):
				tab.write(0, col, caption)
			tab.set_column(0, 0, 50)
			tab.set_column(1, 1, 10)
			tab.set_column(2, 2, 20)
			tab.set_column(3, 3, 10)
			tab.set_column(4, 4, 10)
		
			for row, b in enumerate(s['items']):
				tab.write(row+1, 0, b.title)
				if b.publisher is not None:
					tab.write(row+1, 1, b.publisher.name)
				if b.isbn is not None:
					tab.write(row+1, 2, b.isbn)
				if b.price is not None:
					tab.write(row+1, 3, Currency.toString(b.price, addSymbol=False))
				if b.inGrade == b.outGrade:
					tab.write(row+1, 4, b.inGrade)
				else:
					tab.write(row+1, 4, '%d-%d' % (b.inGrade, b.outGrade)) 
		
	def saveToFile(self):
		assert(self.data is not None)

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
		if not os.path.isdir(self.export):
			os.mkdir(self.export)
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
	def __init__(self, prefix, settings_handle, export='export'):
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
		
		self.tex  = template(self.header)
	
	def __call__(self, student):
		"""Generate loan contract pdf file for the given student. This contains
		all books that are currently given to him or her.
		"""
		lns = loans.orderLoanOverview(student.person.loan)
		self.tex += template(self.content, s=self.s, student=student, lns=lns)
	
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
		with open('docs/booklist/planner.tpl') as f:
			self.planner = f.read()
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
		if not os.path.isdir(self.export):
			os.mkdir(self.export)
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.tex  = template(self.header)
	
	def __call__(self, class_):
		"""Generate requestlist pdf file for the given class.
		"""
		# fetch and order books that are used next year by this class
		bks = books.getBooksStartedIn(class_.grade + 1)
		bks = books.orderBooksList(bks)
		
		# query students
		students = orga.getStudentsIn(class_.grade, class_.tag)
		
		# render template
		self.tex += template(self.content, s=self.s, class_=class_, bks=bks, students=students)
	
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
		if not os.path.isdir(self.export):
			os.mkdir(self.export)
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
		if not os.path.isdir(self.export):
			os.mkdir(self.export)
		if not os.path.isdir(self.texdir):
			os.mkdir(self.texdir)
		# load settings
		self.s = Settings()
		self.s.load_from(settings_handle)
		
		self.tex  = template(self.header)
	
	def __call__(self, class_):
		"""Generate requestlist pdf file for the given class.
		"""
		# fetch and order books that were requested by this class
		bks = books.getBooksUsedIn(class_.grade)
		bks = books.orderBooksList(bks)
		
		# query students
		students = orga.getStudentsIn(class_.grade, class_.tag)
		
		# render template
		self.tex += template(self.content, s=self.s, class_=class_, bks=bks, students=students)
	
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
		
		self.tex  = template(self.header)
	
	def __call__(self, person):
		"""Generate pending books pdf file for the given person.
		"""
		count = len(person.loan)
		if count > 0:
			self.tex += template(self.content, s=self.s, person=person)
		
		return count
	
	def saveToFile(self, with_date=False):
		self.tex += template(self.footer)
		
		ext = ''
		if with_date:
			ext = '_%s' % datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
		pdfname = 'AusstehendeBücher%s' % ext
		
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

		# create booklist
		with open('settings.ini') as h:
			booklist = BooklistPdf(h, export='/tmp/export')
		booklist(11, new_students=True)
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

