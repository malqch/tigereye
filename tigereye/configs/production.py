from tigereye.configs.default import DefalutConfig

class ProductionConfig(DefalutConfig):
    DEBUG = False
    JSON_SORT_KEYS = False
    JSON_PRETTYPRINT_REGULAR = False
    SQLALCHEMY_ECHO = False

    EMAIL_HOST = 'smtp.exmail.qq.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'test1@iguye.com'
    EMAIL_HOST_PASSWORD = 'P67844QUssW3'
    EMAIL_USE_SSL = True
    ADMINS = ['15010893029@163.com', '740830230@qq.com']
