import bottle

from app import db
from app.db import book_queries


app = bottle.default_app()


@app.get('/loan/ajax/books')
@bottle.view('loan/book_list')
def loan_ajax_queryBooks():
    classsets = app.bottle.request.query.classsets != "false"
    value = app.bottle.request.query.value
    if value != '':
        value = int(value)
    else:
        value = None

    person = db.Person[int(app.bottle.request.query.person_id)]
    if app.bottle.request.query.by == 'subject':
        subject = db.Subject[value] if value is not None else None
        bks = book_queries.get_real_books_by_subject(subject, classsets)
    else:
        bks = book_queries.get_real_books_by_grade(value, classsets)

    bks = book_queries.order_books_index(bks)
    return dict(person=person, bks=bks)
