from . import app, fd
from flask import request, jsonify
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


# routes
@app.route('/furnidata/room/furnitype/<int:id>', methods=['GET'])
def route_room_furnitype(id):
    if request.method == 'GET':
        res = get_furnitype('room', id)

    return jsonify(res)


@app.route('/furnidata/wall/furnitype/<int:id>', methods=['GET'])
def route_wall_furnitype(id):
    if request.method == 'GET':
        res = get_furnitype('wall', id)

    return jsonify(res)

@app.route('/furnidata', methods=['GET'])
def route_furnidata_actions():
    action = request.args.get('action')
    actions = {
        'save': fd.save_xml
    }

    if actions[action]:
        actions[action]()

    return jsonify({})

