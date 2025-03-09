from bottle import get, post, view, redirect, request

from app.db import db
from app.tex import *
from app.xls import *
from app.utils import errorhandler

@get('/admin/subjects')
@view('admin/subjects_index')
def subjects_index():
    return dict()


@post('/admin/subjects/add')
@errorhandler
def subjects_add_post():
    for line in request.forms.data.split('\n'):
        if len(line) > 0:
            tag, name = line.split('\t')
            db.Subject(name=name, tag=tag)

    db.commit()
    redirect('/admin/subjects')


@get('/admin/subjects/edit/<id:int>')
@errorhandler
@view('admin/subjects_edit')
def subjects_edit_form(id):
    return dict(s=db.Subject[id])


@post('/admin/subjects/edit/<id:int>')
@errorhandler
def subjects_edit_post(id):
    s = db.Subject[id]
    s.tag = request.forms.tag
    s.name = request.forms.name
    s.elective = request.forms.elective == 'on'

    db.commit()
    redirect('/admin/subjects')


@post('/admin/subjects/delete/<id:int>')
@errorhandler
def subjects_delete(id):
    db.Subject[id].delete()

    db.commit()
    redirect('/admin/subjects')
