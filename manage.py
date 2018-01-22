from flask_script import Manager, Server, Shell
from tigereye.app import create_app
from tigereye.models import db

app = create_app()
manager = Manager(app)

def _make_context():
    from tigereye.models.cinema import Cinema
    from tigereye.models.hall import Hall
    from tigereye.models.movie import Movie
    from tigereye.models.play import Play
    from tigereye.models.seat import Seat, PlaySeat
    from tigereye.models.order import Order
    from tigereye.helper.code import Code
    from tigereye.extensions.validator import Validator
    import redis
    r = redis.Redis()
    locals().update(globals())
    return dict(**locals())

manager.add_command('runserver', Server('127.0.0.1', port=5000))
manager.add_command('shell', Shell(make_context=_make_context))

@manager.command
def createdb():
    from tigereye.models.cinema import Cinema
    from tigereye.models.hall import Hall
    from tigereye.models.movie import Movie
    from tigereye.models.play import Play
    from tigereye.models.seat import Seat, PlaySeat
    from tigereye.models.order import Order
    db.create_all()

@manager.command
def dropdb():
    from tigereye.models.cinema import Cinema
    from tigereye.models.hall import Hall
    from tigereye.models.movie import Movie
    from tigereye.models.play import Play
    from tigereye.models.seat import Seat, PlaySeat
    from tigereye.models.order import Order
    db.drop_all()

@manager.command
def testdata():
    from tigereye.models.cinema import Cinema
    from tigereye.models.movie import Movie
    Cinema.create_test_data()
    Movie.create_test_data()

@manager.command
def init():
    dropdb()
    createdb()
    testdata()

if __name__ == '__main__':
    manager.run()