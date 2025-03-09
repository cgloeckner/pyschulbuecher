from bottle import get, post, view, redirect, request

from app.db import db, Currency
from app.tex import *
from app.xls import *
from app.utils import errorhandler


@get('/admin/books')
@view('admin/books_index')
def books_index():
    return dict()


@post('/admin/books/add')
@errorhandler
def books_add_post():
    books.add_books(request.forms.data)

    db.commit()
    redirect('/admin/books')


@post('/admin/books/addSingle')
@errorhandler
def books_add_post():
    args = [request.forms.title, request.forms.isbn, request.forms.price]

    args.append(db.Publisher[int(request.forms.publisher_id)].name)
    args.append(request.forms.inGrade)
    args.append(request.forms.outGrade)
    args.append(db.Subject[int(request.forms.subject_id)
                           ].tag if request.forms.subject_id != "" else "")

    args.append("True" if request.forms.novices == 'on' else "False")
    args.append("True" if request.forms.advanced == 'on' else "False")
    args.append("True" if request.forms.workbook == 'on' else "False")
    args.append("True" if request.forms.classsets == 'on' else "False")
    args.append("True" if request.forms.for_loan == 'on' else "False")
    args.append(request.forms.comment)

    print(args)

    books.add_book('\t'.join(args))

    db.commit()
    redirect('/admin/books')


@get('/admin/books/edit/<id:int>')
@errorhandler
@view('admin/books_edit')
def books_edit_form(id):
    return dict(b=db.Book[id])


@post('/admin/books/edit/<id:int>')
@errorhandler
def books_edit_post(id):
    b = db.Book[id]
    b.title = request.forms.title
    b.isbn = request.forms.isbn
    b.price = Currency.from_string(
        request.forms.price) if request.forms.price != '' else 0
    b.publisher = db.Publisher[int(request.forms.publisher_id)]
    b.stock = int(request.forms.stock)
    b.inGrade = int(request.forms.inGrade)
    b.outGrade = int(request.forms.outGrade)
    b.subject = db.Subject[int(request.forms.subject_id)
                           ] if request.forms.subject_id != "" else None
    b.novices = True if request.forms.novices == 'on' else False
    b.advanced = True if request.forms.advanced == 'on' else False
    b.workbook = True if request.forms.workbook == 'on' else False
    b.classsets = True if request.forms.classsets == 'on' else False
    b.for_loan = True if request.forms.for_loan == 'on' else False
    b.comment = request.forms.comment

    db.commit()
    redirect('/admin/books')


@post('/admin/books/delete/<id:int>')
@errorhandler
def books_delete(id):
    db.Book[id].delete()

    db.commit()
    redirect('/admin/books')
