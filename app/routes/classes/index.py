import bottle

from app.db import db, db_session
from app.db import orga_queries
from app.db import book_queries
from app.db import loan_queries
from app.utils import errorhandler


app = bottle.default_app()


@app.get('/classes')
@bottle.view('classes/class_index')
def class_index():
    return dict()


@app.get('/classes/<grade:int>')
@bottle.view('classes/grade_index')
def classes_grade_index(grade):
    return dict(grade=grade)


@app.get('/classes/<grade:int>/<tag>')
@bottle.view('classes/students_index')
def classes_students_index(grade, tag):
    bks = book_queries.get_books_used_in(grade)
    bks = book_queries.order_books_list(bks)
    bks.sort(key=lambda b: b.outGrade)
    c = orga_queries.db.Class.get(grade=grade, tag=tag)
    if c is None:
        app.abort(404)
    return dict(grade=grade, tag=tag, books=bks, c=c)
