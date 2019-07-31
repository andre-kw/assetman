import requests
import json
import logging
from flask import Flask, escape, request, cli

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

# TODO: check if furnidata-habbo.xml exists first
Furnidata.download()
fd = Furnidata('xml/furnidata-habbo.xml')

import assetextract.views
