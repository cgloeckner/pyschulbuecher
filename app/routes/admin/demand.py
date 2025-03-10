import bottle
import math

from app.db import Settings, DemandManager, book_queries


app = bottle.default_app()


@app.get('/admin/demand')
@bottle.view('admin/demand_form')
def demand_form():
    s = Settings()

    # load student numbers from file
    demand = DemandManager()
    demand.load_from_file()

    return dict(s=s, demand=demand)


@app.post('/admin/demand')
@bottle.view('admin/demand_report')
def demand_report():
    s = Settings()
    
    # percentage of lowering the stock to gain buffer (e.g. for damaged books)
    lowering = int(bottle.request.forms.lowering)

    # fetch demand from UI input
    demand = DemandManager()
    demand.parse(bottle.request.forms.get)
    demand.save_to_file()

    # create book demand report
    bks = book_queries.order_books_list(book_queries.get_all_books())
    total = 0
    data = dict()
    for b in bks:
        if b.classsets or b.workbook:
            # only consider books for loan
            continue

        if b.price is None:
            # skip because this book cannot be bought anymore
            continue

        # determine raw demand (books in use + requested)
        available = math.floor(b.stock * (100 - lowering) / 100.0)
        in_use = demand.count_books_in_use(b)
        requested = len(b.request)
        raw_demand = in_use + requested

        # determine number of required books
        required = raw_demand - available

        if required > 0:
            # calculate how many books will be bought by school / by parents.
            # if enough books are available, the number of actually required
            # books might be lower as the number requested books, hence the
            # number of required books will be bought by the school.
            # if the requested number is lower, more books are bought by
            # parents
            by_school = min(required, requested)
            by_parents = required - by_school
        else:
            required = 0
            by_parents = 0
            by_school = 0

        costs = b.price * by_school

        # save data
        data[b.id] = {
            'raw_demand': raw_demand,
            'in_use': in_use,
            'requested': requested,
            'available': available,
            'required': required,
            'by_parents': by_parents,
            'by_school': by_school,
            'costs': costs
        }
        total += costs

    return dict(bks=bks, data=data, total=total, s=s)
