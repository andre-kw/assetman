from .. import app, log
from xml.etree.ElementTree import Element, ElementTree
from shutil import copyfile
from flask import jsonify, request
import xml.etree.ElementTree as ET
import logging
import requests
import os.path

class Furnidata:
    def __init__(self, xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        roomitemtypes = Furnidata.furnitypes_to_dict(root, 'roomitemtypes')
        wallitemtypes = Furnidata.furnitypes_to_dict(root, 'wallitemtypes')

        self.roomitemtypes = roomitemtypes
        self.wallitemtypes = wallitemtypes

    # helpers
    @staticmethod
    def furnitypes_to_dict(root, tagname):
        obj = {}

        for item in root.findall('./{}/furnitype'.format(tagname)):
            item_dict = {'classname': item.attrib['classname']}
            index = int(item.attrib['id'])

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

            obj[index] = item_dict

        return obj

    # actions
    # TODO: missing 'adurl' and 'customparams' (which are normally empty)
    def save_xml(self):
        root = Element('furnidata')
        rooms = Element('roomitemtypes')
        walls = Element('wallitemtypes')

        for ft_key, ft_dict in self.roomitemtypes.items():
            ft = Element('furnitype')
            ft.set('id', str(ft_key))
            ft.set('classname', ft_dict['classname'])

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

            rooms.append(ft)

        root.append(rooms)
        root.append(walls)
        tree = ElementTree(root)
        tree.write(open(app.config['XML_OUTPUT'], 'wb'), encoding='utf-8', xml_declaration=True)
        
        log.info('::1 Furnidata saved to %s', app.config['XML_OUTPUT'])

        return app.make_response(('', 204))

    @staticmethod
    def download():
        if not os.path.exists('xml'):
            os.mkdir('xml')

        url = app.config['RES_URL'].format('gamedata/furnidata_xml/0')
        res = requests.get(url)

        with open(app.config['XML_INPUT'], 'wb') as f:
            f.write(res.content)

        log.info('::1 Furnidata downloaded successfully')

        return app.make_response(('', 204))

    @staticmethod
    def copy():
        src = app.config['XML_INPUT']
        dst = app.config['XML_OUTPUT']

        if os.path.isfile(src):
            copyfile(src, dst)
            log.info('::1 Copied %s to %s', src, dst)
        else:
            log.warning('::1 File %s does not exist. Please download and try again.', src)

        return app.make_response(('', 204))

    # TODO: key and val should be sanitized
    def search(self, key, val):
        if not key or not val:
            return app.make_response(({'error': 'Missing key and/or val in request body.'}, 400))

        roomitemtypes = []
        wallitemtypes = []

        for k, v in self.roomitemtypes.items():
            if v[key] == val:
                item = {'id': k, 'classname': v['classname'], 'name': v['name']}
                roomitemtypes.append(item)
        for k, v in self.wallitemtypes.items():
            if v[key] == val:
                item = {'id': k, 'classname': v['classname'], 'name': v['name']}
                wallitemtypes.append(item)

        res = {'roomitemtypes': roomitemtypes, 'wallitemtypes': wallitemtypes}

        return app.make_response((res, 200))


    # http verbs
    def get_furnitype(self, type, id):
        dic = self.wallitemtypes if type == 'wall' else self.roomitemtypes
        
        if id in dic:
            res = dic[id]
            res['id'] = str(id)
        else:
            res = {}

        return jsonify(res)

    def patch_furnitype(self, type, id, form):
        dic = self.wallitemtypes if type == 'wall' else self.roomitemtypes

        if id in dic:
            item = dic[id]
            new_item = {}

            for k, v in item.items():
                new_item[k] = form.get(k, v)

            dic[id] = new_item

        return app.make_response(('', 204, {'Location': request.base_url}))

    def post_furnitype(self, type, id, form):
        dic = self.wallitemtypes if type == 'wall' else self.roomitemtypes
        index = str(id)
        item = {}
        partcolors = []

        if id in dic:
            return app.make_response(({'error': 'ID already exists'}, 409))

        item[index] = {
            'bc': request.form.get('bc', '0'),
            'buyout': request.form.get('buyout', '0'),
            'canlayon': request.form.get('canlayon', '0'),
            'cansiton': request.form.get('cansiton', '0'),
            'canstandon': request.form.get('canstandon', '0'),
            'classname': request.form.get('classname', ''),
            'defaultdir': request.form.get('defaultdir', '0'),
            'description': request.form.get('description', ''),
            'excludeddynamic': request.form.get('excludeddynamic', '0'),
            'excludeddynamic': request.form.get('excludeddynamic', '0'),
            'furniline': request.form.get('furniline', ''),
            'id': str(id),
            'name': request.form.get('name', ''),
            'offerid': request.form.get('offerid', '-1'),
            'partcolors': partcolors,
            'rentbuyout': request.form.get('rentbuyout', '0'),
            'rentofferid': request.form.get('rentofferid', '-1'),
            'revision': request.form.get('revision', '1'),
            'specialtype': request.form.get('specialtype', '1'),
            'xdim': request.form.get('xdim', '1'),
            'ydim': request.form.get('ydim', '1')
        }

        dic[id] = item[index]
        
        return app.make_response((item, 201, {'Location': request.base_url}))

    def delete_furnitype(self, type, id):
        dic = self.wallitemtypes if type == 'wall' else self.roomitemtypes

        if id not in dic:
            return app.make_response(({'error': 'ID not found.'}, 404))

        del dic[id]

        return app.make_response(('', 204))

