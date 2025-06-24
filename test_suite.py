#!/usr/bin/python3
# -*- coding: utf-8 -*-

import locale

__author__ = "Christian Glöckner"

import unittest

from app.db import orga_queries, book_queries, loan_queries

import test.db.orm as orm
import test.db.utils as utils
import test.admin as admin_routes
import test.classes as classes_routes
import test.loans as loans_routes


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
    register(suite, orm.Tests)
    register(suite, orga_queries.Tests)
    register(suite, book_queries.Tests)
    register(suite, loan_queries.Tests)
    register(suite, utils.Tests)
    register(suite, admin_routes.Tests)
    register(suite, classes_routes.Tests)
    register(suite, loans_routes.Tests)
    return suite


if __name__ == '__main__':
    orm.db.bind('sqlite', ':memory:', create_db=True)
    orm.db.generate_mapping(create_tables=True)

    runner = unittest.TextTestRunner()
    runner.run(suite())
