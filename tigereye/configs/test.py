from tigereye.configs.default import DefalutConfig


class Testconfig(DefalutConfig):
    TESTING = True
    JSON_SORT_KEYS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'