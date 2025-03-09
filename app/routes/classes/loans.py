from bottle import *
from pony import orm

from app.db import db, db_session
from app.db import orga_queries as orga
from app.db import book_queries as books
from app.db import loan_queries as loans
from app.utils import errorhandler


@post('/classes/loans/<grade:int>/<tag>')
@errorhandler
def classes_loans_post(grade, tag):
    bks = books.get_books_used_in(grade)
    for s in orga.get_students_in(grade, tag):
        for b in bks:
            key = "%d_%d" % (s.id, b.id)
            count = request.forms.get(key)
            if count is None or count == "":
                count = 0
            else:
                count = int(count)
            loans.update_loan(s.person, b, count)

    db.commit()
    redirect('/classes/%d' % (grade))
