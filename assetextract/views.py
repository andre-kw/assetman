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
        res = Helpers.get_furnitype('room', id)
    elif request.method == 'PATCH':
        res = Helpers.patch_furnitype('room', id, request.form)
    elif request.method == 'POST':
        res = Helpers.post_furnitype('room', id, request.form)
    elif request.method == 'DELETE':
        res = Helpers.delete_furnitype('room', id)

    return res

@app.route('/furnidata/wall/furnitype/<int:id>', methods=['GET', 'PATCH', 'POST', 'DELETE'])
def route_wall_furnitype(id):
    if request.method == 'GET':
        res = Helpers.get_furnitype('wall', id)
    elif request.method == 'PATCH':
        res = Helpers.patch_furnitype('wall', id, request.form)
    elif request.method == 'POST':
        res = Helpers.post_furnitype('wall', id, request.form)
    elif request.method == 'DELETE':
        res = Helpers.delete_furnitype('wall', id)

    return res

@app.route('/furnidata', methods=['GET'])
def route_furnidata_actions():
    action = request.args.get('action')
    actions = {
        'save': fd.save_xml,
        'download': Furnidata.download,
        'copy': Furnidata.copy
    }

    if actions[action]:
        actions[action]()

    return app.make_response(('', 204))

#@app.route('/furnidata/xml/<string:filename>')
