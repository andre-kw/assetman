from . import app, fd
from flask import request, jsonify, Response
from .models.furnidata import Furnidata

@app.route('/')
def hello():
    return 'hmmm?'

# helpers
def get_furnitype(type, id):
    dic = fd.wallitemtypes if type == 'wall' else fd.roomitemtypes
    
    if id in dic:
        res = dic[id]
        res['id'] = str(id)
    else:
        res = {}

    return jsonify(res)

def patch_furnitype(type, id, form):
    dic = fd.wallitemtypes if type == 'wall' else fd.roomitemtypes

    if id in dic:
        item = dic[id]
        new_item = {}

        for k, v in item.items():
            new_item[k] = form.get(k, v)

        dic[id] = new_item

    return app.make_response(({}, 204, {'Location': request.base_url}))

def post_furnitype(type, id, form):
    dic = fd.wallitemtypes if type == 'wall' else fd.roomitemtypes

    if id in dic:
        #return Response({'error': 'ID already exists.'}, status=409)
        return app.make_response(({'error': 'ID already exists'}, 409))

    item = {
        'bc': request.form.get('bc', '0'),
        'buyout': request.form.get('buyout', '1')
    }
    
    return app.make_response(({}, 201, {'Location': request.base_url}))


# routes
@app.route('/furnidata/room/furnitype/<int:id>', methods=['GET', 'PATCH', 'POST'])
def route_room_furnitype(id):
    if request.method == 'GET':
        res = get_furnitype('room', id)
    elif request.method == 'PATCH':
        res = patch_furnitype('room', id, request.form)
    elif request.method == 'POST':
        res = post_furnitype('room', id, request.form)

    return res

@app.route('/furnidata/wall/furnitype/<int:id>', methods=['GET', 'PATCH', 'POST'])
def route_wall_furnitype(id):
    if request.method == 'GET':
        res = get_furnitype('wall', id)
    elif request.method == 'PATCH':
        res = patch_furnitype('wall', id, request.form)
    elif request.method == 'POST':
        res = post_furnitype('wall', id, request.form)

    return res

@app.route('/furnidata', methods=['GET'])
def route_furnidata_actions():
    action = request.args.get('action')
    actions = {
        'save': fd.save_xml,
        'download': Furnidata.download
    }

    if actions[action]:
        actions[action]()

    return app.make_response(({}, 201))

#@app.route('/furnidata/xml/<string:filename>')
