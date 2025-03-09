import sys
import shutil
import bottle

from app.db import db, Settings


app = bottle.default_app()


@app.get('/admin/settings')
@bottle.view('admin/settings')
def settings_form():
    s = Settings()

    return dict(s=s)


@app.post('/admin/settings')
def settings_form_post():
    s = Settings()
    current_year = s.data['general']['school_year']

    s = Settings()
    s.data['general']['school_year'] = app.request.forms.school_year
    s.data['deadline']['booklist_changes'] = app.request.forms.deadline_booklist_changes
    s.data['deadline']['booklist_return'] = app.request.forms.deadline_booklist_return
    s.data['deadline']['bookreturn_graduate'] = app.request.forms.bookreturn_graduate
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

    app.redirect('/admin/settings')
