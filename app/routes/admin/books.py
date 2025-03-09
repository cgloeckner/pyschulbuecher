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
    book_queries.add_books(app.request.forms.data)

    db.commit()
    app.redirect('/admin/books')


@app.post('/admin/books/addSingle')
@errorhandler
def books_add_post():
    args = [app.request.forms.title, app.request.forms.isbn, app.request.forms.price]

    args.append(db.Publisher[int(app.request.forms.publisher_id)].name)
    args.append(app.request.forms.inGrade)
    args.append(app.request.forms.outGrade)
    args.append(db.Subject[int(app.request.forms.subject_id)
                           ].tag if app.request.forms.subject_id != "" else "")

    args.append("True" if app.request.forms.novices == 'on' else "False")
    args.append("True" if app.request.forms.advanced == 'on' else "False")
    args.append("True" if app.request.forms.workbook == 'on' else "False")
    args.append("True" if app.request.forms.classsets == 'on' else "False")
    args.append("True" if app.request.forms.for_loan == 'on' else "False")
    args.append(app.request.forms.comment)

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
    b.title = app.request.forms.title
    b.isbn = app.request.forms.isbn
    b.price = Currency.from_string(
        app.request.forms.price) if app.request.forms.price != '' else 0
    b.publisher = db.Publisher[int(app.request.forms.publisher_id)]
    b.stock = int(app.request.forms.stock)
    b.inGrade = int(app.request.forms.inGrade)
    b.outGrade = int(app.request.forms.outGrade)
    b.subject = db.Subject[int(app.request.forms.subject_id)
                           ] if app.request.forms.subject_id != "" else None
    b.novices = True if app.request.forms.novices == 'on' else False
    b.advanced = True if app.request.forms.advanced == 'on' else False
    b.workbook = True if app.request.forms.workbook == 'on' else False
    b.classsets = True if app.request.forms.classsets == 'on' else False
    b.for_loan = True if app.request.forms.for_loan == 'on' else False
    b.comment = app.request.forms.comment

    db.commit()
    app.redirect('/admin/books')


@app.post('/admin/books/delete/<id:int>')
@errorhandler
def books_delete(id):
    db.Book[id].delete()

    db.commit()
    app.redirect('/admin/books')
