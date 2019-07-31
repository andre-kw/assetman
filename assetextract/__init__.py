import requests
import json
import logging
from flask import Flask, escape, request

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.cfg')

if app.config['DEBUG']:
    log_level = logging.DEBUG
elif app.config['ENVIRONMENT'] == 'development':
    log_level = logging.INFO
else:
    log_level = logging.WARNING

logging.basicConfig(level=log_level)


from assetextract.models.furnidata import Furnidata

# TODO: check if furnidata-habbo.xml exists first
Furnidata.download()
fd = Furnidata('xml/furnidata-habbo.xml')

import assetextract.views
