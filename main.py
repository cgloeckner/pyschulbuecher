#!/usr/bin/python3
# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

from bottle import *
from pony import orm
from db.orm import db, db_session
from db import orga


__author__ = "Christian Glöckner"


debug = True

db.bind('sqlite', 'example.db', create_db=True)
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


import admin, classes

	
run(host='localhost', reloader=True, debug=debug, port=8080)

