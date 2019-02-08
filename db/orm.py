#!/usr/bin/python3
# -*- coding: utf-8 -*-

from decimal import Decimal
from datetime import date

from pony.orm import *


__author__ = "Christian Glöckner"


db = Database()

class Person(db.Entity):
	id        = PrimaryKey(int, auto=True)
	name      = Required(str)
	firstname = Required(str)
	# reverse attributes
	teacher   = Optional("Teacher", cascade_delete=True) # cascade to teacher
	student   = Optional("Student", cascade_delete=True) # cascade to person
	loan      = Set("Loan", cascade_delete=False) # restrict if loans assigned
	request   = Set("Request", cascade_delete=True) # cascade to request

class Teacher(db.Entity):
	id        = PrimaryKey(int, auto=True)
	person    = Required("Person")
	tag       = Required(str, unique=True)
	# reverse attribute
	class_    = Optional("Class", cascade_delete=False) # restrict if class assigned

class Class(db.Entity):
	id        = PrimaryKey(int, auto=True)
	grade     = Required(int)
	tag       = Required(str)
	teacher   = Optional(Teacher)
	# reverse attribute
	student   = Set("Student", cascade_delete=False) # restrict if students assigned

class Student(db.Entity):
	id        = PrimaryKey(int, auto=True)
	person    = Required("Person")
	class_    = Required(Class)

class Subject(db.Entity):
	id        = PrimaryKey(int, auto=True)
	name      = Required(str)
	tag       = Required(str, unique=True)
	# reverse attribute
	book      = Set("Book")

class Publisher(db.Entity):
	id        = PrimaryKey(int, auto=True)
	name      = Required(str, unique=True)
	# reverse attribute
	book      = Set("Book", cascade_delete=False) # restrict if books assigned

class Book(db.Entity):
	id        = PrimaryKey(int, auto=True)
	title     = Required(str)
	isbn      = Optional(str) # book could be out of the shops
	price     = Optional(Decimal) # book could be out of the shops
	publisher = Required(Publisher)
	stock     = Required(int, default=0)
	inGrade   = Required(int) # first grade that uses the book
	outGrade  = Required(int) # last grade that uses the book
	subject   = Optional(Subject) # None for subject-independent
	novices   = Required(bool, default=False) # suitable for novice courses?
	advanced  = Required(bool, default=False) # suitable for advanced courses?
	# reverse attribute
	loan      = Set("Loan", cascade_delete=False) # restrict if loans assigned
	request   = Set("Request", cascade_delete=False) # restrict if request assigned

class Loan(db.Entity):
	id        = PrimaryKey(int, auto=True)
	person    = Required(Person)
	book      = Required(Book)
	given     = Required(date)
	count     = Required(int, default=1)

class Request(db.Entity):
	id        = PrimaryKey(int, auto=True)
	person    = Required(Person)
	book      = Required(Book)


# -----------------------------------------------------------------------------

import unittest

class Tests(unittest.TestCase):
	
	def setUp(self):
		db.create_tables()
		
	def tearDown(self):
		db.drop_all_tables(with_all_data=True)

	@db_session
	def test_canDeletePerson(self):	
		p = db.Person(name='Foo', firstname='Bar')
		
		p.delete()
	
	@db_session
	def test_canDeleteStudentThroughPerson(self):
		p = db.Person(name='Foo', firstname='Bar')
		db.Student(person=p, class_=db.Class(grade=7, tag='b'))
		
		p.delete()
		s = select(s for s in db.Student)
		self.assertEqual(len(s), 0)
	
	@db_session
	def test_canDeleteTeacherThroughPerson(self):
		p = db.Person(name='Foo', firstname='Bar')
		db.Teacher(person=p, tag='FooB')
		
		p.delete()
		s = select(s for s in db.Teacher)
		self.assertEqual(len(s), 0)
	
	@db_session
	def test_cannotDeletePersonWithLoans(self):
		p = db.Person(name='Foo', firstname='Bar')
		
		db.Loan(person=p, given=date.today(),
			book=db.Book(title='spam', publisher=db.Publisher(name='lol'),
				inGrade=7, outGrade=9, subject=db.Subject(name='rofl', tag='xD')
			)
		)
		
		with self.assertRaises(core.ConstraintError):
			p.delete()
	
	@db_session
	def test_canDeletePersonAfterLoans(self):
		p = db.Person(name='Foo', firstname='Bar')
		
		db.Loan(person=p, given=date.today(),
			book=db.Book(title='spam', publisher=db.Publisher(name='lol'),
				inGrade=7, outGrade=9, subject=db.Subject(name='rofl', tag='xD')
			)
		)
		
		for l in p.loan:
			l.delete()
		
		p.delete()
	
	@db_session
	def test_canDeletePersonWithRequest(self):
		p = db.Person(name='Foo', firstname='Bar')
		
		db.Request(person=p, book=db.Book(title='spam',
			publisher=db.Publisher(name='lol'), inGrade=7, outGrade=9,
			subject=db.Subject(name='rofl', tag='xD')
		))
		
		p.delete()
		
		r = select(r for r in db.Request)
		self.assertEqual(len(r), 0)
	
	@db_session
	def test_canDeleteEmptyClass(self):
		c = db.Class(grade=5, tag='c')
		
		c.delete()
	
	@db_session
	def test_cannotDeleteNonEmptyClass(self):
		c = db.Class(grade=5, tag='c')
		db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c)
		
		with self.assertRaises(core.ConstraintError):
			c.delete()
	
	@db_session
	def test_canDeleteClassAfterClearing(self):
		c = db.Class(grade=5, tag='c')
		s = db.Student(person=db.Person(name='Foo', firstname='Bar'), class_=c)
		
		s.delete()
		c.delete()

	@db_session
	def test_canDeleteTeacherWithoutClass(self):
		t = db.Teacher(person=db.Person(name='Foo', firstname='Bar'), tag='FoB')
		
		t.person.delete()
	
	@db_session
	def test_canDeleteTeacherWithClass(self):
		t = db.Teacher(person=db.Person(name='Foo', firstname='Bar'), tag='FoB')
		c = db.Class(grade=5, tag='c', teacher=t)
		
		t.person.delete()
		
		self.assertEqual(c.teacher, None)

	@db_session
	def test_canDeleteSubjectWithoutBook(self):
		s = db.Subject(name='Foo', tag='Fo')
		
		s.delete()
	
	@db_session
	def test_canDeleteSubjectWithBook(self):
		s = db.Subject(name='Foo', tag='Fo')
		b = db.Book(title='Bar', publisher=db.Publisher(name='lol'),
			subject=s, inGrade=5, outGrade=6
		)
		
		s.delete()
		
		self.assertEqual(b.subject, None)
	
	@db_session
	def test_canDeletePublisherWithoutBook(self):
		p = db.Publisher(name='Foo')
		
		p.delete()
	
	@db_session
	def test_cannotDeletePublisherWithBook(self):
		p = db.Publisher(name='Foo')
		b = db.Book(title='Bar', publisher=p,
			subject=db.Subject(name='Foo', tag='Fo'), inGrade=5, outGrade=6
		)
		
		with self.assertRaises(core.ConstraintError):
			p.delete()
		
	@db_session
	def test_canDeletePublisherAfterBook(self):
		p = db.Publisher(name='Foo')
		b = db.Book(title='Bar', publisher=p,
			subject=db.Subject(name='Foo', tag='Fo'), inGrade=5, outGrade=6
		)
		
		b.delete()
		p.delete()
	
	@db_session
	def test_canDeleteBookWithoutLoan(self):
		b = db.Book(title='Bar', publisher=db.Publisher(name='Foo'),
			subject=db.Subject(name='Foo', tag='Fo'), inGrade=5, outGrade=6
		)
		
		b.delete()
	
	@db_session
	def test_cannotDeleteBookWithLoan(self):
		b = db.Book(title='Bar', publisher=db.Publisher(name='Foo'),
			subject=db.Subject(name='Foo', tag='Fo'), inGrade=5, outGrade=6
		)
		l = db.Loan(person=db.Person(name='lol', firstname='Bar'), book=b,
			given=date.today()
		)
		
		with self.assertRaises(core.ConstraintError):
			b.delete()
	
	@db_session
	def test_canDeleteBookAfterLoan(self):
		b = db.Book(title='Bar', publisher=db.Publisher(name='Foo'),
			subject=db.Subject(name='Foo', tag='Fo'), inGrade=5, outGrade=6
		)
		l = db.Loan(person=db.Person(name='lol', firstname='Bar'), book=b,
			given=date.today()
		)
		
		l.delete()
		b.delete()

	@db_session
	def test_canDeleteBookWithoutRequest(self):
		b = db.Book(title='Bar', publisher=db.Publisher(name='Foo'),
			subject=db.Subject(name='Foo', tag='Fo'), inGrade=5, outGrade=6
		)
		
		b.delete()
	
	@db_session
	def test_cannotDeleteBookWithRequest(self):
		b = db.Book(title='Bar', publisher=db.Publisher(name='Foo'),
			subject=db.Subject(name='Foo', tag='Fo'), inGrade=5, outGrade=6
		)
		r = db.Request(person=db.Person(name='lol', firstname='Bar'), book=b)
		
		with self.assertRaises(core.ConstraintError):
			b.delete()
	
	@db_session
	def test_canDeleteBookAfterRequest(self):
		b = db.Book(title='Bar', publisher=db.Publisher(name='Foo'),
			subject=db.Subject(name='Foo', tag='Fo'), inGrade=5, outGrade=6
		)
		r = db.Request(person=db.Person(name='lol', firstname='Bar'), book=b)
		
		r.delete()
		b.delete()

