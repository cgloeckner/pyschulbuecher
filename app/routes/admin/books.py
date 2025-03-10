import bottle

from app.db import db, Currency
from app.db import book_queries
from app.utils import errorhandler


app = bottle.default_app()


@app.get('/admin/books')
@bottle.view('admin/books_index')
def books_index():
    return dict()


@app.post('/admin/books/add')
@errorhandler
def books_add_post():
    book_queries.add_books(bottle.request.forms.data)

    db.commit()
    app.redirect('/admin/books')


@app.post('/admin/books/addSingle')
@errorhandler
def books_add_post():
    args = [bottle.request.forms.title, bottle.request.forms.isbn, bottle.request.forms.price]

    args.append(db.Publisher[int(bottle.request.forms.publisher_id)].name)
    args.append(bottle.request.forms.inGrade)
    args.append(bottle.request.forms.outGrade)
    args.append(db.Subject[int(bottle.request.forms.subject_id)
                           ].tag if bottle.request.forms.subject_id != "" else "")

    args.append("True" if bottle.request.forms.novices == 'on' else "False")
    args.append("True" if bottle.request.forms.advanced == 'on' else "False")
    args.append("True" if bottle.request.forms.workbook == 'on' else "False")
    args.append("True" if bottle.request.forms.classsets == 'on' else "False")
    args.append("True" if bottle.request.forms.for_loan == 'on' else "False")
    args.append(bottle.request.forms.comment)

    print(args)

    book_queries.add_book('\t'.join(args))

    db.commit()
    app.redirect('/admin/books')


@app.get('/admin/books/edit/<id:int>')
@errorhandler
@bottle.view('admin/books_edit')
def books_edit_form(id):
    return dict(b=db.Book[id])


@app.post('/admin/books/edit/<id:int>')
@errorhandler
def books_edit_post(id):
    b = db.Book[id]
    b.title = bottle.request.forms.title
    b.isbn = bottle.request.forms.isbn
    b.price = Currency.from_string(
        bottle.request.forms.price) if bottle.request.forms.price != '' else 0
    b.publisher = db.Publisher[int(bottle.request.forms.publisher_id)]
    b.stock = int(bottle.request.forms.stock)
    b.inGrade = int(bottle.request.forms.inGrade)
    b.outGrade = int(bottle.request.forms.outGrade)
    b.subject = db.Subject[int(bottle.request.forms.subject_id)
                           ] if bottle.request.forms.subject_id != "" else None
    b.novices = True if bottle.request.forms.novices == 'on' else False
    b.advanced = True if bottle.request.forms.advanced == 'on' else False
    b.workbook = True if bottle.request.forms.workbook == 'on' else False
    b.classsets = True if bottle.request.forms.classsets == 'on' else False
    b.for_loan = True if bottle.request.forms.for_loan == 'on' else False
    b.comment = bottle.request.forms.comment

    db.commit()
    app.redirect('/admin/books')


@app.post('/admin/books/delete/<id:int>')
@errorhandler
def books_delete(id):
    db.Book[id].delete()

    db.commit()
    app.redirect('/admin/books')
