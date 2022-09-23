from OSMPythonTools.api import Api
api = Api()
node = api.query('node/1659229170')

print(node.tag('name'))