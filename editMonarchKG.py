import csv


# list[0] is node name
# list[1] is node type name
def readNodes(mNodesF):
    modelOrganisms = set()
    newF = []
    nodes = []
    notMO = ['NCBIGene']

    otherNodes = ['biolink:PhenotypicFeature', 'biolink:Disease', 'biolink:OntologyClass']
    with open(mNodesF, 'r', encoding='utf8') as f:
        rd = csv.reader(f, delimiter='\t')
        c =0
        for row in rd:
            if c ==0:
                newF.append(row)
            # only keep model organism nodes
            if row[1] =='biolink:Gene' and row[0].split(':')[0] not in notMO:
                newF.append(row)
                nodes.append(row[0])
                modelOrganisms.add(row[0].split(':')[0])
            c+=1
            if row[1] in otherNodes:
                newF.append(row)
                nodes.append(row[0])

    with open('monarch-kg_nodes_edited_withHGNC.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(newF)

    return set(nodes)

def readEdges(edgesF, nodeNames):
    with open(edgesF, 'r', encoding='utf8') as f:
        rd = csv.reader(f, delimiter='\t')
        c = 0
        newEdges = []
        for row in rd:
            if c ==0:
                newEdges.append(row)
            if row[19] in nodeNames and row[18] in nodeNames:
                newEdges.append(row)
            c +=1
    print(len(newEdges))
    with open('monarch-kg_edges_edited_withHGNC.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(newEdges)


def change_node_types():
    nodes = []
    with open('monarch-kg_nodes_edited_withHGNC.tsv', 'r', encoding='utf8') as f:
        rd = csv.reader(f, delimiter=',')
        c = 0
        for row in rd:
            if c == 0:
                nodes.append(row)
            else:
                nodeType = row[1]
                nodeName = row[0]
                if nodeType.split(':')[1] == 'Gene':
                    newNodeType = nodeType + ':' + nodeName.split(':')[0]
                    row[1] = newNodeType
                    nodes.append(row)
                else:
                    nodes.append(row)
            c+=1

    with open('monarch-kg_nodes_nameChange_withHGNC.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(nodes)
    return


mEdgesF = 'monarch-kg_edges.tsv'
mNodesF = 'monarch-kg_nodes.tsv'
nodeNames = readNodes(mNodesF)
readEdges(mEdgesF, nodeNames)
change_node_types()