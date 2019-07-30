from . import app, fd
from flask import request, jsonify
from .models.furnidata import Furnidata

@app.route('/')
def hello():
    return 'hmmm?'

@app.route('/furnidata/room/furnitype/<int:id>', methods=['GET'])
def route_room_furnitype(id):
    if fd.roomitemtypes[id]:
        res = fd.roomitemtypes[id]
        res['id'] = str(id)
    else:
        res = {}

    return jsonify(res)

@app.route('/furnidata/wall/furnitype/<int:id>', methods=['GET'])
def route_wall_furnitype(id):
    if fd.wallitemtypes[id]:
        res = fd.wallitemtypes[id]
        res['id'] = str(id)
    else:
        res = {}

    return jsonify(res)

@app.route('/furnidata', methods=['GET'])
def route_furnidata_actions():
    actions = {
        'save': fd.save_xml
    }
    action = request.args.get('action')

    if actions[action]:
        actions[action]()

    return jsonify({})

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
