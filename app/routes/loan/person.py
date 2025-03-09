from bottle import *
from pony import orm

from app import db, db_session, errorhandler
from app.db import orga_queries as orga
from app.db import book_queries as books
from app.db import loan_queries as loans


@get('/loan/person/<id:int>')
@view('loan/person_listing')
def loan_person_overview(id):
    person = db.Person[id]
    loan = loans.order_loan_overview(person.loan)
    request = loans.order_request_overview(person.request)
    return dict(person=person, loan=loan, request=request)


@get('/loan/person/<person_id:int>/add')
@view('loan/person_add')
def loan_person_add(person_id):
    return dict(id=person_id)


@post('/loan/person/<person_id:int>/add')
@errorhandler
def loan_person_add(person_id):
    person = db.Person[person_id]

    for b in db.Book.select():
        raw = request.forms.get(str(b.id), '')
        if raw.isnumeric():
            value = int(raw)
            if value > 0:
                loans.add_loan(person, b, value)

    db.commit()
    redirect('/loan/person/%d' % person_id)


@post('/loan/person/<person_id:int>/back')
@errorhandler
def loan_person_add(person_id):
    person = db.Person[person_id]

    for l in person.loan:
        if request.forms.get(str(l.book.id)) == 'on':
            loans.update_loan(person, db.Book[l.book.id], 0)

    db.commit()
    redirect('/loan/person/%d' % person_id)
