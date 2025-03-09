import bottle

from pony import orm

from app import db


def errorhandler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except orm.core.OrmError as e:
            db.rollback()
            bottle.app.abort(400, str(e))
    return wrapper
