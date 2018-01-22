from flask import jsonify, request
from flask_classy import FlaskView
from tigereye.models.cinema import Cinema
from tigereye.models.hall import Hall
from tigereye.api import ApiView
from tigereye.helper.code import Code
from tigereye.extensions.validator import Validator, multi_int
from tigereye.models.play import Play
from tigereye.models.movie import Movie

class CinemaView(ApiView):

    def all(self):
        cinemas = Cinema.query.all()
        print(cinemas)
        # data_list = []
        # for c in cinemas:
        #     data = {}
        #     data['name'] = c.name
        #     data['halls'] = c.halls
        #     data['cid'] = c.cid
        #     data['address'] = c.address
        #     data_list.append(data)
        return cinemas
    @Validator(cid=int)
    def get(self):
        cid = request.args['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        return cinema

    @Validator(cid=int)
    def halls(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        # 查询数据库中的hall表，取出所有cid等于当前影院的影厅
        cinema.halls = Hall.query.filter_by(cid=cid).all()
        return cinema

    @Validator(cid=int)
    def plays(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        cinema.plays = Play.query.filter_by(cid=cid).all()
        for play in cinema.plays:
            play.movie = Movie.get(play.mid)
        return cinema
