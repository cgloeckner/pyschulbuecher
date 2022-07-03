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
locale.setlocale(locale.LC_ALL, 'de_DE')


__author__ = "Christian Glöckner"


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


run(host='localhost', reloader=True, debug=debug, port=8000)
