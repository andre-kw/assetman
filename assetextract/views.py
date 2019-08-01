from . import app, fd
from flask import request, jsonify
from .models.furnidata import Furnidata
from .models.helpers import Helpers

@app.route('/')
def hello():
    return 'hmmm?'

@app.route('/furnidata/room/furnitype/<int:id>', methods=['GET', 'PATCH', 'POST', 'DELETE'])
def route_room_furnitype(id):
    if request.method == 'GET':
        res = fd.get_furnitype('room', id)
    elif request.method == 'PATCH':
        res = fd.patch_furnitype('room', id, request.form)
    elif request.method == 'POST':
        res = fd.post_furnitype('room', id, request.form)
    elif request.method == 'DELETE':
        res = fd.delete_furnitype('room', id)

    return res

@app.route('/furnidata/wall/furnitype/<int:id>', methods=['GET', 'PATCH', 'POST', 'DELETE'])
def route_wall_furnitype(id):
    if request.method == 'GET':
        res = fd.get_furnitype('wall', id)
    elif request.method == 'PATCH':
        res = fd.patch_furnitype('wall', id, request.form)
    elif request.method == 'POST':
        res = fd.post_furnitype('wall', id, request.form)
    elif request.method == 'DELETE':
        res = fd.delete_furnitype('wall', id)

    return res

@app.route('/furnidata', methods=['GET'])
def route_furnidata_actions():
    res = ''
    action = request.args.get('action')
    key = request.args.get('key')
    val = request.args.get('val')

    actions = {
        'save': fd.save_xml,
        'download': Furnidata.download,
        'copy': Furnidata.copy,
        'search': lambda: fd.search(key, val)
    }

    if action in actions:
        res = actions[action]()

    return res

#@app.route('/furnidata/xml/<string:filename>')
