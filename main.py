#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

@get('/classes')
@view('class_index')
def class_index():
	return dict()

@get('/classes/<grade:int>')
@view('grade_list')
def grade_list(grade):
	return dict()


import admin

	
run(host='localhost', reloader=True, debug=debug, port=8080)

