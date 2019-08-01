from .. import app, fd
from flask import request, jsonify

class Helpers:
    @staticmethod
    def get_furnitype(type, id):
        dic = fd.wallitemtypes if type == 'wall' else fd.roomitemtypes
        
        if id in dic:
            res = dic[id]
            res['id'] = str(id)
        else:
            res = {}

        return jsonify(res)

    @staticmethod
    def patch_furnitype(type, id, form):
        dic = fd.wallitemtypes if type == 'wall' else fd.roomitemtypes

        if id in dic:
            item = dic[id]
            new_item = {}

            for k, v in item.items():
                new_item[k] = form.get(k, v)

            dic[id] = new_item

        return app.make_response(('', 204, {'Location': request.base_url}))

    @staticmethod
    def post_furnitype(type, id, form):
        dic = fd.wallitemtypes if type == 'wall' else fd.roomitemtypes
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
