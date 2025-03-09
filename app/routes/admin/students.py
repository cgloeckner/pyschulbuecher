import bottle

from app.db import db, orga_queries
from app.utils import errorhandler


app = bottle.default_app()


@app.get('/admin/students')
@bottle.view('admin/students_index')
def students_index():
    return dict()


@app.post('/admin/students/add')
@errorhandler
def students_add_post():
    orga_queries.add_students(app.request.forms.data)

    db.commit()
    app.redirect('/admin/students')


@app.post('/admin/students/addSingle')
@errorhandler
def students_add_post():
    c = db.Class[app.request.forms.class_id]
    raw = '{0}\t{1}\t{2}'.format(
        c.to_string(
            twoPlace=True),
        app.request.forms.name,
        app.request.forms.firstname)
    orga_queries.add_student(raw)

    db.commit()
    app.redirect('/admin/students')


@app.post('/admin/students/search')
@errorhandler
@bottle.view('admin/students_search')
def students_search_post():
    data = orga_queries.get_students_like(app.request.forms.name, app.request.forms.firstname)
    return dict(data=data)


@app.get('/admin/students/edit/<id:int>')
@bottle.view('admin/students_edit')
def students_edit(id):
    return dict(s=db.Student[id])


@app.post('/admin/students/edit/<id:int>')
@errorhandler
def students_edit_post(id):
    s = db.Student[id]
    s.person.name = app.request.forms.name
    s.person.firstname = app.request.forms.firstname
    s.class_ = db.Class[app.request.forms.class_id]

    db.commit()
    app.redirect('/admin/students')


@app.post('/admin/students/delete/<id:int>')
@errorhandler
def students_delete_post(id):
    db.Student[id].delete()

    db.commit()
    app.redirect('/admin/students')
