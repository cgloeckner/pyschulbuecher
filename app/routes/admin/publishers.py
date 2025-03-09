import bottle

from app.db import db
from app.utils import errorhandler


app = bottle.default_app()


@app.get('/admin/publishers')
@bottle.view('admin/publishers_index')
def publishers_index():
    return dict()


@app.post('/admin/publishers/add')
@errorhandler
def publishers_add_post():
    for name in app.request.forms.data.split('\n'):
        if len(name) > 0:
            db.Publisher(name=name)

    db.commit()
    app.redirect('/admin/publishers')


@app.get('/admin/publishers/edit/<id:int>')
@errorhandler
@bottle.view('admin/publishers_edit')
def publishers_edit_form(id):
    return dict(p=db.Publisher[id])


@app.post('/admin/publishers/edit/<id:int>')
@errorhandler
def publishers_edit_post(id):
    p = db.Publisher[id]
    p.name = app.request.forms.name

    db.commit()
    app.redirect('/admin/publishers')


@app.post('/admin/publishers/delete/<id:int>')
@errorhandler
def publishers_delete(id):
    db.Publisher[id].delete()

    db.commit()
    app.redirect('/admin/publishers')
