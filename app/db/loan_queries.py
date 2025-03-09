import datetime

from app.db.orm import *

from pony.orm import *


def order_loan_overview(loans):
    # 1st: outGrade, 2nd: subject, 3rd: title
    loans = list(loans.order_by(lambda l: l.book.title))
    loan_queries.sort(key=lambda l: l.person.firstname)
    loan_queries.sort(key=lambda l: l.person.name)
    loan_queries.sort(
        key=lambda l: l.book.subject.tag if l.book.subject is not None else '')
    loan_queries.sort(key=lambda l: l.book.outGrade)
    loan_queries.sort(key=lambda l: l.person.student.class_.tag if l.person.student is not None and l.person.student.class_ is not None else '')
    loan_queries.sort(
        key=lambda l: l.person.student.class_.grade if l.person.student is not None and l.person.student.class_ is not None else -
        1)
    return loans


def order_request_overview(requests):
    # 1st: outGrade, 2nd: subject, 3rd: title
    requests = list(requests.order_by(lambda r: r.book.title))
    requests.sort(
        key=lambda r: r.book.subject.tag if r.book.subject is not None else '')
    requests.sort(key=lambda r: r.book.outGrade)
    return requests


def get_expected_returns(student: db.Student):
    """Returns a list of loans which are expected to be returned referring
    the student's current grade.
    """
    return select(l
                  for l in db.Loan
                  if l.person == student.person
                  and l.book.outGrade <= student.class_.grade
                  )


def is_requested(student: db.Student, book: db.Book):
    """Returns whether the given book is requested by the given student.
    """
    for r in student.person.request:
        if r.book == book:
            return True
    return False


def get_request_count(person: db.Person, book: db.Book):
    """Returns whether the given book is requested by the given person.
    """
    for r in person.request:
        if r.book == book:
            return 1
    return 0


def update_request(student: db.Student, book: db.Book, status: bool):
    """Update request status for the given book and the given student. If True
    is provided, a request object is created. If not, no request object exists
    for that student to that book.
    """
    was = is_requested(student, book)
    if not was and status:
        # new request
        db.Request(person=student.person, book=book)
    elif was and not status:
        # delete request
        r = db.app.request.get(person=student.person, book=book)
        r.delete()
    # else: nothing to update


def add_loan(person: db.Person, book: db.Book, count: int):
    """Add the given number of books to the given person's loaning."""
    l = db.Loan.get(person=person, book=book)
    if l is None and count > 0:
        # create new loan
        db.Loan(person=person, book=book, given=datetime.date.today(), count=count)
    elif l is not None:
        # update it
        l.count += count


def update_loan(person: db.Person, book: db.Book, count: int):
    """Update the loan status for the given book and the given person. If the
    count is set to zero, the loan object is deleted from the database.
    Otherwise the loan object is updated. If no such object exists, it will be
    created as needed.
    """
    l = db.Loan.get(person=person, book=book)
    if l is None and count > 0:
        # create new loan
        db.Loan(person=person, book=book, given=datetime.date.today(), count=count)
    elif l is not None:
        if count == 0:
            # delete loan
            l.delete()
        else:
            # update it
            l.count = count


def get_loan_count(person: db.Person, book: db.Book):
    """Return number of this specific book, either loaned by that person
    or all together.
    """
    if person is not None:
        # determine loan count
        for l in person.loan:
            if l.book == book:
                return l.count
        return 0

    else:
        # determine total loan count for all persons
        return sum(l.count for l in db.Loan if l.book == book)


def query_loans_by_book(book: db.Book):
    """Return a list of persons who loan that book.
    """
    loans = select(l for l in db.Loan if l.book == book)
    if loans is None:
        loans = list()
    else:
        loans = order_loan_overview(loans)
    return loans


def apply_request(student: db.Student):
    """Apply person's request be transfering to loaning these book_queries.
    Note that the requests are deleted after that.
    """
    # add loaning
    bks = list()
    for l in student.person.request:
        if l.book.inGrade == 0:
            # ignore special books
            l.delete()
        else:
            update_loan(student.person, l.book, 1)
            bks.append(l.book)

    # drop as requests
    for b in bks:
        update_request(student, b, False)
