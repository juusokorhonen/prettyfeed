# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
from flask import Flask, url_for, render_template, abort
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from jinja2 import TemplateNotFound

def create_app(config=None, configfile=None):
    """
    Creates a Flask app using the provided configuration.

    Keyword arguments:
    :param config:  Config object or None (default: None)
    :param configfile: - Name and path to configfile (default: None)
    :returns: Flask application
    """
    app = Flask(__name__)
    
    # Configure app
    AppConfig(app, default_settings=config, configfile=configfile) # Use of flask-appconfig is highly recommended
    Bootstrap(app) # Use flask-bootstrap

    # Use QRcodes
    from flask.ext.qrcode import QRcode
    QRcode(app)
    
    # Import Blueprints
    #from doifetcher.simple import simple # Use Blueprints
    #app.register_blueprint(simple) # register Frontend blueprint

    # Development-specific functions 
    if (app.debug):
        pass
    # Testing-specifig functions
    if (app.config.get('TESTING')):
        pass
    # Production-specific functions
    if (app.config.get('PRODUCTION')):
        pass

    # Add frontpage
    @app.route('/')
    def welcome_page():
        import time
        import feedparser
        from bs4 import BeautifulSoup
        from unidecode import unidecode
        from string import lower

        rss = feedparser.parse("http://www.aalto.fi/fi/current/news/rss.xml")
        maxEntries = 12 
        rssFormatted = []
        for post in rss.entries[:maxEntries]:
            date_p = post.published_parsed
            date = time.strftime("%d.%m.%Y", date_p)
            category = unidecode(lower(post.category)).split(',')
            # We use BeautifulSoup to strip html from the description
            descSoup = BeautifulSoup(post.description)
            desc = descSoup.getText()
            postDict = {'date': date,
                        'category': category,
                        'title': post.title,
                        'description': desc,
                        'link': post.link}
            rssFormatted.append(postDict)
        try:
            return render_template('index.html', entries=rssFormatted)
        except TemplateNotFound:
            abort(404)

    return app

