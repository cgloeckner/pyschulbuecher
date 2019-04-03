#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, time
from datetime import datetime

from bottle import *
from pony import orm

from db.orm import db, db_session
from db import orga, books, loans
from utils import errorhandler


__author__ = "Christian Glöckner"



@get('/loan/person/<id:int>')
def loan_person_overview(id):
	p = db.Person[id]
	return "this is a stub"


# TODO: Unit Test

