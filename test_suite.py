#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Christian Glöckner"

import unittest

from database import classes, persons, publishers, students, subjects, teachers

def register(suite, class_):
	"""Register all testcase methods of the given test case class to the given
	suite
	"""
	for method in dir(class_):
		if method.startswith('test_'):
			suite.addTest(class_(method))

def suite():
	"""Create whole test suite
	"""
	suite = unittest.TestSuite()
	register(suite, classes.CRUDTest)
	register(suite, persons.CRUDTest)
	register(suite, publishers.CRUDTest)
	register(suite, students.CRUDTest)
	register(suite, subjects.CRUDTest)
	register(suite, teachers.CRUDTest)
	return suite

if __name__ == '__main__':
	runner = unittest.TextTestRunner()
	runner.run(suite())
