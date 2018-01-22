from flask import current_app
from tigereye.models import db, Model
"""
    ID
    名称
    语言
    字幕
    上映日期
    版本（2D/3D/4D）
    模式（胶片/数字）
    屏幕尺寸
    简介
    状态
"""

class Movie(db.Model, Model):
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    language = db.Column(db.String(32))
    subtitle = db.Column(db.String(32))
    show_date = db.Column(db.Date)
    vision = db.Column(db.String(16))
    model = db.Column(db.String(16))
    screen_size = db.Column(db.String(16))
    introduction = db.Column(db.Text)
    status = db.Column(db.Integer, default=0, nullable=False, index=True)


    # def __json__(self):
    #     keys = vars(self).keys()
    #     data = {}
    #     for key in keys:
    #         if not key.startswith('_'):
    #             data[key] = getattr(self, key)
    #     return data

            # def __dict__(self):
            #     return self.__json__()

    @classmethod
    def create_test_data(cls, num=10):
        for i in range(1, num + 1):
            m = Movie()
            m.mid = i
            m.sn = str(i).zfill(10)
            m.name = '无问西东%s' % i
            m.language = '英文'
            m.subtitle = '中文'
            # m.show_date =
            m.mode = '数字'
            m.vision = '2D'
            m.screen_size = 'IMAX'
            m.introduction = 'blahblah哈哈'
            m.status = 1
            db.session.add(m)
        db.session.commit()
        current_app.logger.info('movie test data done!')
