#!/usr/bin/python3
# -*- coding: utf-8 -*-

import loans
import classes
import admin
from db import orga, utils
from db import orga
from db.orm import db, db_session
from pony import orm
from bottle import *
import locale
import sys


__author__ = "Christian Glöckner"


def main():
    # determine school year and load suitable database

    s = utils.Settings()
    try:
        with open('settings.ini') as h:
            s.load_from(h)
    except FileNotFoundError:
        # keep default values
        pass

    debug = True

    db.bind(
        'sqlite',
        'data%s.db' %
        s.data['general']['school_year'],
        create_db=True)
    db.generate_mapping(create_tables=True)

    app = default_app()
    app.catchall = not debug
    app.install(db_session)


    @get('/static/<fname>')
    def static_files(fname):
        return static_file(fname, root='./static')


    @get('/')
    @view('home')
    def landingpage():
        return dict()

    port = 8000
    for val in sys.argv:
        if not val.startswith('--port='):
            continue

        port = int(val.split('--port=')[1])

    run(host='localhost', reloader=True, debug=debug, port=port)


if __name__ == '__main__':
    main()