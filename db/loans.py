#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import date

from db.orm import db
from db import books, orga

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

def isRequested(student: db.Student, book: db.Book):
	"""Returns whether the given book is requested by the given student.
	"""
	for r in student.person.request:
		if r.book == book:
			return True
	return False

def updateRequest(student: db.Student, book: db.Book, status: bool):
	"""Update request status for the given book and the given student. If True
	is provided, a request object is created. If not, no request object exists
	for that student to that book.
	"""
	was = isRequested(student, book)
	if not was and status:
		# new request
		db.Request(person=student.person, book=book)
	elif was and not status:
		# delete request
		r = db.Request.get(person=student.person, book=book)
		r.delete()
	# else: nothing to update

def countNeededBooks(book: db.Book):
	"""Count how many books are required considering current loans, returning
	loans and new requested loans.
	"""

	# consider new requests
	n = len(book.request)
		
	# consider books already in used
	for l in book.loan:
		n += l.count
		
	# consider books being returned by last grade that uses it
	for c in orga.getClassesByGrade(book.outGrade):
		for s in c.student:
			if s.person in book.loan:
				l = db.Loan.get(person=s.person, book=book)
				n -= l.count
	
	return n

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
	def test_isRequested(self):
		Tests.prepare()
		
		db.Request(person=db.Student[3].person, book=db.Book[3])
		
		self.assertTrue(isRequested(db.Student[3], db.Book[3]))
		self.assertFalse(isRequested(db.Student[3], db.Book[5]))
		self.assertFalse(isRequested(db.Student[1], db.Book[3]))

	@db_session
	def test_updateRequest(self):
		Tests.prepare()
		
		self.assertEqual(len(db.Student[3].person.request), 0)
		
		# register book 3
		updateRequest(db.Student[3], db.Book[3], True)
		self.assertEqual(len(db.Student[3].person.request), 1)
		self.assertTrue(isRequested(db.Student[3], db.Book[3]))
		
		# double-register book 3
		updateRequest(db.Student[3], db.Book[3], True)
		self.assertEqual(len(db.Student[3].person.request), 1)
		
		# double-unregister book 5
		updateRequest(db.Student[3], db.Book[5], False)
		self.assertEqual(len(db.Student[3].person.request), 1)
		
		# register book 5
		updateRequest(db.Student[3], db.Book[5], True)
		self.assertEqual(len(db.Student[3].person.request), 2)
		self.assertTrue(isRequested(db.Student[3], db.Book[5]))
		
		# unregister book 3
		updateRequest(db.Student[3], db.Book[3], False)
		self.assertEqual(len(db.Student[3].person.request), 1)
		self.assertFalse(isRequested(db.Student[3], db.Book[3]))
		
		# unregister book 5
		updateRequest(db.Student[3], db.Book[5], False)
		self.assertEqual(len(db.Student[3].person.request), 0)
		self.assertFalse(isRequested(db.Student[3], db.Book[5]))

	@db_session
	def test_countNeededBooks(self):
		Tests.prepare()
		
		# prepare book
		b = db.Book(title='Example', isbn='000-001', price=2495,
			publisher=db.Publisher[1], inGrade=5, outGrade=7,
			subject=db.Subject[1])
		
		# prepare addition classes
		c_new  = db.Class(grade=5, tag='a')
		c_cont = db.Class(grade=6, tag='c')
		c_ret  = db.Class(grade=7, tag='b')
		for i in range(5):
			s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_new)
			db.Request(person=s.person, book=b)
		
		for i in range(5):
			s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_cont)
			db.Loan(person=s.person, book=b, given=date.today())

		# give 6th student two books		
		s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_cont)
		db.Loan(person=s.person, book=b, given=date.today(), count=2)
			
		for i in range(3):
			s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_ret)
			db.Loan(person=s.person, book=b, given=date.today())
		
		# give 4th student two books		
		s2 = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c_cont)
		db.Loan(person=s2.person, book=b, given=date.today(), count=2)
			
		n = countNeededBooks(b)
		# 5 new, 6+1 already used, 4+1 returning --> 17 needed
		self.assertEqual(n, 17)

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
		

