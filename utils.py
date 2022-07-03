#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

from bottle import template, abort
from pony import orm
from db.orm import db, db_session
from db.utils import shortName

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
        '€': r'\euro',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile(
        '|'.join(
            re.escape(
                str(key)) for key in sorted(
                conv.keys(),
                key=lambda item: -
                len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


def errorhandler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except orm.core.OrmError as e:
            db.rollback()
            abort(400, str(e))
    return wrapper


def bool2str(b: bool):
    return 'Ja' if b else 'Nein'


def bool2checked(b: bool):
    return 'checked' if b else ''
