from bottle import *
from pony import orm

from app import db, db_session, errorhandler
from app.db import orga_queries as orga
from app.db import book_queries as books
from app.db import loan_queries as loans


@get('/loan/book/<book_id:int>')
@view('loan/book_loan')
def loan_book_queryLoan(book_id):
    book = db.Book[book_id]
    l = loans.query_loans_by_book(book)

    return dict(book=book, loans=l)
