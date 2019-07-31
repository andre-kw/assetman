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

    return res

def post_furnitype(type, id, form):
    dic = fd.wallitemtypes if type == 'wall' else fd.roomitemtypes

    if id in dic:
        item = dic[id]
        new_item = {}

        for k, v in item.items():
            new_item[k] = form.get(k, v)

        dic[id] = new_item

    res = Response({}, status=201)
    res.headers['Location'] = request.base_url
    return res


# routes
@app.route('/furnidata/room/furnitype/<int:id>', methods=['GET', 'POST'])
def route_room_furnitype(id):
    if request.method == 'GET':
        res = jsonify(get_furnitype('room', id))
    elif request.method == 'POST':
        res = post_furnitype('room', id, request.form)

    return res

@app.route('/furnidata/wall/furnitype/<int:id>', methods=['GET', 'POST'])
def route_wall_furnitype(id):
    if request.method == 'GET':
        res = jsonify(get_furnitype('wall', id))
    elif request.method == 'POST':
        res = post_furnitype('wall', id, request.form)

    return res

@app.route('/furnidata', methods=['GET'])
def route_furnidata_actions():
    action = request.args.get('action')
    actions = {
        'save': fd.save_xml
    }

    if actions[action]:
        actions[action]()

    res = Response({}, status=201)
    res.headers['Location'] = request.base_url + '/' + app.config['XML_OUTPUT']

    return res

#@app.route('/furnidata/xml/<string:filename>')
