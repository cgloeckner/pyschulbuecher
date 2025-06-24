import bottle

from app import db, db_session, Settings


__author__ = 'Christian Glöckner'
__version__ = 'v0.2.1'


def main(debug: bool = True) -> None:
    s = Settings()
    year = s.data['general']['school_year']
    port = s.data['hosting']['port']

    db.bind('sqlite', f'data{year}.db', create_db=True)
    db.generate_mapping(create_tables=True)

    app = bottle.default_app()
    app.catchall = not debug
    app.install(db_session)

    @app.get('/static/<fname>')
    def static_files(fname):
        return bottle.static_file(fname, root='./static')

    @app.get('/')
    @bottle.view('home')
    def landingpage():
        return dict()

    import app.routes
    
    bottle.run(host='localhost', debug=debug, port=port)


if __name__ == '__main__':
    main()