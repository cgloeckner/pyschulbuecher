import os
import bottle

from app.db import Settings, orga_queries, book_queries


app = bottle.default_app()


@app.get('/admin/lists/download/<fname>')
def admin_lists_download(fname):
    """Note that this callback is NOT covered by the test suite.
    """
    return bottle.static_file(fname, root='./export')


@app.get('/admin/lists')
@bottle.view('admin/lists_index')
def lists_index():
    if not os.path.isdir('export'):
        os.mkdir('export')

    export = os.path.join(os.getcwd(), 'export')

    s = Settings()
    return dict(export=export, settings=s)


@app.get('/admin/preview/booklist')
@bottle.view('admin/booklist_preview')
def booklist_preview():
    all_books = dict()

    for grade in orga_queries.get_grade_range():
        # fetch specific books
        spec_bks = book_queries.get_books_used_in(0, True)

        # fetch and order books
        bks_new = book_queries.get_books_used_in(grade, booklist=True)
        bks_old = book_queries.get_books_started_in(grade, booklist=True)

        key = f'{grade:02d}'
        all_books[key] = book_queries.order_books_list(bks_old)
        if grade > 5:
            all_books[f'{key}_neu'] = book_queries.order_books_list(bks_new)

    return dict(all_books=all_books)

