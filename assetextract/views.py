from . import app, fd
from flask import jsonify

@app.route('/')
def hello():
    return 'hmmm?'

@app.route('/furnitype/<int:id>', methods=['GET'])
def route_furnitype(id):
    res = {}
    node = next((item for item in fd.furnitypes if int(item['id']) == id), False)

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
