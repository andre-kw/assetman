import requests
import json
from xml.etree.ElementTree import Element, ElementTree
from flask import Flask, escape, request

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

from assetextract.models.furnidata import Furnidata

#get_furnidata()
#fd = parse_furnidata('xml/furnidata-habbo.xml')
fd = Furnidata('xml/furnidata-habbo.xml')


import assetextract.views
