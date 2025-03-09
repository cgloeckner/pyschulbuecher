from bottle import get, post, view, request, redirect
import math
import sys
import shutil

from app.db import db, Settings, DemandManager
from app.utils import errorhandler
from app.tex import *
from app.xls import *


@get('/admin/settings')
@view('admin/settings')
def settings_form():
    s = Settings()

    return dict(s=s)


@post('/admin/settings')
def settings_form_post():
    s = Settings()
    current_year = s.data['general']['school_year']

    s = Settings()
    s.data['general']['school_year'] = request.forms.school_year
    s.data['deadline']['booklist_changes'] = request.forms.deadline_booklist_changes
    s.data['deadline']['booklist_return'] = request.forms.deadline_booklist_return
    s.data['deadline']['bookreturn_graduate'] = request.forms.bookreturn_graduate
    s.save()

    db.commit()

    next_year = s.data['general']['school_year']

    if current_year is not None and (current_year != next_year):
        # copy database for new year
        print('Copying database...')
        shutil.copyfile('data%s.db' % current_year, 'data%s.db' % next_year)
        print('Finished')

        # notify admin about restart
        print('=' * 80)
        print(
            '\nPlease Restart Application and browse http://localhost:8080/admin/advance\n')
        print('=' * 80)
        sys.exit(0)

    redirect('/admin/settings')
