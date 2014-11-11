# -*- coding: utf-8 -*-

from prettyfeed import create_app
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig

app = create_app(config=DevelopmentConfig)
app.run()
