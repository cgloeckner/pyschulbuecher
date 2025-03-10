import bottle

from app.db import db, orga_queries, loan_queries


app = bottle.default_app()


@app.get('/admin/apply_requests')
def apply_requests():
    for c in orga_queries.get_classes():
        # convert book requests to loans
        for s in c.student:
            loan_queries.apply_request(s)

    db.commit()

    bottle.redirect('/')
