from bottle import get, post, view, redirect, request

from app.db import db
from app.tex import *
from app.xls import *
from app.utils import errorhandler

@get('/admin/publishers')
@view('admin/publishers_index')
def publishers_index():
    return dict()


@post('/admin/publishers/add')
@errorhandler
def publishers_add_post():
    for name in request.forms.data.split('\n'):
        if len(name) > 0:
            db.Publisher(name=name)

    db.commit()
    redirect('/admin/publishers')


@get('/admin/publishers/edit/<id:int>')
@errorhandler
@view('admin/publishers_edit')
def publishers_edit_form(id):
    return dict(p=db.Publisher[id])


@post('/admin/publishers/edit/<id:int>')
@errorhandler
def publishers_edit_post(id):
    p = db.Publisher[id]
    p.name = request.forms.name

    db.commit()
    redirect('/admin/publishers')


@post('/admin/publishers/delete/<id:int>')
@errorhandler
def publishers_delete(id):
    db.Publisher[id].delete()

    db.commit()
    redirect('/admin/publishers')
