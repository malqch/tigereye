from flask import json
from .helper import FlaskTestCase
from tigereye.helper.code import Code


class TestApiCinema(FlaskTestCase):

    def test_cinema_all(self):
        self.get_succ_json('/cinema/all/')
        # self.assertAlmostEquals(response.status_code, 200)
        # data = json.loads(response.data)
        # print(data)
        # self.assertAlmostEquals(data['rc'], Code.succ.value)

    def test_cinema_halls(self):
        self.assert_get('/cinema/halls/', 400)
        data = self.get_succ_json('/cinema/halls/', cid=1)
        self.assertIsNotNone(data['data'])
