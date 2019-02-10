#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

from bottle import template
from pony import orm
from db.orm import db, db_session


__author__ = "Christian Glöckner"


def tex_escape(text):
	"""
	:param text: a plain text message
	:return: the message escaped to appear correctly in LaTeX
	"""
	conv = {
		'&': r'\&',
		'%': r'\%',
		'$': r'\$',
		'#': r'\#',
		'_': r'\_',
		'{': r'\{',
		'}': r'\}',
		'~': r'\textasciitilde{}',
		'^': r'\^{}',
		'\\': r'\textbackslash{}',
		'<': r'\textless{}',
		'>': r'\textgreater{}',
	}
	regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
	return regex.sub(lambda match: conv[match.group()], text)

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
