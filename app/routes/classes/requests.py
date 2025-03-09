from bottle import *
from pony import orm

from app.db import db, db_session
from app.db import orga_queries as orga
from app.db import book_queries as books
from app.db import loan_queries as loans
from app.utils import errorhandler



@get('/classes/requests/<grade:int>/<tag>/<version>')
@view('classes/request_form')
def classes_requests_form(grade, tag, version):
    query_grade = grade
    if 'next' in version:
        query_grade += 1

    # query grade-specific books
    if tag.lower() == 'neu' or 'full' in version:
        bks = books.get_books_used_in(query_grade, True)
    else:
        bks = books.get_books_started_in(query_grade, True)
    # order queried books
    bks = books.order_books_list(bks)

    # add misc books
    bks += list(books.get_books_used_in(0, True))
    c = orga.db.Class.get(grade=grade, tag=tag)
    if c is None:
        abort(404)

    return dict(grade=grade, tag=tag, books=bks, c=c, version=version)


@post('/classes/requests/<grade:int>/<tag>/<version>')
@errorhandler
def classes_requests_post(grade, tag, version):
    query_grade = grade
    if 'next' in version:
        query_grade += 1

    # query grade-specific books
    if tag.lower() == 'neu' or 'full' in version:
        bks = books.get_books_used_in(query_grade, True)
    else:
        bks = books.get_books_started_in(query_grade, True)
    # order queried books
    bks = books.order_books_list(bks)

    # add misc books
    bks += list(books.get_books_used_in(0, True))
    for s in orga.get_students_in(grade, tag):
        for b in bks:
            key = "%d_%d" % (s.id, b.id)
            status = request.forms.get(key) == 'on'
            loans.update_request(s, b, status)

    db.commit()
    redirect('/classes/%d' % (grade))
