#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import date

from db.orm import db
from db import books

__author__ = "Christian Glöckner"

def getExpectedReturns(student: db.Student):
	"""Returns a list of loans which are expected to be returned referring
	the student's current grade.
	"""
	return select(l
		for l in db.Loan
			if l.person == student.person
			and l.book.outGrade <= student.class_.grade
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
		import db.orga, db.books
		
		db.orga.Tests.prepare()
		db.books.Tests.prepare()
	
	def setUp(self):
		db.create_tables()
		
	def tearDown(self):
		db.drop_all_tables(with_all_data=True)

	@db_session
	def test_addLoans(self):
		Tests.prepare()
		
		# regular usecase
		db.Loan(person=db.Student[3].person, book=db.Book[3], given=date.today())
		db.Loan(person=db.Student[3].person, book=db.Book[5], given=date.today())
		db.Loan(person=db.Student[3].person, book=db.Book[8], given=date.today())
		
		ln = list(db.Student[3].person.loan)
		self.assertEqual(len(ln), 3)
		bs = set()
		for l in ln:
			self.assertEqual(l.count, 1)
			self.assertEqual(l.given, date.today())
			bs.add(l.book)
		self.assertIn(db.Book[3], bs)
		self.assertIn(db.Book[5], bs)
		self.assertIn(db.Book[8], bs)
		
		# with 2nd set
		db.Loan(person=db.Student[1].person, book=db.Book[3], given=date.today(), count=2)
		db.Loan(person=db.Student[1].person, book=db.Book[5], given=date.today(), count=2)
		db.Loan(person=db.Student[1].person, book=db.Book[8], given=date.today(), count=2)

		ln = list(db.Student[1].person.loan)
		self.assertEqual(len(ln), 3)
		bs = set()
		for l in ln:
			self.assertEqual(l.count, 2)
			self.assertEqual(l.given, date.today())
			bs.add(l.book)
		self.assertIn(db.Book[3], bs)
		self.assertIn(db.Book[5], bs)
		self.assertIn(db.Book[8], bs)
		
		# giving 30 books to a teacher
		db.Loan(person=db.Teacher[1].person, book=db.Book[3], given=date.today(), count=30)

		ln = list(db.Teacher[1].person.loan)
		self.assertEqual(len(ln), 1)
		self.assertEqual(ln[0].book, db.Book[3])
		self.assertEqual(ln[0].count, 30)
		self.assertEqual(ln[0].given, date.today())
	
	@db_session
	def test_getExpectedReturns(self):
		Tests.prepare()
		
		# give away some books to 12th grade student
		db.Loan(person=db.Student[3].person, book=db.Book[3], given=date.today())
		db.Loan(person=db.Student[3].person, book=db.Book[5], given=date.today())
		db.Loan(person=db.Student[3].person, book=db.Book[8], given=date.today())
		
		# expected returns for 12th grade
		ln = list(getExpectedReturns(db.Student[3]))
		self.assertEqual(len(ln), 3)
		bs = set()
		for l in ln:
			bs.add(l.book)
		self.assertIn(db.Book[3], bs)
		self.assertIn(db.Book[5], bs)
		self.assertIn(db.Book[8], bs)
		
		# expected returns for 11th
		db.Student[3].class_.grade = 11
		
		ln = list(getExpectedReturns(db.Student[3]))
		self.assertEqual(len(ln), 1)
		self.assertEqual(ln[0].book, db.Book[3]) # yet outdated (ends at 10)
		
		# give away some books to 8th grade student
		db.Loan(person=db.Student[1].person, book=db.Book[2], given=date.today())
		db.Loan(person=db.Student[1].person, book=db.Book[6], given=date.today())
		db.Loan(person=db.Student[1].person, book=db.Book[8], given=date.today())
		
		# expected returns for 8th grade
		ln = list(getExpectedReturns(db.Student[1]))
		self.assertEqual(len(ln), 1)
		self.assertEqual(ln[0].book, db.Book[2])
		
		# expected returns for 7th grade
		db.Student[1].class_.grade = 7
		ln = list(getExpectedReturns(db.Student[1]))
		self.assertEqual(len(ln), 0)
		

