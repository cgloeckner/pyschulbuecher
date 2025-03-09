from bottle import *
from pony import orm

from app import db, db_session, errorhandler
from app.db import orga_queries as orga
from app.db import book_queries as books
from app.db import loan_queries as loans


@get('/loan/ajax/books')
@view('loan/book_list')
def loan_ajax_queryBooks():
    classsets = request.query.classsets != "false"
    value = request.query.value
    if value != '':
        value = int(value)
    else:
        value = None

    person = db.Person[int(request.query.person_id)]
    if request.query.by == 'subject':
        subject = db.Subject[value] if value is not None else None
        bks = books.get_real_books_by_subject(subject, classsets)
    else:
        bks = books.get_real_books_by_grade(value, classsets)

    bks = books.order_books_index(bks)
    return dict(person=person, bks=bks)
