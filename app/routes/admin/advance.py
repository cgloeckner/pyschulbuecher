import bottle

from app.db import db, orga_queries

app = bottle.default_app()

@app.get('/admin/advance')
@bottle.view('admin/advance')
def advance_info():
    return dict()


@app.get('/admin/advance/confirm')
def advance_confirm():
    for c in orga_queries.get_classes():
        # advance every class
        c.grade += 1

    db.commit()

    app.redirect('/')
