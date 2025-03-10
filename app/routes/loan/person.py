import bottle

from app import db, errorhandler
from app.db import loan_queries


app = bottle.default_app()


@app.get('/loan/person/<id:int>')
@bottle.view('loan/person_listing')
def loan_person_overview(id):
    person = db.Person[id]
    loan = loan_queries.order_loan_overview(person.loan)
    request = loan_queries.order_request_overview(person.request)
    return dict(person=person, loan=loan, request=request)


@app.get('/loan/person/<person_id:int>/add')
@bottle.view('loan/person_add')
def loan_person_add(person_id):
    return dict(id=person_id)


@app.post('/loan/person/<person_id:int>/add')
@errorhandler
def loan_person_add(person_id):
    person = db.Person[person_id]

    for b in db.Book.select():
        raw = bottle.request.forms.get(str(b.id), '')
        if raw.isnumeric():
            value = int(raw)
            if value > 0:
                loan_queries.add_loan(person, b, value)

    db.commit()
    app.redirect('/loan/person/%d' % person_id)


@app.post('/loan/person/<person_id:int>/back')
@errorhandler
def loan_person_add(person_id):
    person = db.Person[person_id]

    for l in person.loan:
        if bottle.request.forms.get(str(l.book.id)) == 'on':
            loan_queries.update_loan(person, db.Book[l.book.id], 0)

    db.commit()
    app.redirect('/loan/person/%d' % person_id)
