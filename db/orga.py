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

def advanceSchoolYear(last_grade: int, first_grade: int, new_tags: list):
	"""Advance all students and classes to the next school year.
	All classes of the last_grade are dropped, so those students remain without
	any class. All remaining classes advance one grade and a new set of classes
	is created for the first_grade using a list of new_tags. Those classes are
	created without a teacher being assigned.
	"""
	# drop last grade's classes
	for c in getClassesByGrade(last_grade):
		c.delete()
	
	# advance all classes' grades
	for c in getClasses():
		c.grade += 1
	
	# create new clases for first grade
	for tag in new_tags:
		db.Class(grade=first_grade, tag=tag)


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
		c2 = db.Class(grade=12, tag=t1.tag, teacher=t1)
		c3 = db.Class(grade=12, tag='Lip')
		
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
		self.assertIn(12, gs)
	
	@db_session
	def test_getClassTags(self):
		self.prepare()
		
		tgs = getClassTags(12)
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
		cs = getClassesByGrade(12)
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

	@db_session
	def test_advanceSchoolYear(self):
		self.prepare()
		
		db.Class(grade=7, tag='a')
		db.Class(grade=9, tag='a')
		
		# advance to a new year with three 5th grades
		advanceSchoolYear(12, 5, ['a', 'b', 'c'])
		
		# check existing classes
		c9a  = db.Class[1]
		c8a  = db.Class[4]
		c10a = db.Class[5]
		c5a  = db.Class[6]
		c5b  = db.Class[7]
		c5c  = db.Class[8]
		
		self.assertEqual(c9a.grade,  9)
		self.assertEqual(c8a.grade,  8)
		self.assertEqual(c10a.grade, 10)
		self.assertEqual(c5a.grade,  5)
		self.assertEqual(c5b.grade,  5)
		self.assertEqual(c5c.grade,  5)
		self.assertEqual(c5a.tag, 'a')
		self.assertEqual(c5b.tag, 'b')
		self.assertEqual(c5c.tag, 'c')
		
		cs = getClasses()
		self.assertEqual(len(cs), 6)
		
		# check existing students
		self.assertEqual(db.Student[1].class_, c9a)
		self.assertEqual(db.Student[2].class_, c9a)
		self.assertEqual(db.Student[3].class_, None)

	@db_session
	def test_advanceMultipleSchoolYears(self):
		self.prepare()
		
		# 8a; 12glö, 12lip
		
		advanceSchoolYear(12, 5, ['a', 'b', 'c'])
		
		cs = getClasses()
		self.assertEqual(len(cs), 4)
		
		# 5a, 5b, 5c; 9a
		
		advanceSchoolYear(12, 5, ['a', 'b', 'c', 'd'])
		
		cs = getClasses()
		self.assertEqual(len(cs), 8)
		
		# 5a, 5b, 5c, 5d; 6a, 6b, 6c; 10a
		
		advanceSchoolYear(12, 5, ['a', 'b'])
		
		cs = getClasses()
		self.assertEqual(len(cs), 10)
		
		# 5a, 5b; 6a, 6b, 6c, 6d; 7a, 7b, 7c; 11a
		
		advanceSchoolYear(12, 5, ['a', 'b', 'c'])
		
		cs = getClasses()
		self.assertEqual(len(cs), 13)
		
		# 5a, 5b, 5c; 6a, 6b; 7a, 7b, 7c, 7d; 8a, 8b, 8c; 12a

		advanceSchoolYear(12, 5, ['a', 'b', 'c'])
		
		cs = getClasses()
		self.assertEqual(len(cs), 15)
		
		# 5a, 5b, 5c; 6a, 6b, 6c; 7a, 7b; 8a, 8b, 8c, 8d; 9a, 9b, 9c


