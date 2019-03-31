#!/usr/bin/python3
# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

from pony import orm

from db.orm import db

__author__ = "Christian Glöckner"

def getClassGrades():
	"""Return a list of grades for which classes exist.
	"""
	return select(c.grade
		for c in db.Class
	).order_by(lambda g: g)

def getClassTags(grade: int):
	"""Return a list of tags for which classes exist in the given grade.
	"""
	return select(c.tag
		for c in db.Class
			if c.grade == grade
	).order_by(lambda t: t)

def getClasses():
	"""Return a list of all existing classes.
	"""
	return select(c
		for c in db.Class
	)

def getClassesByGrade(grade: int):
	"""Return a list of classes which exist in the given grade.
	"""
	return select(c
		for c in db.Class
			if c.grade == grade
	).order_by(db.Class.tag)

def getClassesCount():
	"""Return total number of classes.
	"""
	return db.Class.select().count()

def getStudentsCount(grade: int):
	"""Return total number of students in the given grade.
	"""
	cs = getClassesByGrade(grade)
	total = 0
	for c in cs:
		total += len(c.student)
	return total

def getStudentsIn(grade: int, tag: str):
	"""Return all students in the given grade.
	"""
	# Note: explicit list conversion + sort (instead directly order_by)
	# to fix use of Umlaute while sorting
	# e.g. handling O and Ö similar instead of sorting Ö after Z
	l = list(db.Class.get(grade=grade, tag=tag).student)
	#l.sort(key=lambda s: locale.strxfrm(s.person.firstname))
	l.sort(key=lambda s: locale.strxfrm(s.person.name))
	return l

# -----------------------------------------------------------------------------

def parseClass(raw: str):
	"""Parse class grade and tag from a raw string.
	"""
	grade = raw[:2]
	tag   = raw.split(grade)[1].lower()
	return int(grade), tag

def addClass(raw: str):
	"""Add a new class from a ggiven raw string. This string contains the
	grade (with ALWAYS two characters, like '08') followed by the class tag
	(e.g. '08a'), where uppercase characters are ignored. No teacher is
	assigned to this class.
	"""
	# split data
	grade, tag = parseClass(raw)
	
	existing = select(c for c in db.Class if c.grade == grade and c.tag == tag)
	if existing.count() > 0:
		raise orm.core.ConstraintError('Class %s aready existing' % raw)
	
	db.Class(grade=grade, tag=tag)

def addClasses(raw: str):
	"""Add classes from a given raw string dump, assuming all students being
	separated by newlines. Each line is handled by addClass().
	"""
	for data in raw.split('\n'):
		if len(data) > 0:
			addClass(data)

def updateClass(id: int, grade: int, tag: str, teacher_id: int):
	# try to query class with grade and tag
	cs = select(c for c in db.Class if c.grade == grade and c.tag == tag)
	if cs.count() > 0:
		assert(cs.count() == 1)
		if cs.get().id != id:
			raise orm.core.ConstraintError('Ambiguous class %d%s' % (grade, tag))
	
	# update class
	c = db.Class[id]
	c.grade   = grade
	c.tag     = tag
	if teacher_id > 0:
		c.teacher = db.Teacher[teacher_id]
	else:
		c.teacher = None

# -----------------------------------------------------------------------------

def getStudentCount():
	"""Return total number of students.
	"""
	return db.Student.select().count()

def addStudent(raw: str):
	"""Add a new students from a given raw string dump, assuming all
	information being separated by tabs in the following order:
		Class, Name, FirstName
	Note that the Class must contain both, grade and tag (e.g. `08A` or
	`11ABC`). If a class does not exist, it needs to be added in the first
	place. Uppercase class tags are ignored.
	"""
	# split data
	data = raw.split('\t')
	grade, tag = parseClass(data[0])
	name, firstname = data[1], data[2]
	
	# query referenced class
	class_ = db.Class.get(grade=grade, tag=tag)
	
	try:
		# create actual student
		db.Student(person=db.Person(name=name, firstname=firstname), class_=class_)
	except ValueError as e:
		raise orm.core.ConstraintError(e)

def addStudents(raw: str):
	"""Add students from a given raw string dump, assuming all students being
	separated by newlines. Each line is handled by addStudent().
	"""
	for data in raw.split('\n'):
		if len(data) > 0:
			addStudent(data)

def getStudentsLike(name: str="", firstname: str=""):
	"""Return a list of students by name and firstname using partial matching.
	Both parameters default to an empty string if not specified.
	"""
	return select(s
		for s in db.Student
			if name.lower() in s.person.name.lower()
			and firstname.lower() in s.person.firstname.lower()
	).order_by(lambda s: s.person.firstname).order_by(lambda s: s.person.name).order_by(lambda s: s.class_.tag).order_by(lambda s: s.class_.grade)

# -----------------------------------------------------------------------------

def getTeacherCount():
	"""Return total number of teachers.
	"""
	return db.Teacher.select().count()

def getTeachers():
	"""Return all teachers sorted.
	"""
	return select(t for t in db.Teacher).order_by(lambda t: t.person.firstname).order_by(lambda t: t.person.name).order_by(lambda t: t.tag)

def addTeacher(raw: str):
	"""Add a new teacher from a given raw string dump, assuming all
	information being separated by tabs in the following order:
		Tag, Name, FirstName
	Uppercase tags are ignored.
	"""
	# split data
	data = raw.split('\t')
	tag, name, firstname = data[0], data[1], data[2]
	tag = tag.lower()
	
	try:
		# create actual teacher
		db.Teacher(person=db.Person(name=name, firstname=firstname), tag=tag)
	except ValueError as e:
		raise orm.core.ConstraintError(e)

def addTeachers(raw: str):
	"""Add teachers from a given raw string dump, assuming all teachers being
	separated by newlines. Each line is handled by addTeacher().
	"""
	for data in raw.split('\n'):
		if len(data) > 0:
			addTeacher(data)

# -----------------------------------------------------------------------------

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

	@staticmethod
	@db_session
	def prepare():
		# create teachers
		t1 = db.Teacher(
			person=db.Person(name='Glöckner', firstname='Christian'),
			tag='glö'
		)
		t2 = db.Teacher(
			person=db.Person(name='Thiele', firstname='Felix'),
			tag='thi'
		)
		
		# create some classes
		c1 = db.Class(grade=8, tag='a', teacher=t2)
		c2 = db.Class(grade=12, tag=t1.tag, teacher=t1)
		c3 = db.Class(grade=12, tag='lip')
		
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
	def test_getClassesCount(self):
		Tests.prepare()
		
		n = getClassesCount()
		self.assertEqual(n, 3)

	@db_session
	def test_addClasses_regular_case(self):
		Tests.prepare()
		
		raw = "10b\n05a\n12Foo\n\n"
		addClasses(raw)
		
		sds = list(db.Class.select())
		self.assertEqual(len(sds), 6)
		self.assertEqual(sds[3].grade, 10)
		self.assertEqual(sds[4].grade, 5)
		self.assertEqual(sds[5].grade, 12)
		self.assertEqual(sds[3].tag, 'b')
		self.assertEqual(sds[4].tag, 'a')
		self.assertEqual(sds[5].tag, 'foo')
		
	@db_session
	def test_addClasses_already_existing(self):
		Tests.prepare()
		
		raw = "10B\n08a\n12Foo\n\n"
		with self.assertRaises(orm.core.ConstraintError):
			addClasses(raw)

	@db_session
	def test_getStudentCount(self):
		Tests.prepare()
		
		n = getStudentCount()
		self.assertEqual(n, 3)

	@db_session
	def test_addStudents_for_existing_classes(self):
		Tests.prepare()
		
		raw = """08A	Schneider	Petra
12LIP	Mustermann	Thomas
"""
		addStudents(raw)
		
		sds = list(db.Student.select())
		self.assertEqual(len(sds), 5)
		self.assertEqual(sds[3].class_,    db.Class.get(grade=8, tag='a'))
		self.assertEqual(sds[4].class_,    db.Class.get(grade=12, tag='lip'))
		self.assertEqual(sds[3].person.name,      'Schneider')
		self.assertEqual(sds[3].person.firstname, 'Petra')
		self.assertEqual(sds[4].person.name,      'Mustermann')
		self.assertEqual(sds[4].person.firstname, 'Thomas')

	@db_session
	def test_addStudents_for_invalid_class(self):
		Tests.prepare()
		
		raw = """08A	Schneider	Petra
10C	Sonstwer	Beispiel
12LIP	Mustermann	Thomas
"""
		with self.assertRaises(orm.core.ConstraintError):
			addStudents(raw)
	
	@db_session
	def test_getTeacherCount(self):
		Tests.prepare()
		
		n = getTeacherCount()
		self.assertEqual(n, 2)

	@db_session
	def test_addTeachers_for_existing_classes(self):
		Tests.prepare()
		
		raw = """LIP	Lippmann	Iris
bsp	Beispiel	Peter

Mus	Mustermann	Max
"""
		addTeachers(raw)
		
		ts = list(db.Teacher.select())
		self.assertEqual(len(ts), 5)
		self.assertEqual(ts[2].tag, 'lip')
		self.assertEqual(ts[3].tag, 'bsp')
		self.assertEqual(ts[4].tag, 'mus')
		self.assertEqual(ts[2].person.name,      'Lippmann')
		self.assertEqual(ts[2].person.firstname, 'Iris')
		self.assertEqual(ts[3].person.name,      'Beispiel')
		self.assertEqual(ts[3].person.firstname, 'Peter')
		self.assertEqual(ts[4].person.name,      'Mustermann')
		self.assertEqual(ts[4].person.firstname, 'Max')

	@db_session
	def test_addTeachers_with_invalid_tag(self):
		Tests.prepare()
		
		raw = "glö	A	B"
		with self.assertRaises(orm.core.CacheIndexError):
			addTeachers(raw)
	
	@db_session
	def test_getClassGrades(self):
		Tests.prepare()
		
		gs = getClassGrades()
		self.assertEqual(len(gs), 2)
		self.assertIn(8, gs)
		self.assertIn(12, gs)
	
	@db_session
	def test_getClassTags(self):
		Tests.prepare()
		
		tgs = getClassTags(12)
		self.assertEqual(len(tgs), 2)
		self.assertIn('glö', tgs)
		self.assertIn('lip', tgs)

		tgs = getClassTags(8)
		self.assertEqual(len(tgs), 1)
		self.assertIn('a', tgs)

	@db_session
	def test_getClasses(self):
		Tests.prepare()
		
		cs = getClasses()
		self.assertEqual(len(cs), 3)
		self.assertIn(db.Class[1], cs)
		self.assertIn(db.Class[2], cs)
		self.assertIn(db.Class[3], cs)
	
	@db_session
	def test_getClassesByGrade(self):
		Tests.prepare()
		
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
		Tests.prepare()
		
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
		
		# search should ignore cases
		st = getStudentsLike(name='sch', firstname='A')
		self.assertEqual(len(st), 2)
		self.assertIn(db.Student[2], st)
		self.assertIn(db.Student[3], st)

	@db_session
	def test_advanceSchoolYear(self):
		Tests.prepare()
		
		db.Class(grade=7, tag='a')
		db.Class(grade=9, tag='a')
		
		# delete 12th grade students to avoid delete restriction
		delete(s for s in db.Class[2].student)
		delete(s for s in db.Class[3].student)
		
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

	@db_session
	def test_advanceMultipleSchoolYears(self):
		Tests.prepare()
		
		delete(s for s in db.Student) # clear students to avoid delete restriction
		
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


