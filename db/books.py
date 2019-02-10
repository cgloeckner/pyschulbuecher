#!/usr/bin/python3
# -*- coding: utf-8 -*-

from db.orm import db, Currency


__author__ = "Christian Glöckner"


def getPublishers():
	"""Return a list of all publishers.
	"""
	return select(p
		for p in db.Publisher
	)

def getSubjects():
	"""Return a list of all subjects.
	"""
	return select(s
		for s in db.Subject
	)

def getAllBooks():
	"""Return a list of all books sorted by subject.tag, inGrade and title.
	"""
	return select(b
		for b in db.Book
	).order_by(db.Book.title).order_by(db.Book.inGrade).order_by(db.Book.subject)

def getBooksWithoutSubject():
	"""Return a list of books which are not assigned to a specific subject.
	Those books are supposed to be used across subjects.
	"""
	return select(b
		for b in db.Book
			if b.subject is None
	)

def getBooksUsedIn(grade: int):
	"""Return a list of books which are used in the given grade.
	This includes books which are used across multiple grades, as well as books
	that are only used by this grade.
	"""
	return select(b
		for b in db.Book
			if b.inGrade <= grade
			and grade <= b.outGrade
	)

def getBooksStartedIn(grade: int):
	"""Return a list of books which are introduced in the given grade.
	This includes books which are used across multiple grades (from that grade)
	on, as well as books which are only used by this grade.
	"""
	return select(b
		for b in db.Book
			if b.inGrade == grade
	)

def getBooksFinishedIn(grade: int):
	"""Return a list of books which are used in the given grade for the last
	time. This includes books which are used across multiple grades (up to this
	grade), as well as books that are only used by this grade.
	"""
	return select(b
		for b in db.Book
			if b.outGrade == grade
	)

def getBooksByTitle(title: str):
	"""Return a list of books with similar titles.
	"""
	return select(b
		for b in db.Book
			if title in b.title
	)

def getBooksByIsbn(isbn: str):
	"""Returns a list of books with this exact isbn.
	Note that most commonly, only one or none will be returned. If an empty
	string is given as isbn, all books without isbn are returned. Note that
	this is mostly used for books which are not longer available in market.
	"""
	return select(b
		for b in db.Book
			if isbn == b.isbn
	)


# -----------------------------------------------------------------------------

def addSubjects(raw: str):
	"""Add subjects from a given raw string dump, assuming subjects being
	separated by newlines. Name and tag are assumed to be separated by a tab.
	"""
	for data in raw.split("\n"):
		res = data.split("\t")
		assert(len(res) == 2)
		db.Subject(name=res[0], tag=res[1])

def addPublishers(raw: str):
	"""Add publishers from a given raw string dump, assuming publishers being
	separated by newlines
	"""
	for data in raw.split("\n"):
		db.Publisher(name=data)

def addBook(raw: str):
	"""Add book from a given raw string dump, assuming all information being
	separated by tabs in the following order:
		Title, ISBN, Price, Publisher, inGrade, outGrade
	Optional: Subject, Novices, Advanced, Workbook, Classsets, Comment
	Earlier optional data must be provided (at least as empty strings) if a
	later parameter is given.
	"""
	# split data
	data = raw.split('\t')
	title, isbn, price, publisher, inGrade, outGrade = data[:6]
	subject   = data[6]  if  6 < len(data) else ""
	novices   = data[7]  if  7 < len(data) else ""
	advanced  = data[8]  if  8 < len(data) else ""
	workbook  = data[9]  if  9 < len(data) else ""
	classsets = data[10] if 10 < len(data) else ""
	comment   = data[11] if 11 < len(data) else ""
	
	# fix parameters
	price    = Currency.fromString(price) if price != "" else None
	inGrade  = int(inGrade)
	outGrade = int(outGrade)
	
	novices   = True if novices   == 'True' else False
	advanced  = True if advanced  == 'True' else False
	workbook  = True if workbook  == 'True' else False
	classsets = True if classsets == 'True' else False
	
	# query referenced entities
	publisher = db.Publisher.get(name=publisher)
	subject   = db.Subject.get(tag=subject) if subject != "" else None
	
	# create actual book
	db.Book(title=title, isbn=isbn, price=price, publisher=publisher,
		inGrade=inGrade, outGrade=outGrade, subject=subject, novices=novices,
		advanced=advanced, workbook=workbook, classsets=classsets,
		comment=comment)

def addBooks(raw: str):
	"""Add books from a given raw string dump, assuming all books being
	separated by newlines. Each line is handled by addBook().
	"""
	for data in raw.split('\n'):
		addBook(data)


# -----------------------------------------------------------------------------

import unittest

from pony.orm import *

from db.orm import db

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
		
	def tearDown(self):
		db.drop_all_tables(with_all_data=True)

	@db_session
	def test_getPublishers(self):
		Tests.prepare()
		
		ps = getPublishers()
		self.assertEqual(len(ps), 2)
		self.assertIn(db.Publisher[1], ps)
		self.assertIn(db.Publisher[2], ps)
	
	@db_session
	def test_getSubjects(self):
		Tests.prepare()
		
		sb = getSubjects()
		self.assertEqual(len(sb), 3)
		self.assertIn(db.Subject[1], sb)
		self.assertIn(db.Subject[2], sb)
		self.assertIn(db.Subject[3], sb)
	
	@db_session
	def test_getAllBooks(self):
		Tests.prepare()
		
		bs = list(getAllBooks())
		self.assertEqual(len(bs), 9)
		self.assertEqual(bs[0], db.Book[8]) # subject-independend
		self.assertEqual(bs[1], db.Book[1]) # Math book since 5th grade
		self.assertEqual(bs[2], db.Book[2]) # Math book since 7th grade
		self.assertEqual(bs[4], db.Book[5]) # advanced Math book since 11th grade
		self.assertEqual(bs[5], db.Book[4]) # basic book since 7th grade
	
	@db_session
	def test_getBooksWithoutSubject(self):
		Tests.prepare()
		
		bs = getBooksWithoutSubject()
		self.assertEqual(len(bs), 1)
		self.assertIn(db.Book[8], bs)
		
	@db_session
	def test_getBooksUsedIn(self):
		Tests.prepare()
		
		bs = getBooksUsedIn(5)
		self.assertEqual(len(bs), 3)
		self.assertIn(db.Book[1], bs)
		self.assertIn(db.Book[6], bs)
		self.assertIn(db.Book[9], bs)
		
		bs = getBooksUsedIn(6)
		self.assertEqual(len(bs), 2)
		self.assertIn(db.Book[1], bs)
		self.assertIn(db.Book[6], bs)
		
		bs = getBooksUsedIn(7)
		self.assertEqual(len(bs), 3)
		self.assertIn(db.Book[2], bs)
		self.assertIn(db.Book[6], bs)
		self.assertIn(db.Book[8], bs)
		
		bs = getBooksUsedIn(10)
		self.assertEqual(len(bs), 3)
		self.assertIn(db.Book[3], bs)
		self.assertIn(db.Book[6], bs)
		self.assertIn(db.Book[8], bs)
		
		bs = getBooksUsedIn(11)
		self.assertEqual(len(bs), 4)
		self.assertIn(db.Book[4], bs)
		self.assertIn(db.Book[5], bs)
		self.assertIn(db.Book[7], bs)
		self.assertIn(db.Book[8], bs)
		
		bs = getBooksUsedIn(13)
		self.assertEqual(len(bs), 0)

	@db_session
	def test_getBooksStartedIn(self):
		Tests.prepare()
		
		bs = getBooksStartedIn(5)
		self.assertEqual(len(bs), 3)
		self.assertIn(db.Book[1], bs)
		self.assertIn(db.Book[6], bs)
		self.assertIn(db.Book[9], bs)
		
		bs = getBooksStartedIn(6)
		self.assertEqual(len(bs), 0)
		
		bs = getBooksStartedIn(7)
		self.assertEqual(len(bs), 2)
		self.assertIn(db.Book[2], bs)
		self.assertIn(db.Book[8], bs)
		
		bs = getBooksStartedIn(11)
		self.assertEqual(len(bs), 3)
		self.assertIn(db.Book[4], bs)
		self.assertIn(db.Book[5], bs)
		self.assertIn(db.Book[7], bs)
		
	@db_session
	def test_getBooksFinishedIn(self):
		Tests.prepare()
		
		bs = getBooksFinishedIn(5)
		self.assertEqual(len(bs), 1)
		self.assertIn(db.Book[9], bs)
		
		bs = getBooksFinishedIn(6)
		self.assertEqual(len(bs), 1)
		self.assertIn(db.Book[1], bs)
		
		bs = getBooksFinishedIn(10)
		self.assertEqual(len(bs), 2)
		self.assertIn(db.Book[3], bs)
		self.assertIn(db.Book[6], bs)
		
		bs = getBooksFinishedIn(12)
		self.assertEqual(len(bs), 4)
		self.assertIn(db.Book[4], bs)
		self.assertIn(db.Book[5], bs)
		self.assertIn(db.Book[7], bs)
		self.assertIn(db.Book[8], bs)

	@db_session
	def test_getBooksByTitle(self):
		Tests.prepare()
		
		bs = getBooksByTitle('Maths')
		self.assertEqual(len(bs), 5)
		self.assertIn(db.Book[1], bs)
		self.assertIn(db.Book[2], bs)
		self.assertIn(db.Book[3], bs)
		self.assertIn(db.Book[4], bs)
		self.assertIn(db.Book[5], bs)

	@db_session
	def test_getBooksByIsbn(self):
		Tests.prepare()
		
		# single book
		bs = getBooksByIsbn('236-7634-62')
		self.assertEqual(len(bs), 1)
		self.assertIn(db.Book[8], bs)
		
		# all not yet available books
		bs = getBooksByIsbn('')
		self.assertEqual(len(bs), 3)
		self.assertIn(db.Book[4], bs)
		self.assertIn(db.Book[5], bs)
		self.assertIn(db.Book[9], bs)

	@db_session
	def test_addSubjects(self):
		raw = """Mathematik\tMa
Englisch\tEn
Deutsch\tDe
Sport\tSp"""
		addSubjects(raw)
		
		s = select(s.name for s in db.Subject)
		self.assertEqual(len(s), 4)
		self.assertIn("Mathematik", s)
		self.assertIn("Englisch", s)
		self.assertIn("Deutsch", s)
		self.assertIn("Sport", s)

	@db_session
	def test_addPublishers(self):
		raw = """Cornelsen
Klett
Volk & Wissen
C.C. Buchner"""
		addPublishers(raw)
		
		p = select(s.name for s in db.Publisher)
		self.assertEqual(len(p), 4)
		self.assertIn("Cornelsen", p)
		self.assertIn("Klett", p)
		self.assertIn("Volk & Wissen", p)
		self.assertIn("C.C. Buchner", p)

	@db_session
	def test_canAddBookWithFullInformation(self):
		addSubjects("Mathematik\tMa")
		addPublishers("Klett")
		
		raw = "Mathematik Live\t0815-1234\t23,95 €\tKlett\t11\t12\tMa\tTrue\tFalse\tFalse\tFalse\tLehrbuch"
		addBook(raw)
		
		b = db.Book[1]
		self.assertEqual(b.title, "Mathematik Live")
		self.assertEqual(b.isbn, "0815-1234")
		self.assertEqual(b.price, 2395)
		self.assertEqual(b.publisher, db.Publisher[1])
		self.assertEqual(b.inGrade, 11)
		self.assertEqual(b.outGrade, 12)
		self.assertEqual(b.subject, db.Subject[1])
		self.assertTrue(b.novices)
		self.assertFalse(b.advanced)
		self.assertFalse(b.workbook)
		self.assertFalse(b.classsets)
		self.assertEqual(b.comment, "Lehrbuch")
	
	@db_session
	def test_canAddBookWithMinimalInformation(self):
		addPublishers("Klett")
		
		raw = "Das Große Tafelwerk\t\t\tKlett\t7\t12\t\t\t\t\t\t"
		addBook(raw)
		
		b = db.Book[1]
		self.assertEqual(b.title, "Das Große Tafelwerk")
		self.assertEqual(b.isbn, "")
		self.assertEqual(b.price, None)
		self.assertEqual(b.publisher, db.Publisher[1])
		self.assertEqual(b.inGrade, 7)
		self.assertEqual(b.outGrade, 12)
		self.assertFalse(b.novices)
		self.assertFalse(b.advanced)

	@db_session
	def test_addBooks(self):
		addPublishers("Klett\nCornelsen")
		addSubjects("Mathemati\tMa\nEnglisch\tEng")
		
		raw = """Mathematik Live\t0815-1234\t2395\tKlett\t11\t12\tMa\tTrue\tFalse\tFalse\tFalse\t
Tafelwerk\t12-52-6346\t1999\tKlett\t7\t12\t\tFalse\tFalse\tFalse\tFalse\tfächerübergreifend
Englisch Oberstufe\t433-5213-6246\t4995\tCornelsen\t11\t12\tEng\tTrue\tTrue\tFalse\tFalse\t
Das Große Tafelwerk\t\t\tKlett\t7\t12\t\tFalse\tFalse\tFalse\tFalse\tfächerübergreifend"""
	
		addBooks(raw)
		
		b1 = db.Book[1]
		b2 = db.Book[2]
		b3 = db.Book[3]
		b4 = db.Book[4]
		
		self.assertEqual(b1.title, "Mathematik Live")
		self.assertEqual(b2.title, "Tafelwerk")
		self.assertEqual(b3.title, "Englisch Oberstufe")
		self.assertEqual(b4.title, "Das Große Tafelwerk")
		self.assertTrue(b3.novices)
		self.assertTrue(b3.advanced)


