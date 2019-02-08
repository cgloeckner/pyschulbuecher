#!/usr/bin/python3
# -*- coding: utf-8 -*-

from db.orm import db

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

import unittest
from decimal import Decimal

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
		db.Book(title='Maths I', isbn='000-001', price=Decimal('24.95'),
			publisher=db.Publisher[1], inGrade=5, outGrade=6,
			subject=db.Subject[1])
		db.Book(title='Maths II', isbn='001-021', price=Decimal('29.99'),
			publisher=db.Publisher[1], inGrade=7, outGrade=8,
			subject=db.Subject[1])
		db.Book(title='Maths III', isbn='914-721', price=Decimal('34.99'),
			publisher=db.Publisher[1], inGrade=9, outGrade=10,
			subject=db.Subject[1])
		db.Book(title='Basic Maths', publisher=db.Publisher[1], inGrade=11,
			outGrade=12, subject=db.Subject[1], novices=True)
		db.Book(title='Advanced Maths', publisher=db.Publisher[1], inGrade=11,
			outGrade=12, subject=db.Subject[1], advanced=True)
		
		# create russian books
		db.Book(title='Privjet', isbn='49322-6346', price=Decimal('59.99'),
			publisher=db.Publisher[2], inGrade=5, outGrade=10,
			subject=db.Subject[2])
		db.Book(title='Dialog', isbn='43623-8485', price=Decimal('79.99'),
			publisher=db.Publisher[2], inGrade=11, outGrade=12,
			subject=db.Subject[2], novices=True, advanced=True)
		
		# create subject-independent books
		db.Book(title='Formulary', isbn='236-7634-62', price=Decimal('22.95'),
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



