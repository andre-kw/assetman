import requests
import xml.etree.ElementTree as ElementTree

dcr_url = 'http://habboo-a.akamaihd.net/dcr/hof_furni/{}'
res_url = 'https://habbo.com/{}'

def get_furnidata():
    url = res_url.format('gamedata/furnidata_xml/0')
    res = requests.get(url)

    with open('xml/furnidata-habbo.xml', 'wb') as f:
        f.write(res.content)

def parse_furnidata(xmlfile):
    tree = ElementTree.parse(xmlfile)
    root = tree.getroot()

    for item in root.findall('./roomitemtypes/furnitype'):
        print(item)



#get_furnidata()
parse_furnidata('xml/furnidata-habbo.xml')
