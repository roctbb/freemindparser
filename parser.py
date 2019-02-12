import xml.dom.minidom as minidom
from xml.dom import Node
import json


def process_node(node):
    for child in node.childNodes:
        if child.nodeType != Node.ELEMENT_NODE:
            continue
        if child.tagName == 'node':
            id_from = node.getAttribute('ID')
            id_to = child.getAttribute('ID')
            if id_from:
                export_edges.append({"source": simple_ids[id_from], "target": simple_ids[id_to]})
            process_node(child)


def grade_node(node, level):
    node['level'] += level
    if len(node['visited_inputs']) == len(node['input']):
        for node_number in node['output']:
            if node['id'] not in graph[node_number]['visited_inputs']:
                graph[node_number]['visited_inputs'].append(node['id'])
                grade_node(graph[node_number], node['level'])


def grade_start(node):
    children = list(map(lambda x:graph[x], node['output']))
    if len(children) == 0:
        return 1
    min_node = min(children, key=lambda x:x['level'])
    print(min_node)
    return min_node['level'] - 1


graph = {}
simple_ids = {}

document = 'python-map.mm'

doc = minidom.parse(document)
nodes = doc.getElementsByTagName("node")

number = 500

for node in nodes:
    if node.getAttribute('ID'):
        graph[number] = {
            "id": number,
            "name": node.getAttribute('TEXT'),
            "level": 8,
            "cluster": 0,
            "root": False,
        }
        simple_ids[node.getAttribute('ID')] = number
        number += 1

export_nodes = list(graph.values())
export_edges = []

root_node = nodes[0]
process_node(root_node)


edges = doc.getElementsByTagName("arrowlink")
for edge in edges:
    id = edge.getAttribute('ID')
    parts = id.split('_')
    id_from = parts[2]
    id_to = parts[3]
    export_edges.append({"source": simple_ids[id_from], "target": simple_ids[id_to]})

print(json.dumps({"nodes": export_nodes, "edges": export_edges}))
# for node in start_nodes:
#     grade_node(node, 0)
#
# for node in start_nodes:
#     node['level'] = grade_start(node)
#
# print(graph)
#
# max_node = max(graph.values(), key=lambda x:x['level'])
#
# for level in range(max_node['level']):
#     nodes = list(filter(lambda x:x['level']==level, graph.values()))
#
#     if len(nodes) != 0:
#         print('\nlevel - {}:'.format(level))
#         for node in nodes:
#             print(node['name'])