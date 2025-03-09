from bottle import get, post, view, request, redirect
import math

from app.db import db, Settings, DemandManager
from app.utils import errorhandler
from app.tex import *
from app.xls import *


@get('/admin/classes')
@view('admin/classes_index')
def classes_index():
    return dict()


@post('/admin/classes/add')
@errorhandler
def classes_add_post():
    orga.add_classes(request.forms.data)

    db.commit()
    redirect('/admin/classes')


@get('/admin/classes/edit/<id:int>')
@view('admin/classes_edit')
def classes_edit(id):
    return dict(c=db.Class[id])


@post('/admin/classes/edit/<id:int>')
@errorhandler
def classes_edit_post(id):
    orga.update_class(id, int(request.forms.grade), request.forms.tag,
                     int(request.forms.teacher_id))

    db.commit()
    redirect('/admin/classes')


@get('/admin/classes/move/<id:int>')
@view('admin/classes_move')
def classes_edit(id):
    return dict(c=db.Class[id])


@post('/admin/classes/move/<id:int>')
@errorhandler
def classes_move_post(id):
    # fetch target class
    new_id = int(request.forms.class_id)
    new_class = db.Class[new_id]

    # move students to new class
    students = list()
    for s in db.Class[id].student:
        # note that form names are always strings
        key = str(s.id)
        if request.forms.get(key) == 'on':
            s.class_ = new_class

    db.commit()
    redirect('/admin/classes/move/%d' % new_id)


@post('/admin/classes/delete/<id:int>')
@view('admin/classes_delete')
def class_delete_prompt(id):
    return dict(c=db.Class[id])


@get('/admin/classes/delete/<id:int>/confirm')
@errorhandler
def classes_delete_post(id):
    c = db.Class[id]
    for s in c.student:
        s.delete()

    c.delete()

    db.commit()
    redirect('/admin/classes')
