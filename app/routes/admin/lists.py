from bottle import get, post, view, request, static_file
import time

from app.db import db, Settings, DemandManager
from app.utils import errorhandler
from app.tex import *
from app.xls import *



@get('/admin/lists/download/<fname>')
def admin_lists_download(fname):
    """Note that this callback is NOT covered by the test suite.
    """
    return static_file(fname, root='./export')


@get('/admin/lists')
@view('admin/lists_index')
def lists_index():
    if not os.path.isdir('export'):
        os.mkdir('export')

    export = os.path.join(os.getcwd(), 'export')

    s = Settings()
    return dict(export=export, settings=s)


@get('/admin/lists/generate/db_dump')
def db_dump_generate():
    s = Settings()
    # generte Excel sheet with entire db loaning content

    print('Generating Loan Reports')
    d = time.time()
    yield 'Bitte warten...'

    xlsx = DatabaseDumpXls(s)

    # sort classes
    classes = list(db.Class.select())
    orga.sort_classes(classes)

    for c in classes:
        yield '%s<br />' % c.to_string()
        bks = books.get_books_used_in(c.grade, booklist=True)
        xlsx(c, bks)

    xlsx.saveToFile()

    print('Done')
    d = time.time() - d

    yield '<hr /><br />Erledigt in %f Sekunden<hr /><pre>%s</pre>' % (d, xlsx.getPath())


@get('/admin/lists/generate/inventory')
def book_inventory():
    s = Settings()
    inv = InventoryReport(s)
    inv()
    inv.saveToFile()
    yield '<pre>%s</pre>' % inv.getPath()


@get('/admin/lists/generate/councils')
def councils_generate():
    s = Settings()
    # generate Excel sheet for demand of councils (file per subject
    # council)

    print('Generating Loan Reports')
    d = time.time()
    yield 'Bitte warten...'

    for s in db.Subject.select():
        councils = SubjectCouncilXls(s)
        councils(s)
        councils.saveToFile()
        yield '<pre>%s</pre>' % councils.getPath(s)

    print('Done')
    d = time.time() - d

    yield '<hr /><br />Erledigt in %f Sekunden' % (d)


@get('/admin/lists/generate/teacherloans')
def teacherloans_generate():
    s = Settings()
    loanreport = LoanReportPdf('Lehrer', s)

    print('Generating Loan Reports')
    d = time.time()

    for t in db.Teacher.select().order_by(
            lambda t: t.person.firstname).order_by(
            lambda t: t.person.name):
        yield '%s ' % t.tag.upper()
        loanreport(t.person)

    loanreport.saveToFile()
    yield '<pre>%s</pre>\n' % loanreport.getPath()

    print('Done')
    d = time.time() - d

    yield '<hr /><br />Erledigt in %f Sekunden' % (d)


@get('/admin/lists/generate/classsets')
def teacher_classsets_generate():
    s = Settings()
    loanreport = ClasssetsPdf('Lehrer', settings=s, threshold=3)

    print('Generating Loan Reports')
    d = time.time()

    for t in db.Teacher.select().order_by(
            lambda t: t.person.firstname).order_by(
            lambda t: t.person.name):
        yield '%s ' % t.tag.upper()
        loanreport(t.person)

    loanreport.saveToFile()
    yield '<pre>%s</pre>\n' % loanreport.getPath()

    print('Done')
    d = time.time() - d

    yield '<hr /><br />Erledigt in %f Sekunden' % (d)


@get('/admin/lists/generate/studentloans')
@view('admin/loanlist_select')
def studentloans_selection():
    classes = list(
        db.Class.select().order_by(
            lambda c: c.tag).order_by(
            lambda c: c.grade))

    return dict(classes=classes, sort_students=orga.sort_students)


@post('/admin/lists/generate/studentloans')
def studentsloans_generate():
    next_year = request.forms.get('next_year') == 'on'
    use_requests = request.forms.get('use_requests') == 'on'
    split_pdf = request.forms.get('split_pdf') == 'on'
    loan_report = request.forms.get('loan_report') == 'on'

    if not split_pdf:
        s = Settings()
        loancontract = LoanContractPdf('manual', s, advance=next_year)

    print('Generating Loan Contracts')
    d = time.time()
    yield 'Bitte warten...<br /><ul>'

    # iterate all classes
    for c in db.Class.select().order_by(
            lambda c: c.tag).order_by(
            lambda c: c.grade):
        yield '<li>{0}'.format(c.to_string())
        students = students = list(c.student)
        orga.sort_students(students)

        # start new pdf
        if split_pdf:
            s = Settings()
            loancontract = LoanContractPdf(
                c.to_string(), s, advance=next_year)

        n = 0
        yield '<ul>'
        for s in students:
            # add student if selected
            if request.forms.get(str(s.person.id)) == 'on':
                yield '<li>{0}, {1}</li>'.format(s.person.name, s.person.firstname)
                n += 1
                loancontract(
                    s,
                    include_requests=use_requests,
                    loan_report=loan_report)

        yield '</ul>'

        if n > 0 and split_pdf:
            # save pdf
            loancontract.saveToFile()
            yield '<pre>%s</pre>\n' % loancontract.getPath()

        yield '</li>'

    if not split_pdf:
        loancontract.saveToFile()
        yield '<pre>%s</pre>\n' % loancontract.getPath()

    d = time.time() - d

    yield '<hr /><br />Erledigt in %f Sekunden\n' % (d)


@get('/admin/preview/booklist')
@view('admin/booklist_preview')
def booklist_preview():
    all_books = dict()

    for grade in orga.get_grade_range():
        # fetch specific books
        spec_bks = books.get_books_used_in(0, True)

        # fetch and order books
        bks_new = books.get_books_used_in(grade, booklist=True)
        bks_old = books.get_books_started_in(grade, booklist=True)

        key = f'{grade:02d}'
        all_books[key] = books.order_books_list(bks_old)
        if grade > 5:
            all_books[f'{key}_neu'] = books.order_books_list(bks_new)

    return dict(all_books=all_books)


@post('/admin/lists/generate/booklist')
def booklist_generate():
    s = Settings()
    booklist = BooklistPdf(s)

    print('Detecting excluded books')
    exclude = set()
    for g in orga.get_grade_range():
        grade_key = f'{g:02d}'
        for b in books.get_books_used_in(g):
            # regular booklist
            key = f'{grade_key}_{b.id}'
            if request.forms.get(key) != 'on':
                exclude.add(key)
            # new student's booklist
            key = f'{grade_key}_neu_{b.id}'
            if request.forms.get(key) != 'on':
                exclude.add(key)

    print('Generating Booklists')
    d = time.time()
    yield 'Bitte warten...'
    for g in orga.get_grade_range():
        yield '<br>Klasse %d\n' % g
        booklist(g, exclude)
        if g > 5:
            yield ' und Neuzugänge'
            booklist(g, exclude, new_students=True)

    booklist.infosheet()

    print('Fertig')
    d = time.time() - d

    yield '<hr /><br />Erledigt in %f Sekunden' % (d)


@get('/admin/lists/generate/requestlist')
def requestlist_generate():
    s = Settings()
    requestlist = RequestlistPdf(s)

    # exclude 12th grade (last grade)
    for grade in orga.get_persisting_grade_range():
        yield 'Klasse %d<br />\n' % grade
        for c in orga.get_classes_by_grade(grade):
            requestlist(c)
    requestlist.saveToFile()

    yield '<pre>%s</pre>\n' % (requestlist.getPath())


@get('/admin/lists/generate/planner/<mode>')
def plannerlist_generate(mode):
    planners = PlannerXls()
    classes = list()
    if mode == 'next':
        r = orga.get_persisting_grade_range(delta=-1)
        advance = True
    else:
        r = orga.get_grade_range()
        advance = False
    for grade in r:
        for c in orga.get_classes_by_grade(grade):
            classes.append(c)
    planners(classes, advance=advance)
    planners.saveToFile()

    return '<a href="/admin/lists/download/{0}" target="_blank">Übersicht Schulplaner</a>'.format(
        planners.fname)


@get('/admin/lists/generate/bookreturn')
def bookreturn_generate():
    s = Settings()
    bookreturn = BookreturnPdf(s)

    # generate overview lists for all grades
    for grade in orga.get_grade_range():
        bookreturn.addOverview(grade)

    # generate return lists for all grades
    for grade in orga.get_grade_range():
        yield 'Klasse %d<br />\n' % grade
        for c in orga.get_classes_by_grade(grade):
            bookreturn(c)
    bookreturn.saveToFile()

    yield '<pre>%s</pre>' % bookreturn.getPath()


@get('/admin/lists/generate/requestloan')
def requestloan_generate():
    s = Settings()
    bookloan = BookloanPdf(s)

    yield 'Erzeuge Ausleihübersicht...<br />\n'

    # generate return lists for all grades (for the next year)
    for grade in orga.get_grade_range():
        yield 'Klasse %d<br />\n' % (grade)
        for c in orga.get_classes_by_grade(grade-1):
            bookloan(c, True)
    bookloan.saveToFile()
    yield '<pre>%s</pre>\n' % bookloan.getPath()

    yield 'Erzeuge Ausleihlisten...<br />\n'

    for c in db.Class.select().order_by(
            lambda c: c.tag).order_by(
            lambda c: c.grade):
        if len(c.student) == 0:
            continue

        # start new pdf
        s = Settings()
        loancontract = LoanContractPdf(c.to_string(), s, advance=True)

        for s in c.student.order_by(
                lambda s: s.person.firstname).order_by(
                lambda s: s.person.name):
            loancontract(s, include_requests=True)

        # save pdf
        loancontract.saveToFile()
        yield '<pre>%s</pre>\n' % loancontract.getPath()

    yield '<hr />Fertig'


@get('/admin/lists/generate/bookloan')
def bookloan_generate():
    s = Settings()
    bookloan = BookloanPdf(s)

    yield 'Erzeuge Ausleihübersicht...<br />\n'

    # generate return lists for all grades (for the current year)
    for grade in orga.get_grade_range():
        yield 'Klasse %d<br />\n' % grade
        for c in orga.get_classes_by_grade(grade):
            bookloan(c, True)
    bookloan.saveToFile()
    yield '<pre>%s</pre>\n' % bookloan.getPath()

    yield 'Erzeuge Ausleihlisten...<br />\n'

    for c in db.Class.select().order_by(
            lambda c: c.tag).order_by(
            lambda c: c.grade):
        if len(c.student) == 0:
            continue

        # start new pdf
        s = Settings()
        loancontract = LoanContractPdf(c.to_string(), set)

        for s in c.student.order_by(
                lambda s: s.person.firstname).order_by(
                lambda s: s.person.name):
            loancontract(s, include_requests=True)

        # save pdf
        loancontract.saveToFile()
        yield '<pre>%s</pre>\n' % loancontract.getPath()

    yield '<hr />Fertig'


@get('/admin/lists/generate/returnlist/<mode>')
def bookpending_generate(mode):
    yield '<b>Nach Büchern:</b><ul>'
    for grade in orga.get_grade_range():
        s = Settings()
        pending = BookpendingPdf(s)
        n = pending.queryBooks(grade, tooLate=mode == 'tooLate')
        if n > 0:
            fname = pending.saveToFile(
                suffix='Klasse{0}_nachBüchern'.format(grade))
            yield '<li><a href="/admin/lists/download/{0}.pdf" target="_blank">Klassenstufe {1}</a></li>'.format(fname, grade)
        else:
            yield '<li>keine in Klasse {0}</li>'.format(grade)
    yield '</ul><hr />Fertig'


@get('/admin/lists/generate/loanlist/<grade>')
def bookpending_generate(grade):
    yield '<b>Bücher in Klasse {0}</b><br />'.format(grade)
    for c in orga.get_classes_by_grade(grade):
        for s in c.student:
            yield '{0}, {1}<br /><ul>'.format(s.person.name, s.person.firstname)
            for l in s.person.loan:
                yield '<li>'
                if l.book.subject is not None:
                    yield '<b>{0}</b>: '.format(l.book.subject.tag)
                yield '{0}</li>'.format(l.book.title)
            yield '</ul><br /><hr /><br />'
    yield '</ul><hr />Fertig'


@get('/admin/lists/generate/bookpending')
def bookpending_generate():
    yield '<b>Ausstehende Bücher:</b><br /><ul>'
    for g in orga.get_grade_range():
        yield '<li>Klasse {0}: '.format(g)
        s = Settings()
        by_books = BookpendingPdf(s)
        by_books.add_books(g)
        fname = by_books.saveToFile(suffix='Klasse{0}-nachBüchern'.format(g))

        yield '<a href="/admin/lists/download/{0}.pdf" target="_blank">nach Büchern</a>, '.format(fname, g)

        s = Settings()
        by_students = BookpendingPdf(s)
        by_students.add_students(g)
        fname = by_students.saveToFile(
            suffix='Klasse{0}-nachSchülern'.format(g))

        yield '<a href="/admin/lists/download/{0}.pdf" target="_blank">nach Schülern</a>'.format(fname, g)
        yield '</li>'

    yield '</ul><hr />Fertig'


@get('/admin/lists/generate/classlist')
def classlist_generate():
    s = Settings()
    classlist = ClassListPdf(s)

    yield 'Lade Klassen...\n'

    classes = list(orga.get_classes())
    orga.sort_classes(classes)
    classlist(classes)
    classlist.saveToFile()

    yield '<pre>%s</pre>\n' % classlist.getPath()
