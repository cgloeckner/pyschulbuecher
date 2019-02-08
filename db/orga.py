#!/usr/bin/python3
# -*- coding: utf-8 -*-

from db.orm import db

__author__ = "Christian Glöckner"


def getClassGrades():
	"""Return a list of grades for which classes exist.
	"""
	return select(c.grade for c in db.Class)

def getClassTags(grade: int):
	"""Return a list of tags for which classes exist in the given grade.
	"""
	return select(c.tag for c in db.Class if c.grade == grade)

def getClasses():
	"""Return a list of all existing classes.
	"""
	return select(c for c in db.Class)

def getClassesByGrade(grade: int):
	"""Return a list of classes which exist in the given grade.
	"""
	return select(c for c in db.Class if c.grade == grade)

def getStudentsLike(name: str="", firstname: str=""):
	"""Return a list of students by name and firstname using partial matching.
	Both parameters default to an empty string if not specified.
	"""
	return select(s for s in db.Student if name in s.person.name and firstname in s.person.firstname)


# -----------------------------------------------------------------------------

import unittest

from pony.orm import *

from db.orm import db

class Tests(unittest.TestCase):

	@db_session
	def prepare(self):
		# create teachers
		t1 = db.Teacher(
			person=db.Person(name='Glöckner', firstname='Christian'),
			tag='Glö'
		)
		t2 = db.Teacher(
			person=db.Person(name='Thiele', firstname='Felix'),
			tag='Thi'
		)
		
		# create some classes
		c1 = db.Class(grade=8, tag='a', teacher=t2)
		c2 = db.Class(grade=11, tag=t1.tag, teacher=t1)
		c3 = db.Class(grade=11, tag='Lip')
		
		# create students
		s1 = db.Student(
			person=db.Person(name='Mustermann', firstname='Florian'),
			class_=c1
		)
		s2 = db.Student(
			person=db.Person(name='Schmidt', firstname='Fabian'),
			class_=c1
		)
		s3 = db.Student(
			person=db.Person(name='Schneider', firstname='Max'),
			class_=c2
		)
	
	def setUp(self):
		db.create_tables()
		
	def tearDown(self):
		db.drop_all_tables(with_all_data=True)

	@db_session
	def test_getClassGrades(self):
		self.prepare()
		
		gs = getClassGrades()
		self.assertEqual(len(gs), 2)
		self.assertIn(8, gs)
		self.assertIn(11, gs)
	
	@db_session
	def test_getClassTags(self):
		self.prepare()
		
		tgs = getClassTags(11)
		self.assertEqual(len(tgs), 2)
		self.assertIn('Glö', tgs)
		self.assertIn('Lip', tgs)

		tgs = getClassTags(8)
		self.assertEqual(len(tgs), 1)
		self.assertIn('a', tgs)

	@db_session
	def test_getClasses(self):
		self.prepare()
		
		cs = getClasses()
		self.assertEqual(len(cs), 3)
		self.assertIn(db.Class[1], cs)
		self.assertIn(db.Class[2], cs)
		self.assertIn(db.Class[3], cs)
	
	@db_session
	def test_getClassesByGrade(self):
		self.prepare()
		
		# single class
		cs = getClassesByGrade(8)
		self.assertEqual(len(cs), 1)
		self.assertIn(db.Class[1], cs)
		
		# multiple classes
		cs = getClassesByGrade(11)
		self.assertEqual(len(cs), 2)
		self.assertIn(db.Class[2], cs)
		self.assertIn(db.Class[3], cs)
		
		# no classes
		cs = getClassesByGrade(9)
		self.assertEqual(len(cs), 0)
	
	@db_session
	def test_getStudentsLike(self):
		self.prepare()
		
		# by name
		st = getStudentsLike(name='ch')
		self.assertEqual(len(st), 2)
		self.assertIn(db.Student[2], st)
		self.assertIn(db.Student[3], st)
		
		# by firstname
		st = getStudentsLike(firstname='ia')
		self.assertEqual(len(st), 2)
		self.assertIn(db.Student[1], st)
		self.assertIn(db.Student[2], st)
		
		# using both
		st = getStudentsLike(name='ch', firstname='ia')
		self.assertEqual(len(st), 1)
		self.assertIn(db.Student[2], st)


