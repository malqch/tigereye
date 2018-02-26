from flask import jsonify
from flask_classy import FlaskView
from tigereye.models.movie import Movie
from tigereye.api import ApiView
from tigereye.helper.code import Code


class MovieView(ApiView):

    def all(self):
        return Movie.query.all()
        # print(movies)
        # data_list = []
        # for m in movies:
        #     data = {}
        #     data['name'] = m.name
        #     data['halls'] = m.halls
        #     data['cid'] = m.cid
        #     data['address'] = m.address
        #     data_list.append(data)
        # return movies


