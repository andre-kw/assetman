import xml.etree.ElementTree as ET
from .. import app

class Furnidata:
    def __init__(self, xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        fd = []

        for item in root.findall('./roomitemtypes/furnitype'):
            item_dict = {'id': item.attrib['id'], 'classname': item.attrib['classname']}

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

            fd.append(item_dict)

        self.furnitypes = fd
        print(fd)


def get_furnidata():
    url = app.config['RES_URL'].format('gamedata/furnidata_xml/0')
    res = requests.get(url)

    with open('xml/furnidata-habbo.xml', 'wb') as f:
        f.write(res.content)

