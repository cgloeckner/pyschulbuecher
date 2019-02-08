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
	teacher   = Optional("Teacher")
	student   = Optional("Student")
	loan      = Set("Loan")

class Teacher(db.Entity):
	id        = PrimaryKey(int, auto=True)
	person    = Required("Person")
	tag       = Required(str, unique=True)
	# reverse attribute
	class_    = Optional("Class")

class Class(db.Entity):
	id        = PrimaryKey(int, auto=True)
	grade     = Required(int)
	tag       = Required(str)
	teacher   = Optional(Teacher)
	# reverse attribute
	student   = Set("Student")

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
	book      = Set("Book")

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
	loan      = Set("Loan")

class Loan(db.Entity):
	id        = PrimaryKey(int, auto=True)
	person    = Required(Person)
	book      = Required(Book)
	given     = Required(date)
	count     = Required(int, default=1)


"""
# -----------------------------------------------------------------------------

import unittest

class Tests(unittest.TestCase):

	def setUp(self):
		db.generate_mapping(create_tables=True)
		
	def tearDown(self):
		db.drop_all_tables(with_all_data=True)

	@db_session
	def prepare(self):
		ma = db.Subject(name='Mathematik', tag='Ma')
		de = db.Subject(name='Deutsch', tag='De')
		
		t1 = db.Teacher(
			person=db.Person(name='Glöckner', firstname='Christian'),
			tag='Glö'
		)
		t2 = db.Teacher(
			person=db.Person(name='Lippmann', firstname='Iris'),
			tag='Lip'
		)
		
		for stufe in [5, 6, 7, 8, 9, 10]:
			for gruppe in ['a', 'b', 'c']:
				db.Class(grade=stufe, tag=gruppe)
		db.Class(grade=11, tag='Glö', teacher=t1)
		db.Class(grade=11, tag='Lip', teacher=t2)
	
		v1 = db.Publisher(name='Cornelsen')
		v2 = db.Publisher(name='Klett')
		
		self.b1 = db.Book(title='Mathematik II', isbn='0815', price=Decimal('24.95'),
			publisher=v1, inGrade=7, outGrade=9, subject=ma)
		self.b2 = db.Book(title='Mathematik Oberstufe', publisher=v2, inGrade=10,
			outGrade=12, subject=ma, novices=True, advanced=True)
	
		self.b3 = db.Book(title='Deutsch kompetent 9', publisher=v2, inGrade=9,
			outGrade=9, subject=de)
		self.b4 = db.Book(title='Tafelwerk', publisher=v1, inGrade=7, outGrade=12)
		

	@db_session
	def test_queryNewBooksForClass(self):
		self.prepare()
	
		result = select(
			b for b in db.Book
			if b.inGrade == 7
		)
				
		self.assertIn(self.b1, result)
		self.assertNotIn(self.b2, result)
		self.assertNotIn(self.b3, result)
		self.assertIn(   self.b4, result)


		#l1 = db.Loan(person=p2, book=b1, given=date.today()) # one book
		#l2 = db.Loan(person=p1, book=b3, given=date.today(), count=30) # class set

	print("All Books with at least 10 Books")
	result = select(b for b in db.Book if b.stock >= 10)
	for e in result:
		print(e.title)
		for s in e.subjects:
			print("\t", s.name)

if __name__ == '__main__':
	db.bind('sqlite', ':memory:', create_db=True)
	unittest.main()
"""

