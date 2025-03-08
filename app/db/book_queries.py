from app.db.orm import *

from pony.orm import *
from pony import orm


def get_publishers():
    """Return a list of all publishers.
    """
    return select(p for p in db.Publisher).order_by(db.Publisher.name)


def get_subjects(elective=None):
    """Return a list of all subjects. If elective is provided, only elective
    or non-elective subjects are returned. If elective is not provided, all
    subjects are returned (default).
    """
    if elective is not None:
        ret = select(s for s in db.Subject if s.elective == elective)
    else:
        ret = select(s for s in db.Subject)
    return ret.order_by(db.Subject.tag).order_by(db.Subject.elective)


def order_books_index(bks):
    # 1st: subject, 2nd: inGrade, 3rd: title
    bks = list(bks.order_by(db.Book.title).order_by(db.Book.inGrade).order_by(db.Book.classsets))
    bks.sort(key=lambda b: b.subject.tag if b.subject is not None else '')
    return bks


def order_books_list(bks):
    # 1st: subject, 2rd: title, 3rd: publisher
    bks = list(
        bks.order_by(lambda b: b.publisher.name).order_by(db.Book.title))
    bks.sort(key=lambda b: b.subject.tag if b.subject is not None else '')
    bks.sort(key=lambda b: b.subject.elective if b.subject is not None else False)
    return bks


def get_all_books():
    """Return a list of all books sorted by subject.tag, inGrade and title.
    """
    return select(b for b in db.Book)


def get_books_without_subject():
    """Return a list of books which are not assigned to a specific subject.
    Those books are supposed to be used across subjects.
    """
    return select(b for b in db.Book if b.subject is None)


def get_books_used_in(grade: int, booklist: bool = False):
    """Return a list of books which are used in the given grade.
    This includes books which are used across multiple grades, as well as books
    that are only used by this grade.
    The optional booklist parameter specifies if only books which are for loan
    are queried.
    """
    if booklist:
        return select(
            b for b in db.Book if b.inGrade <= grade
            and grade <= b.outGrade and b.for_loan
        )
    else:
        return select(b for b in db.Book if b.inGrade <= grade and grade <= b.outGrade)


def get_books_started_in(grade: int, booklist: bool = False):
    """Return a list of books which are introduced in the given grade.
    This includes books which are used across multiple grades (from that grade)
    on, as well as books which are only used by this grade.
    The optional booklist parameter specifies if only books which are for loan
    are queried.
    """
    if booklist:
        return select(b for b in db.Book if b.inGrade == grade and b.for_loan)
    else:
        return select(b for b in db.Book if b.inGrade == grade)


def get_books_finished_in(grade: int, booklist: bool = False):
    """Return a list of books which are used in the given grade for the last
    time. This includes books which are used across multiple grades (up to this
    grade), as well as books that are only used by this grade.
    The optional booklist parameter specifies if only books which are for loan
    are queried.
    """
    if booklist:
        return select(b for b in db.Book if b.outGrade == grade and b.for_loan)
    else:
        return select(b for b in db.Book if b.outGrade == grade)


def get_books_by_title(title: str):
    """Return a list of books with similar titles.
    """
    return select(b for b in db.Book if title in b.title)


def get_books_by_isbn(isbn: str):
    """Returns a list of books with this exact isbn.
    Note that most commonly, only one or none will be returned. If an empty
    string is given as isbn, all books without isbn are returned. Note that
    this is mostly used for books which are not longer available in market.
    """
    return select(b for b in db.Book if isbn == b.isbn)


def get_real_books():
    """Return a list of all real books (which are no workbooks).
    """
    return select(b for b in db.Book if not b.workbook)


def get_real_books_by_subject(subject: db.Subject, classsets: bool):
    """Returns a list of books used in the given subject. If classsets is
    provided with `false`, now classset books are included.
    Note that only real books (no workbooks) are queried
    """
    if classsets:
        return select(b for b in db.Book if not b.workbook and b.subject == subject)
    else:
        return select(b for b in db.Book if not b.workbook and b.subject == subject and not b.classsets)


def get_real_books_by_grade(grade: int, classsets: bool):
    """Returns a list of books used in the given grade. If classsets is
    provided with `false`, now classset books are included.
    Note that only real books (no workbooks) are queried
    """
    if classsets:
        return select(b for b in db.Book if not b.workbook and b.inGrade <= grade and grade <= b.outGrade)
    else:
        return select(
            b for b in db.Book
            if not b.workbook and b.inGrade <= grade and grade <= b.outGrade and not b.classsets
        )


def get_workbooks_by_subject(subject: db.Subject):
    """Returns a list of workbooks used in the given subject."""
    return select(b for b in db.Book if b.workbook and b.subject == subject)


def get_classsets_by_subject(subject: db.Subject):
    """Returns a list of workbooks used in the given subject."""
    return select(b for b in db.Book if not b.workbook and b.classsets and b.subject == subject)

# -----------------------------------------------------------------------------


def add_subjects(raw: str):
    """Add subjects from a given raw string dump, assuming subjects being
    separated by newlines. Name and tag are assumed to be separated by a tab.
    A new subject is declared as non-elective by default.
    """
    for data in raw.split("\n"):
        res = data.split("\t")
        assert(len(res) == 2)
        db.Subject(name=res[0], tag=res[1])


def add_publishers(raw: str):
    """Add publishers from a given raw string dump, assuming publishers being
    separated by newlines
    """
    for data in raw.split("\n"):
        db.Publisher(name=data)


def add_book(raw: str):
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
        price = Currency.from_string(price) if price != "" else None
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
            comment=comment
        )
    except ValueError as e:
        raise orm.core.ConstraintError(e)


def add_books(raw: str):
    """Add books from a given raw string dump, assuming all books being
    separated by newlines. Each line is handled by add_book().
    """
    for data in raw.split('\n'):
        if len(data) > 0:
            add_book(data)
