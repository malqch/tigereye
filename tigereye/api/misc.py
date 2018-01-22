from flask import current_app, request
from flask_classy import FlaskView, route
from tigereye.api import ApiView
from tigereye.helper.code import Code


class MiscView(ApiView):
    route_base = '/'

    def index(self):
        return self.check()

    def check(self):
        current_app.logger.info('checked from %s' % request.remote_addr)
        return 'I am OK'

    def error(self):
        1 / 0