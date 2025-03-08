#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app.db import db, db_session
from pony.orm import *
import unittest

from app.tex import *
from app.xls import *


class Tests(unittest.TestCase):

    @staticmethod
    @db_session
    def prepare():
        import db.orga
        import db.books
        import db.orga

        db.orga.Tests.prepare()
        db.books.Tests.prepare()

    def setUp(self):
        db.create_tables()

    def tearDown(self):
        db.drop_all_tables(with_all_data=True)

    @db_session
    def test_create_custom_booklist(self):
        # create custom database content (real world example)
        books.add_subjects(
            "Mathematik\tMa\nDeutsch\tDe\nEnglisch\tEn\nPhysik\tPh")
        books.add_publishers("Klett\nCornelsen")
        books.add_books(
            """Ein Mathe-Buch\t978-3-7661-5000-4\t32,80 €\tCornelsen\t5\t12\tMa\tTrue\tTrue\tFalse\tFalse\tTrue
Mathe AH\t978-3-7661-5007-3\t8,80 €\tCornelsen\t5\t12\tMa\tTrue\tTrue\tTrue\tFalse\tTrue
Deutsch-Buch mit sehr langam Titel und damit einigen Zeilenumbrüchen .. ach und Umlaute in größeren Mengen öÖäÄüÜß sowie Sonderzeichen !"§$%&/()=?.:,;-_@\t978-3-12-104104-6\t35,95 €\tKlett\t11\t12\tDe\tTrue\tTrue\tFalse\tFalse\tTrue
Old English Book\t\t\tKlett\t5\t12\tEn\tTrue\tTrue\tFalse\tTrue\tTrue
Grundlagen der Physik\t\t\tCornelsen\t5\t12\tPh\tTrue\tTrue\tFalse\tFalse\tTrue
Tafelwerk\t978-3-06-001611-2\t13,50 €\tCornelsen\t7\t12\tFalse\tFalse\tFalse\tFalse\tTrue""")

        exclude = set()
        exclude.add('11_1')  # "Ein Mathe-Buch"

        # create booklist
        with open('settings.ini') as h:
            booklist = BooklistPdf(h, export='/tmp/export')
        booklist(11, new_students=True, exclude=exclude)
        print('PLEASE MANUALLY VIEW /tmp/export/Buecherzettel11.pdf')

    @db_session
    def test_create_custom_requestlist(self):
        Tests.prepare()

        # create custom database content (real world example)
        books.add_subjects("Deutsch\tDe\nPhysik\tPh")
        books.add_books(
            """Ein Mathe-Buch\t978-3-7661-5000-4\t32,80 €\tCornelsen\t5\t12\tMa\tTrue\tTrue\tFalse\tFalse\tTrue
Mathe AH\t978-3-7661-5007-3\t8,80 €\tCornelsen\t5\t12\tMa\tTrue\tTrue\tTrue\tFalse\tTrue
Deutsch-Buch mit sehr langam Titel und damit einigen Zeilenumbrüchen .. ach und Umlaute in größeren Mengen öÖäÄüÜß sowie Sonderzeichen !"§$%&/()=?.:,;-_@\t978-3-12-104104-6\t35,95 €\tKlett\t11\t12\tDe\tTrue\tTrue\tFalse\tFalse\tTrue
Old English Book\t\t\tKlett\t5\t12\tEn\tTrue\tTrue\tFalse\tTrue\tTrue
Grundlagen der Physik\t\t\tCornelsen\t5\t12\tPh\tTrue\tTrue\tFalse\tFalse\tTrue
Tafelwerk\t978-3-06-001611-2\t13,50 €\tCornelsen\t7\t12\tFalse\tFalse\tFalse\tFalse\tTrue""")

        # create requestlists
        with open('settings.ini') as h:
            requestlist = RequestlistPdf(h, export='/tmp/export')
        for c in select(c for c in db.Class):
            requestlist(c)
        requestlist.saveToFile()

        print('PLEASE MANUALLY VIEW /tmp/export/Erfassungsliste.pdf')
