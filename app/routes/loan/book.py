import bottle

from app import db
from app.db import loan_queries


app = bottle.default_app()


@app.get('/loan/book/<book_id:int>')
@bottle.view('loan/book_loan')
def loan_book_queryLoan(book_id):
    book = db.Book[book_id]
    l = loan_queries.query_loans_by_book(book)

    return dict(book=book, loans=l)
