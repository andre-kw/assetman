import requests
import json
import xml.etree.ElementTree as ElementTree
from flask import Flask, escape, request

dcr_url = 'http://habboo-a.akamaihd.net/dcr/hof_furni/{}'
res_url = 'https://habbo.com/{}'

def get_furnidata():
    url = res_url.format('gamedata/furnidata_xml/0')
    res = requests.get(url)

    with open('xml/furnidata-habbo.xml', 'wb') as f:
        f.write(res.content)

def parse_furnidata(xmlfile):
    tree = ElementTree.parse(xmlfile)
    root = tree.getroot()

    fd = []

    for item in root.findall('./roomitemtypes/furnitype'):
        item_dict = {'id': item.attrib['id'], 'classname': item.attrib['classname']}

        for child in item:
            if(child.text):
                item_dict[child.tag] = child.text

        fd.append(item_dict)

    return fd



#get_furnidata()
fd = parse_furnidata('xml/furnidata-habbo.xml')

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hmmm?'

@app.route('/furnitype/<int:id>')
def get_furnitype(id):
    #node = list(filter(lambda furnitype: furnitype['id'] == id, fd))
    node = next((item for item in fd if int(item['id']) == id), False)
    print(node)

    if node:
        res = json.dumps(node)
        return res

    return 'didnt find it'

# TODO: figure out GET and POSTs
#@app.route('/furnitype/<int:id>/<str:attribute>')
