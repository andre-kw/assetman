from flask import Flask, cli
import requests
import os.path

#cli.load_dotenv('../.flaskenv')

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.cfg')

from assetextract.models.helpers import Helpers
log = Helpers.get_logger()

from assetextract.models.furnidata import Furnidata

if not os.path.isfile(app.config['XML_INPUT']):
    log.warning('::1 File %s does not exist. Attempting to download...', app.config['XML_INPUT'])
    Furnidata.download()

if not os.path.isfile(app.config['XML_OUTPUT']):
    log.warning('::1 File %s does not exist. Creating...', app.config['XML_OUTPUT'])
    Furnidata.copy()

fd = Furnidata(app.config['XML_INPUT'])

import assetextract.views
