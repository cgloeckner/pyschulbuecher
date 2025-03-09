from bottle import get, post, view, request, redirect
import math

from app.db import db, Settings, DemandManager
from app.utils import errorhandler
from app.tex import *
from app.xls import *


@get('/admin/students')
@view('admin/students_index')
def students_index():
    return dict()


@post('/admin/students/add')
@errorhandler
def students_add_post():
    orga.add_students(request.forms.data)

    db.commit()
    redirect('/admin/students')


@post('/admin/students/addSingle')
@errorhandler
def students_add_post():
    c = db.Class[request.forms.class_id]
    raw = '{0}\t{1}\t{2}'.format(
        c.to_string(
            twoPlace=True),
        request.forms.name,
        request.forms.firstname)
    orga.add_student(raw)

    db.commit()
    redirect('/admin/students')


@post('/admin/students/search')
@errorhandler
@view('admin/students_search')
def students_search_post():
    data = orga.get_students_like(request.forms.name, request.forms.firstname)
    return dict(data=data)


@get('/admin/students/edit/<id:int>')
@view('admin/students_edit')
def students_edit(id):
    return dict(s=db.Student[id])


@post('/admin/students/edit/<id:int>')
@errorhandler
def students_edit_post(id):
    s = db.Student[id]
    s.person.name = request.forms.name
    s.person.firstname = request.forms.firstname
    s.class_ = db.Class[request.forms.class_id]

    db.commit()
    redirect('/admin/students')


@post('/admin/students/delete/<id:int>')
@errorhandler
def students_delete_post(id):
    db.Student[id].delete()

    db.commit()
    redirect('/admin/students')
