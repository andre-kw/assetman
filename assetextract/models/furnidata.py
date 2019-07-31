from .. import app, log
from xml.etree.ElementTree import Element, ElementTree
import xml.etree.ElementTree as ET
import logging

class Furnidata:
    def __init__(self, xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        roomitemtypes = Furnidata.furnitypes_to_dict(root, 'roomitemtypes')
        wallitemtypes = Furnidata.furnitypes_to_dict(root, 'wallitemtypes')

        self.roomitemtypes = roomitemtypes
        self.wallitemtypes = wallitemtypes

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
        
        log.info('Furnidata saved to {}'.format(app.config['XML_OUTPUT']))
        return True

    @staticmethod
    def download():
        url = app.config['RES_URL'].format('gamedata/furnidata_xml/0')
        log.info('Attempting to download furnidata from {}'.format(url))

        """
        res = requests.get(url)

        with open('xml/furnidata-habbo.xml', 'wb') as f:
            f.write(res.content)
        """

