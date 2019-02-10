#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bottle import *
from pony import orm
from db.orm import db, db_session, Currency
from db import orga, books
from utils import try_flush


__author__ = "Christian Glöckner"


@get('/admin/subjects')
@view('admin/subjects_index')
def subjects_index():
	return dict()

@post('/admin/subjects/add')
def subjects_add_post():
	for line in request.forms.data.split('\n'):
		tag, name = line.split('\t')
		db.Subject(name=name, tag=tag)
	return try_flush()

@get('/admin/subjects/edit/<id:int>')
@view('admin/subjects_edit')
def subjects_edit_form(id):
	return dict(s=db.Subject[id])

@post('/admin/subjects/edit/<id:int>')
def subjects_edit_post(id):
	s = db.Subject[id]
	s.tag = request.forms.tag
	s.name = request.forms.name
	return try_flush()

@post('/admin/subjects/delete/<id:int>')
def subjects_delete(id):
	db.Subject[id].delete()
	return try_flush()

# -----------------------------------------------------------------------------

@get('/admin/publishers')
@view('admin/publishers_index')
def publishers_index():
	return dict()

@post('/admin/publishers/add')
def publishers_add_post():
	for name in request.forms.data.split('\n'):
		db.Publisher(name=name)
	return try_flush()

@get('/admin/publishers/edit/<id:int>')
@view('admin/publishers_edit')
def publishers_edit_form(id):
	return dict(p=db.Publisher[id])

@post('/admin/publishers/edit/<id:int>')
def publishers_edit_post(id):
	p = db.Publisher[id]
	p.name = request.forms.name
	return try_flush()

@post('/admin/publishers/delete/<id:int>')
def publishers_delete(id):
	db.Publisher[id].delete()
	return try_flush()

# -----------------------------------------------------------------------------

@get('/admin/books')
@view('admin/books_index')
def books_index():
	return dict()

@post('/admin/books/add')
def books_add_post():
	books.addBooks(request.forms.data)
	return try_flush()

@get('/admin/books/edit/<id:int>')
@view('admin/books_edit')
def books_edit_form(id):
	return dict(b=db.Book[id])

@post('/admin/books/edit/<id:int>')
def books_edit_post(id):
	b = db.Book[id]
	b.title   = request.forms.title
	b.isbn    = request.forms.isbn
	b.price   = Currency.fromString(request.forms.price)
	b.publisher = db.Publisher[int(request.forms.publisher_id)]
	b.stock     = int(request.forms.stock)
	b.inGrade   = int(request.forms.inGrade)
	b.outGrade  = int(request.forms.outGrade)
	b.subject   = db.Subject[int(request.forms.subject_id)] if request.forms.subject_id != "" else None
	b.novices   = True if request.forms.novices   == 'on' else False
	b.advanced  = True if request.forms.advnaced  == 'on' else False
	b.workbook  = True if request.forms.workbook  == 'on' else False
	b.classsets = True if request.forms.classsets == 'on' else False
	b.comment   = request.forms.comment
	return try_flush()

@post('/admin/books/delete/<id:int>')
def books_delete(id):
	db.Book[id].delete()
	return try_flush()

