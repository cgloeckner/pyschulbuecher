import bottle

from app.db import db, orga_queries
from app.utils import errorhandler


app = bottle.default_app()


@app.get('/admin/teachers')
@bottle.view('admin/teachers_index')
def teachers_index():
    return dict()


@app.post('/admin/teachers/addSingle')
@errorhandler
def students_add_post():
    raw = '{0}\t{1}\t{2}'.format(
        bottle.request.forms.tag,
        bottle.request.forms.name,
        bottle.request.forms.firstname)
    orga_queries.add_teacher(raw)

    db.commit()
    bottle.redirect('/admin/teachers')


@app.post('/admin/teachers/add')
@errorhandler
def teachers_add_post():
    orga_queries.add_teachers(bottle.request.forms.data)

    db.commit()
    bottle.redirect('/admin/teachers')


@app.get('/admin/teachers/edit/<id:int>')
@bottle.view('admin/teachers_edit')
def students_edit(id):
    return dict(t=db.Teacher[id])


@app.post('/admin/teachers/edit/<id:int>')
@errorhandler
def teachers_edit_post(id):
    s = db.Teacher[id]
    s.person.name = bottle.request.forms.name
    s.person.firstname = bottle.request.forms.firstname
    s.tag = bottle.request.forms.tag.lower()

    db.commit()
    bottle.redirect('/admin/teachers')


@app.post('/admin/teachers/delete/<id:int>')
@errorhandler
def teachers_delete_post(id):
    db.Teacher[id].delete()

    db.commit()
    bottle.redirect('/admin/teachers')
