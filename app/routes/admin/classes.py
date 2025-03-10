import bottle

from app.db import db, orga_queries
from app.utils import errorhandler


app = bottle.default_app()


@app.get('/admin/classes')
@bottle.view('admin/classes_index')
def classes_index():
    return dict()


@app.post('/admin/classes/add')
@errorhandler
def classes_add_post():
    orga_queries.add_classes(bottle.request.forms.data)

    db.commit()
    bottle.redirect('/admin/classes')


@app.get('/admin/classes/edit/<id:int>')
@bottle.view('admin/classes_edit')
def classes_edit(id):
    return dict(c=db.Class[id])


@app.post('/admin/classes/edit/<id:int>')
@errorhandler
def classes_edit_post(id):
    orga_queries.update_class(id, int(bottle.request.forms.grade), bottle.request.forms.tag,
                     int(bottle.request.forms.teacher_id))

    db.commit()
    bottle.redirect('/admin/classes')


@app.get('/admin/classes/move/<id:int>')
@bottle.view('admin/classes_move')
def classes_edit(id):
    return dict(c=db.Class[id])


@app.post('/admin/classes/move/<id:int>')
@errorhandler
def classes_move_post(id):
    # fetch target class
    new_id = int(bottle.request.forms.class_id)
    new_class = db.Class[new_id]

    # move students to new class
    students = list()
    for s in db.Class[id].student:
        # note that form names are always strings
        key = str(s.id)
        if bottle.request.forms.get(key) == 'on':
            s.class_ = new_class

    db.commit()
    bottle.redirect('/admin/classes/move/%d' % new_id)


@app.post('/admin/classes/delete/<id:int>')
@bottle.view('admin/classes_delete')
def class_delete_prompt(id):
    return dict(c=db.Class[id])


@app.get('/admin/classes/delete/<id:int>/confirm')
@errorhandler
def classes_delete_post(id):
    c = db.Class[id]
    for s in c.student:
        s.delete()

    c.delete()

    db.commit()
    bottle.redirect('/admin/classes')
