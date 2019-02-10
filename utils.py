#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bottle import template
from pony import orm
from db.orm import db, db_session


__author__ = "Christian Glöckner"


@db_session
def try_flush():
	try:
		db.flush()
	except orm.core.TransactionIntegrityError as e:
		db.rollback()
		return template('error', error=str(e))
	else:
		return template('success')

def bool2str(b: bool):
	return 'Ja' if b else 'Nein'

def bool2checked(b: bool):
	return 'checked' if b else ''
