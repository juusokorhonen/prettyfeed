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

    # Add custom filter to jinja
    app.jinja_env.filters['expandlist'] = _jinja2_filter_expandlist

    # Add frontpage
    @app.route('/')
    @app.route('/feed/<int:feed_index>')
    @app.route('/feed/<feed_link>')
    def feed_page(feed_link=None, feed_index=None):
        import time
        import feedparser
        from bs4 import BeautifulSoup
        from unidecode import unidecode
        from string import lower

        if not feed_index:
            try:
                if not feed_link:
                    # No feed link was provided, so show the first one
                    feed_index = 0
                else:
                    # Try to extract the feed link number
                    feed_index = [x[1] for x in app.config.get('FEEDS')].index(feed_link)
            except ValueError as ve:
                abort(404)
            except Exception as e:
                print(e)
                import traceback
                print(traceback.format_exc())
                feed_index = 0

        try:
            feedDesc, feedLink, feedURL = app.config.get('FEEDS')[feed_index]
        except:
            #feedDesc, feedLink, feedURL = ('Test Feed', 'test_feed', 'http://feedparser.org/docs/examples/atom10.xml')
            abort(404)

        rss = feedparser.parse(feedURL)

        maxEntries = 12 
        rssFormatted = []
        for post in rss.entries[:maxEntries]:
            date_p = post.published_parsed
            date = time.strftime("%d.%m.%Y", date_p)
            
            catstr = unidecode(lower(post.category))
            for fr,to in [(u"tutkimus", u"research"),
                          (u"palkitut", u"honored"),
                          (u"opiskelu", u"studies"),
                          (u"yhteistyo", u"cooperation"),
                          (u"muut", u"other")]:
                catstr = catstr.replace(fr, to)
            category = catstr.split(',')

            # We use BeautifulSoup to strip html from the description
            descSoup = BeautifulSoup(post.description)
            desc = descSoup.getText()
            postDict = {'date': date,
                        'category': category,
                        'category_unformatted': post.category.replace(u",", u", "),
                        'title': post.title,
                        'description': desc,
                        'link': post.link}
            rssFormatted.append(postDict)
        try:
            return render_template('index.html', entries=rssFormatted)
        except TemplateNotFound:
            abort(404)

    return app

def _jinja2_filter_expandlist(data):
    if data:
        if (not isinstance(data, basestring)):
            delimiter = u""
            datastr = u""
            for d in data:
                datastr = u"{}{}{}".format(datastr, delimiter, unicode.title(d))
                delimiter = u", "
            return datastr
        else:
            return unicode.title(data)
    else: 
        return None
