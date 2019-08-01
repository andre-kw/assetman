from flask import Flask, escape, request, cli
import requests
import json
import logging
import os.path

#cli.load_dotenv('../.flaskenv')

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.cfg')

def get_logger():
    if app.config['DEBUG']:
        log_level = logging.DEBUG
    elif app.config['ENVIRONMENT'] == 'development':
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    log = logging.getLogger('werkzeug')
    log.setLevel(log_level)

    return log

log = get_logger()


from assetextract.models.furnidata import Furnidata

if not os.path.isfile(app.config['XML_INPUT']):
    log.warning('::1 File {} does not exist. Attempting to download...'.format(app.config['XML_INPUT']))
    Furnidata.download()

if not os.path.isfile(app.config['XML_OUTPUT']):
    log.warning('::1 File {} does not exist. Creating...'.format(app.config['XML_OUTPUT']))
    Furnidata.copy()

fd = Furnidata(app.config['XML_INPUT'])

import assetextract.views
