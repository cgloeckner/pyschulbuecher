from bottle import get, redirect
import math

from app.db import db
from app.tex import *
from app.xls import *


@get('/admin/apply_requests')
def apply_requests():
    for c in orga.get_classes():
        # convert book requests to loans
        for s in c.student:
            loans.apply_request(s)

    db.commit()

    redirect('/')
