# -*- coding: utf-8 -*-

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "secretkey_o0*7_fga+^#dhk(s!zm2wbfpgmlb(9^jd_ha32888l6!=w@^3__changeme"

class DevelopmentConfig(Config):
    DEBUG = True 

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    SECRET_KEY = "secretkey_j^bj6y%$1wq2mcs+clvy__%skjyd5dt)tz1w6+q0&dx=sb4w^a_changeme"
