#!/usr/bin/python3
# -*- coding: utf-8 -*-

import loans
import classes
import admin
from app.db import db, db_session
from app.db import orga_queries as orga
from app.db import book_queries as books
from app.db import loan_queries as loans
from pony import orm
from bottle import *
import locale
import sys

from app import Settings


__author__ = "Christian Glöckner"


def main():
    # determine school year and load suitable database

    s = Settings()

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

    run(host='localhost', debug=debug, port=s.data['hosting']['port'])


if __name__ == '__main__':
    main()