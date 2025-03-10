import bottle

from app.db import db, db_session
from app.db import orga_queries
from app.db import book_queries
from app.db import loan_queries
from app.utils import errorhandler


app = bottle.default_app()


@app.get('/classes/requests/<grade:int>/<tag>/<version>')
@bottle.view('classes/request_form')
def classes_requests_form(grade, tag, version):
    query_grade = grade
    if 'next' in version:
        query_grade += 1

    # query grade-specific books
    if tag.lower() == 'neu' or 'full' in version:
        bks = book_queries.get_books_used_in(query_grade, True)
    else:
        bks = book_queries.get_books_started_in(query_grade, True)
    # order queried books
    bks = book_queries.order_books_list(bks)

    # add misc books
    bks += list(book_queries.get_books_used_in(0, True))
    c = orga_queries.db.Class.get(grade=grade, tag=tag)
    if c is None:
        app.abort(404)

    return dict(grade=grade, tag=tag, books=bks, c=c, version=version)


@app.post('/classes/requests/<grade:int>/<tag>/<version>')
@errorhandler
def classes_requests_post(grade, tag, version):
    query_grade = grade
    if 'next' in version:
        query_grade += 1

    # query grade-specific books
    if tag.lower() == 'neu' or 'full' in version:
        bks = book_queries.get_books_used_in(query_grade, True)
    else:
        bks = book_queries.get_books_started_in(query_grade, True)
    # order queried books
    bks = book_queries.order_books_list(bks)

    # add misc books
    bks += list(book_queries.get_books_used_in(0, True))
    for s in orga_queries.get_students_in(grade, tag):
        for b in bks:
            key = "%d_%d" % (s.id, b.id)
            status = bottle.request.forms.get(key) == 'on'
            loan_queries.update_request(s, b, status)

    db.commit()
    app.redirect('/classes/%d' % (grade))
