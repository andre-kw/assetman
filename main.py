import requests
import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree
from flask import Flask, escape, request, jsonify

dcr_url = 'http://habboo-a.akamaihd.net/dcr/hof_furni/{}'
res_url = 'https://habbo.com/{}'

def get_furnidata():
    url = res_url.format('gamedata/furnidata_xml/0')
    res = requests.get(url)

    with open('xml/furnidata-habbo.xml', 'wb') as f:
        f.write(res.content)

def parse_furnidata(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    fd = []

    for item in root.findall('./roomitemtypes/furnitype'):
        item_dict = {'id': item.attrib['id'], 'classname': item.attrib['classname']}

        for child in item:
            if(child.text):
                item_dict[child.tag] = child.text
            elif(child):
                subitems = []

                for subchild in child:
                    subitem_dict = {}
                    subitem_dict[subchild.tag] = subchild.text
                    subitems.append(subitem_dict)

                item_dict[child.tag] = subitems

        fd.append(item_dict)

    return fd



#get_furnidata()
fd = parse_furnidata('xml/furnidata-habbo.xml')

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hmmm?'

@app.route('/furnitype/<int:id>', methods=['GET'])
def route_furnitype(id):
    res = {}
    node = next((item for item in fd if int(item['id']) == id), False)

    if node:
        res = node

    return jsonify(res)


#@app.route('/furnitype/<int:id>/<string:attribute>')


# TODO: missing 'adurl' and 'customparams' (which are normally empty)
@app.route('/xml/save')
def route_xml_save():
    root = Element('furnidata')
    rooms = Element('roomitemtypes')
    walls = Element('wallitemtypes')

    for ft_dict in fd:
        ft = Element('furnitype')

        for key, val in ft_dict.items():
            if(key != 'id' and key != 'classname'):
                child = Element(key)

                if(isinstance(val, list)):
                    for d in val:
                        for k, v in d.items():
                            subchild = Element(k)
                            subchild.text = v
                            child.append(subchild)
                else:
                    child.text = val

                ft.append(child)
            else:
                ft.set(key, val)

        rooms.append(ft)
        #print(ft)

    root.append(rooms)
    root.append(walls)
    tree = ElementTree(root)
    tree.write(open('xml/furnidata-sea.xml', 'wb'), encoding='utf-8', xml_declaration=True)

    return 'hey'
