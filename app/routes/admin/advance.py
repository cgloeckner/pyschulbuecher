from bottle import get, view, redirect

from app.db import orga_queries as orga
from app.db import db


@get('/admin/advance')
@view('admin/advance')
def advance_info():
    return dict()


@get('/admin/advance/confirm')
def advance_confirm():
    for c in orga.get_classes():
        # advance every class
        c.grade += 1

    db.commit()

    redirect('/')
