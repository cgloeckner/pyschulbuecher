#!/usr/bin/python3
# -*- coding: utf-8 -*-

from db.orm import db
from pony.orm import *
import unittest
from pony import orm

from db.orm import db, Currency


__author__ = "Christian Glöckner"


def getPublishers():
    """Return a list of all publishers.
    """
    return select(p
                  for p in db.Publisher
                  ).order_by(db.Publisher.name)


def getSubjects(elective=None):
    """Return a list of all subjects. If elective is provided, only elective
    or non-elective subjects are returned. If elective is not provided, all
    subjects are returned (default).
    """
    if elective is not None:
        ret = select(s
                     for s in db.Subject
                     if s.elective == elective
                     )
    else:
        ret = select(s
                     for s in db.Subject
                     )
    return ret.order_by(db.Subject.tag).order_by(db.Subject.elective)


def orderBooksIndex(bks):
    # 1st: subject, 2nd: inGrade, 3rd: title
    bks = list(bks.order_by(db.Book.title).order_by(db.Book.inGrade).order_by(db.Book.classsets))
    bks.sort(key=lambda b: b.subject.tag if b.subject is not None else '')
    return bks


def orderBooksList(bks):
    # 1st: subject, 2rd: title, 3rd: publisher
    bks = list(
        bks.order_by(
            lambda b: b.publisher.name).order_by(
            db.Book.title))
    bks.sort(key=lambda b: b.subject.tag if b.subject is not None else '')
    return bks


def getAllBooks():
    """Return a list of all books sorted by subject.tag, inGrade and title.
    """
    return select(b
                  for b in db.Book
                  )


def getBooksWithoutSubject():
    """Return a list of books which are not assigned to a specific subject.
    Those books are supposed to be used across subjects.
    """
    return select(b
                  for b in db.Book
                  if b.subject is None
                  )


def getBooksUsedIn(grade: int, booklist: bool = False):
    """Return a list of books which are used in the given grade.
    This includes books which are used across multiple grades, as well as books
    that are only used by this grade.
    The optional booklist parameter specifies if only books which are for loan
    are queried.
    """
    if booklist:
        return select(b
                      for b in db.Book
                      if b.inGrade <= grade
                      and grade <= b.outGrade
                      and b.for_loan
                      )
    else:
        return select(b
                      for b in db.Book
                      if b.inGrade <= grade
                      and grade <= b.outGrade
                      )


def getBooksStartedIn(grade: int, booklist: bool = False):
    """Return a list of books which are introduced in the given grade.
    This includes books which are used across multiple grades (from that grade)
    on, as well as books which are only used by this grade.
    The optional booklist parameter specifies if only books which are for loan
    are queried.
    """
    if booklist:
        return select(b
                      for b in db.Book
                      if b.inGrade == grade
                      and b.for_loan
                      )
    else:
        return select(b
                      for b in db.Book
                      if b.inGrade == grade
                      )


def getBooksFinishedIn(grade: int, booklist: bool = False):
    """Return a list of books which are used in the given grade for the last
    time. This includes books which are used across multiple grades (up to this
    grade), as well as books that are only used by this grade.
    The optional booklist parameter specifies if only books which are for loan
    are queried.
    """
    if booklist:
        return select(b
                      for b in db.Book
                      if b.outGrade == grade
                      and b.for_loan
                      )
    else:
        return select(b
                      for b in db.Book
                      if b.outGrade == grade
                      )


def getBooksByTitle(title: str):
    """Return a list of books with similar titles.
    """
    return select(b
                  for b in db.Book
                  if title in b.title
                  )


def getBooksByIsbn(isbn: str):
    """Returns a list of books with this exact isbn.
    Note that most commonly, only one or none will be returned. If an empty
    string is given as isbn, all books without isbn are returned. Note that
    this is mostly used for books which are not longer available in market.
    """
    return select(b
                  for b in db.Book
                  if isbn == b.isbn
                  )


def getRealBooks():
    """Return a list of all real books (which are no workbooks).
    """
    return select(b
                  for b in db.Book
                  if not b.workbook
                  )


def getRealBooksBySubject(subject: db.Subject, classsets: bool):
    """Returns a list of books used in the given subject. If classsets is
    provided with `false`, now classset books are included.
    Note that only real books (no workbooks) are queried
    """
    if classsets:
        return select(b
                      for b in db.Book
                      if not b.workbook
                      and b.subject == subject
                      )
    else:
        return select(b
                      for b in db.Book
                      if not b.workbook
                      and b.subject == subject
                      and not b.classsets
                      )


def getRealBooksByGrade(grade: int, classsets: bool):
    """Returns a list of books used in the given grade. If classsets is
    provided with `false`, now classset books are included.
    Note that only real books (no workbooks) are queried
    """
    if classsets:
        return select(b
                      for b in db.Book
                      if not b.workbook
                      and b.inGrade <= grade
                      and grade <= b.outGrade
                      )
    else:
        return select(b
                      for b in db.Book
                      if not b.workbook
                      and b.inGrade <= grade
                      and grade <= b.outGrade
                      and not b.classsets
                      )


def getWorkbooksBySubject(subject: db.Subject):
    """Returns a list of workbooks used in the given subject."""
    return select(b
                  for b in db.Book
                  if b.workbook
                  and b.subject == subject
                  )


def getClasssetsBySubject(subject: db.Subject):
    """Returns a list of workbooks used in the given subject."""
    return select(b
                  for b in db.Book
                  if not b.workbook
                  and b.classsets
                  and b.subject == subject
                  )

# -----------------------------------------------------------------------------


def addSubjects(raw: str):
    """Add subjects from a given raw string dump, assuming subjects being
    separated by newlines. Name and tag are assumed to be separated by a tab.
    A new subject is declared as non-elective by default.
    """
    for data in raw.split("\n"):
        res = data.split("\t")
        assert(len(res) == 2)
        db.Subject(name=res[0], tag=res[1])


def addPublishers(raw: str):
    """Add publishers from a given raw string dump, assuming publishers being
    separated by newlines
    """
    for data in raw.split("\n"):
        db.Publisher(name=data)


def addBook(raw: str):
    """Add book from a given raw string dump, assuming all information being
    separated by tabs in the following order:
        Title, ISBN, Price, Publisher, inGrade, outGrade
    Optional: Subject, Novices, Advanced, Workbook, Classsets, Comment
    Earlier optional data must be provided (at least as empty strings) if a
    later parameter is given.
    Note that the stock is always set to zero and must be specified later.
    """
    # split data
    data = raw.split('\t')
    title, isbn, price, publisher, inGrade, outGrade = data[:6]
    subject = data[6] if 6 < len(data) else ""
    novices = data[7] if 7 < len(data) else ""
    advanced = data[8] if 8 < len(data) else ""
    workbook = data[9] if 9 < len(data) else ""
    classsets = data[10] if 10 < len(data) else ""
    for_loan = data[11] if 11 < len(data) else ""
    comment = data[12] if 12 < len(data) else ""

    # fix parameters
    try:
        price = Currency.fromString(price) if price != "" else None
        inGrade = int(inGrade)
        outGrade = int(outGrade)
    except ValueError as e:
        raise orm.core.ConstraintError(e)

    # interpret boolean values (based on entity's default values)
    novices = True if novices == 'True' else False
    advanced = True if advanced == 'True' else False
    workbook = True if workbook == 'True' else False
    classsets = True if classsets == 'True' else False
    for_loan = False if for_loan == 'False' else True

    # query referenced entities
    publisher = db.Publisher.get(name=publisher)
    subject = db.Subject.get(tag=subject) if subject != "" else None

    try:
        # create actual book
        db.Book(
            title=title,
            isbn=isbn,
            price=price,
            publisher=publisher,
            inGrade=inGrade,
            outGrade=outGrade,
            subject=subject,
            novices=novices,
            advanced=advanced,
            workbook=workbook,
            classsets=classsets,
            for_loan=for_loan,
            comment=comment)
    except ValueError as e:
        raise orm.core.ConstraintError(e)


def addBooks(raw: str):
    """Add books from a given raw string dump, assuming all books being
    separated by newlines. Each line is handled by addBook().
    """
    for data in raw.split('\n'):
        if len(data) > 0:
            addBook(data)


# -----------------------------------------------------------------------------


class Tests(unittest.TestCase):

    @staticmethod
    @db_session
    def prepare():
        # create subjects
        db.Subject(name='Mathematics', tag='Ma')
        db.Subject(name='Russian', tag='Ru')
        db.Subject(name='English', tag='Eng')
        db.Subject(name='Spanish', tag='Spa')
        db.Subject[2].elective = True
        db.Subject[4].elective = True

        # create publishers
        db.Publisher(name='Cornelsen')
        db.Publisher(name='Klett')

        # create maths books
        db.Book(title='Maths II', isbn='001-021', price=2999,
                publisher=db.Publisher[1], inGrade=7, outGrade=8,
                subject=db.Subject[1])
        db.Book(title='Maths I', isbn='000-001', price=2495,
                publisher=db.Publisher[1], inGrade=5, outGrade=6,
                subject=db.Subject[1])
        db.Book(title='Maths III', isbn='914-721', price=3499,
                publisher=db.Publisher[1], inGrade=9, outGrade=10,
                subject=db.Subject[1])
        db.Book(
            title='Basic Maths',
            publisher=db.Publisher[1],
            inGrade=11,
            outGrade=12,
            subject=db.Subject[1],
            novices=True,
            classsets=True,
            for_loan=False)
        db.Book(
            title='Advanced Maths',
            publisher=db.Publisher[1],
            inGrade=11,
            outGrade=12,
            subject=db.Subject[1],
            advanced=True,
            classsets=True)

        # create russian books
        db.Book(title='Privjet', isbn='49322-6346', price=5999,
                publisher=db.Publisher[2], inGrade=5, outGrade=10,
                subject=db.Subject[2])
        db.Book(title='Dialog', isbn='43623-8485', price=7999,
                publisher=db.Publisher[2], inGrade=11, outGrade=12,
                subject=db.Subject[2], novices=True, advanced=True)

        # create subject-independent books
        db.Book(title='Formulary', isbn='236-7634-62', price=2295,
                publisher=db.Publisher[1], inGrade=7, outGrade=12)

        # create english book
        db.Book(title='English 5th grade', publisher=db.Publisher[2],
                inGrade=5, outGrade=5, subject=db.Subject[3], classsets=True,
                for_loan=False)

    def setUp(self):
        db.create_tables()

    def tearDown(self):
        db.drop_all_tables(with_all_data=True)

    @db_session
    def test_getPublishers(self):
        Tests.prepare()

        ps = getPublishers()
        self.assertEqual(len(ps), 2)
        self.assertIn(db.Publisher[1], ps)
        self.assertIn(db.Publisher[2], ps)

    @db_session
    def test_getSubjects(self):
        Tests.prepare()

        sb = getSubjects()
        self.assertEqual(len(sb), 4)
        self.assertIn(db.Subject[1], sb)
        self.assertIn(db.Subject[3], sb)
        self.assertIn(db.Subject[2], sb)
        self.assertIn(db.Subject[4], sb)

        sb = getSubjects(elective=False)
        self.assertEqual(len(sb), 2)
        self.assertIn(db.Subject[1], sb)
        self.assertIn(db.Subject[3], sb)

        sb = getSubjects(elective=True)
        self.assertEqual(len(sb), 2)
        self.assertIn(db.Subject[2], sb)
        self.assertIn(db.Subject[4], sb)

    @db_session
    def test_orderBooksIndex(self):
        Tests.prepare()

        bks = db.Book.select()
        bks = orderBooksIndex(bks)
        self.assertEqual(bks[0], db.Book[8])
        self.assertEqual(bks[1], db.Book[9])
        self.assertEqual(bks[2], db.Book[2])
        self.assertEqual(bks[3], db.Book[1])
        self.assertEqual(bks[4], db.Book[3])
        self.assertEqual(bks[5], db.Book[5])
        self.assertEqual(bks[6], db.Book[4])
        self.assertEqual(bks[7], db.Book[6])
        self.assertEqual(bks[8], db.Book[7])

    @db_session
    def test_orderBooksList(self):
        Tests.prepare()

        bks = db.Book.select()
        bks = orderBooksList(bks)
        self.assertEqual(bks[0], db.Book[8])
        self.assertEqual(bks[1], db.Book[9])
        self.assertEqual(bks[2], db.Book[5])
        self.assertEqual(bks[3], db.Book[4])
        self.assertEqual(bks[4], db.Book[2])
        self.assertEqual(bks[5], db.Book[1])
        self.assertEqual(bks[6], db.Book[3])
        self.assertEqual(bks[7], db.Book[7])
        self.assertEqual(bks[8], db.Book[6])

    @db_session
    def test_getAllBooks(self):
        Tests.prepare()

        bs = set(getAllBooks())
        self.assertEqual(len(bs), 9)
        self.assertIn(db.Book[8], bs)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[1], bs)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)
        self.assertIn(db.Book[9], bs)

    @db_session
    def test_getBooksWithoutSubject(self):
        Tests.prepare()

        bs = getBooksWithoutSubject()
        self.assertEqual(len(bs), 1)
        self.assertIn(db.Book[8], bs)

    @db_session
    def test_getBooksUsedIn(self):
        Tests.prepare()

        bs = getBooksUsedIn(5)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[9], bs)

        bs = getBooksUsedIn(5, booklist=True)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)

        bs = getBooksUsedIn(6)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)

        bs = getBooksUsedIn(7)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[1], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[8], bs)

        bs = getBooksUsedIn(10)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[8], bs)

        bs = getBooksUsedIn(11)
        self.assertEqual(len(bs), 4)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

        bs = getBooksUsedIn(11, booklist=True)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

        bs = getBooksUsedIn(13)
        self.assertEqual(len(bs), 0)

    @db_session
    def test_getBooksStartedIn(self):
        Tests.prepare()

        bs = getBooksStartedIn(5)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)
        self.assertIn(db.Book[9], bs)

        bs = getBooksStartedIn(5, booklist=True)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[6], bs)

        bs = getBooksStartedIn(6)
        self.assertEqual(len(bs), 0)

        bs = getBooksStartedIn(7)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[1], bs)
        self.assertIn(db.Book[8], bs)

        bs = getBooksStartedIn(11)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)

        bs = getBooksStartedIn(11, booklist=True)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)

    @db_session
    def test_getBooksFinishedIn(self):
        Tests.prepare()

        bs = getBooksFinishedIn(5)
        self.assertEqual(len(bs), 1)
        self.assertIn(db.Book[9], bs)

        bs = getBooksFinishedIn(5, booklist=True)
        self.assertEqual(len(bs), 0)

        bs = getBooksFinishedIn(6)
        self.assertEqual(len(bs), 1)
        self.assertIn(db.Book[2], bs)

        bs = getBooksFinishedIn(10)
        self.assertEqual(len(bs), 2)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[6], bs)

        bs = getBooksFinishedIn(12)
        self.assertEqual(len(bs), 4)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

        bs = getBooksFinishedIn(12, booklist=True)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

    @db_session
    def test_getBooksByTitle(self):
        Tests.prepare()

        bs = getBooksByTitle('Maths')
        self.assertEqual(len(bs), 5)
        self.assertIn(db.Book[2], bs)
        self.assertIn(db.Book[1], bs)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)

    @db_session
    def test_getBooksByIsbn(self):
        Tests.prepare()

        # single book
        bs = getBooksByIsbn('236-7634-62')
        self.assertEqual(len(bs), 1)
        self.assertIn(db.Book[8], bs)

        # all not yet available books
        bs = getBooksByIsbn('')
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[9], bs)

    @db_session
    def test_getRealBooks(self):
        Tests.prepare()

        # make some books become workbooks / classsets
        db.Book[2].workbook = True
        db.Book[7].workbook = True
        db.Book[4].classsets = True
        db.Book[5].classsets = False

        # query real books
        bs = getRealBooks()
        self.assertEqual(len(bs), 7)
        self.assertIn(db.Book[1], bs)
        self.assertNotIn(db.Book[2], bs)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertIn(db.Book[6], bs)
        self.assertNotIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)
        self.assertIn(db.Book[9], bs)

        # query real books by subject (including classsets)
        bs = getRealBooksBySubject(db.Subject[1], True)
        self.assertEqual(len(bs), 4)
        self.assertIn(db.Book[1], bs)
        self.assertNotIn(db.Book[2], bs)
        self.assertIn(db.Book[3], bs)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)

        # query real books by subject (without classsets)
        bs = getRealBooksBySubject(db.Subject[1], False)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[1], bs)
        self.assertNotIn(db.Book[2], bs)
        self.assertIn(db.Book[3], bs)
        self.assertNotIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)

        # query real books by grade (with classets)
        bs = getRealBooksByGrade(11, True)
        self.assertEqual(len(bs), 3)
        self.assertIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertNotIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

        # query real books by grade (without classets)
        bs = getRealBooksByGrade(11, False)
        self.assertEqual(len(bs), 2)
        self.assertNotIn(db.Book[4], bs)
        self.assertIn(db.Book[5], bs)
        self.assertNotIn(db.Book[7], bs)
        self.assertIn(db.Book[8], bs)

    @db_session
    def test_getWorkbooks(self):
        Tests.prepare()

        # make some books become workbooks / classsets
        db.Book[2].workbook = True
        db.Book[3].workbook = True

        # query math workbooks
        wb = getWorkbooksBySubject(db.Subject[1])
        self.assertEqual(len(wb), 2)
        self.assertIn(db.Book[2], wb)
        self.assertIn(db.Book[3], wb)

    @db_session
    def test_getClassSets(self):
        Tests.prepare()

        # query math classets
        cb = getClasssetsBySubject(db.Subject[1])
        self.assertEqual(len(cb), 2)
        self.assertIn(db.Book[4], cb)
        self.assertIn(db.Book[5], cb)

    @db_session
    def test_addSubjects(self):
        raw = """Mathematik\tMa
Englisch\tEng
Deutsch\tDe
Sport\tSp"""
        addSubjects(raw)

        s = select(s.name for s in db.Subject)
        self.assertEqual(len(s), 4)
        self.assertIn("Mathematik", s)
        self.assertIn("Englisch", s)
        self.assertIn("Deutsch", s)
        self.assertIn("Sport", s)

    @db_session
    def test_addPublishers(self):
        raw = """Cornelsen
Klett
Volk & Wissen
C.C. Buchner"""
        addPublishers(raw)

        p = select(s.name for s in db.Publisher)
        self.assertEqual(len(p), 4)
        self.assertIn("Cornelsen", p)
        self.assertIn("Klett", p)
        self.assertIn("Volk & Wissen", p)
        self.assertIn("C.C. Buchner", p)

    @db_session
    def test_canAddBookWithFullInformation(self):
        addSubjects("Mathematik\tMa")
        addPublishers("Klett")

        raw = "Mathematik Live\t0815-1234\t23,95 €\tKlett\t11\t12\tMa\tTrue\tFalse\tFalse\tFalse\tFalse\tLehrbuch"
        addBook(raw)

        b = db.Book[1]
        self.assertEqual(b.title, "Mathematik Live")
        self.assertEqual(b.isbn, "0815-1234")
        self.assertEqual(b.price, 2395)
        self.assertEqual(b.publisher, db.Publisher[1])
        self.assertEqual(b.inGrade, 11)
        self.assertEqual(b.outGrade, 12)
        self.assertEqual(b.subject, db.Subject[1])
        self.assertTrue(b.novices)
        self.assertFalse(b.advanced)
        self.assertFalse(b.workbook)
        self.assertFalse(b.classsets)
        self.assertFalse(b.for_loan)
        self.assertEqual(b.comment, "Lehrbuch")

    @db_session
    def test_canAddBookWithMinimalInformation(self):
        addPublishers("Klett")

        raw = "Das Große Tafelwerk\t\t\tKlett\t7\t12\t\t\t\t\t\t\t"
        addBook(raw)

        b = db.Book[1]
        self.assertEqual(b.title, "Das Große Tafelwerk")
        self.assertEqual(b.isbn, "")
        self.assertEqual(b.price, None)
        self.assertEqual(b.publisher, db.Publisher[1])
        self.assertEqual(b.inGrade, 7)
        self.assertEqual(b.outGrade, 12)
        self.assertFalse(b.novices)
        self.assertFalse(b.advanced)
        self.assertTrue(b.for_loan)

    @db_session
    def test_addBooks(self):
        addPublishers("Klett\nCornelsen")
        addSubjects("Mathemati\tMa\nEnglisch\tEng")

        ma = db.Subject.get(tag="Ma")
        eng = db.Subject.get(tag="Eng")

        raw = """Mathematik Live\t0815-1234\t23,95\tKlett\t11\t12\tMa\tTrue\tFalse\tFalse\tFalse\tTrue\t
Tafelwerk\t12-52-6346\t19,99\tKlett\t7\t12\t\tFalse\tFalse\tFalse\tFalse\tfächerübergreifend
Englisch Oberstufe\t433-5213-6246\t49,95\tCornelsen\t11\t12\tEng\tTrue\tTrue\tFalse\tFalse\tTrue\t
Das Große Tafelwerk\t\t\tKlett\t7\t12\t\tFalse\tFalse\tFalse\tFalse\tTrue\tfächerübergreifend"""

        addBooks(raw)

        b1 = db.Book[1]
        b2 = db.Book[2]
        b3 = db.Book[3]
        b4 = db.Book[4]

        self.assertEqual(b1.title, "Mathematik Live")
        self.assertEqual(b2.title, "Tafelwerk")
        self.assertEqual(b3.title, "Englisch Oberstufe")
        self.assertEqual(b4.title, "Das Große Tafelwerk")
        self.assertEqual(b1.subject, ma)
        self.assertEqual(b2.subject, None)
        self.assertEqual(b3.subject, eng)
        self.assertTrue(b3.novices)
        self.assertTrue(b3.advanced)
