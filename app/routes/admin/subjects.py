import bottle

from app.db import db
from app.utils import errorhandler


app = bottle.default_app()


@app.get('/admin/subjects')
@bottle.view('admin/subjects_index')
def subjects_index():
    return dict()


@app.post('/admin/subjects/add')
@errorhandler
def subjects_add_post():
    for line in bottle.request.forms.data.split('\n'):
        if len(line) > 0:
            tag, name = line.split('\t')
            db.Subject(name=name, tag=tag)

    db.commit()
    bottle.redirect('/admin/subjects')


@app.get('/admin/subjects/edit/<id:int>')
@errorhandler
@bottle.view('admin/subjects_edit')
def subjects_edit_form(id):
    return dict(s=db.Subject[id])


@app.post('/admin/subjects/edit/<id:int>')
@errorhandler
def subjects_edit_post(id):
    s = db.Subject[id]
    s.tag = bottle.request.forms.tag
    s.name = bottle.request.forms.name
    s.elective = bottle.request.forms.elective == 'on'

    db.commit()
    bottle.redirect('/admin/subjects')


@app.post('/admin/subjects/delete/<id:int>')
@errorhandler
def subjects_delete(id):
    db.Subject[id].delete()

    db.commit()
    bottle.redirect('/admin/subjects')
