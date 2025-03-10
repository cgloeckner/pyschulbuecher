import bottle

from app.db import db, db_session
from app.db import orga_queries
from app.db import book_queries
from app.db import loan_queries
from app.utils import errorhandler


app = bottle.default_app()


@app.post('/classes/loans/<grade:int>/<tag>')
@errorhandler
def classes_loans_post(grade, tag):
    bks = book_queries.get_books_used_in(grade)
    for s in orga_queries.get_students_in(grade, tag):
        for b in bks:
            key = "%d_%d" % (s.id, b.id)
            count = bottle.request.forms.get(key)
            if count is None or count == "":
                count = 0
            else:
                count = int(count)
            loan_queries.update_loan(s.person, b, count)

    db.commit()
    app.redirect('/classes/%d' % (grade))
