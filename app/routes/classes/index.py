from bottle import *
from pony import orm

from app.db import db, db_session
from app.db import orga_queries as orga
from app.db import book_queries as books
from app.db import loan_queries as loans
from app.utils import errorhandler


@get('/classes')
@view('classes/class_index')
def class_index():
    return dict()


@get('/classes/<grade:int>')
@view('classes/grade_index')
def classes_grade_index(grade):
    return dict(grade=grade)


@get('/classes/<grade:int>/<tag>')
@view('classes/students_index')
def classes_students_index(grade, tag):
    bks = books.get_books_used_in(grade)
    bks = books.order_books_list(bks)
    bks.sort(key=lambda b: b.outGrade)
    c = orga.db.Class.get(grade=grade, tag=tag)
    if c is None:
        abort(404)
    return dict(grade=grade, tag=tag, books=bks, c=c)
