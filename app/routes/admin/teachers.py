from bottle import get, post, view, request, redirect
import math

from app.db import db, Settings, DemandManager
from app.utils import errorhandler
from app.tex import *
from app.xls import *


@get('/admin/teachers')
@view('admin/teachers_index')
def teachers_index():
    return dict()


@post('/admin/teachers/addSingle')
@errorhandler
def students_add_post():
    raw = '{0}\t{1}\t{2}'.format(
        request.forms.tag,
        request.forms.name,
        request.forms.firstname)
    orga.add_teacher(raw)

    db.commit()
    redirect('/admin/teachers')


@post('/admin/teachers/add')
@errorhandler
def teachers_add_post():
    orga.add_teachers(request.forms.data)

    db.commit()
    redirect('/admin/teachers')


@get('/admin/teachers/edit/<id:int>')
@view('admin/teachers_edit')
def students_edit(id):
    return dict(t=db.Teacher[id])


@post('/admin/teachers/edit/<id:int>')
@errorhandler
def teachers_edit_post(id):
    s = db.Teacher[id]
    s.person.name = request.forms.name
    s.person.firstname = request.forms.firstname
    s.tag = request.forms.tag.lower()

    db.commit()
    redirect('/admin/teachers')


@post('/admin/teachers/delete/<id:int>')
@errorhandler
def teachers_delete_post(id):
    db.Teacher[id].delete()

    db.commit()
    redirect('/admin/teachers')
