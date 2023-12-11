import csv


# list[0] is node name
# list[1] is node type name
import random


def readNodes(mNodesF):
    modelOrganisms = set()
    newF = []
    nodes = []
    notMO = []
    notMO = ['MGI']
    allNodeNames = []
    nodeNames = []
    otherNodes = ['biolink:PhenotypicFeature', 'biolink:Disease', 'biolink:OntologyClass']
    with open(mNodesF, 'r', encoding='utf8') as f:
        rd = csv.reader(f, delimiter='\t')
        c =0
        for row in rd:
            allNodeNames.append(row[0])
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


    print(len(allNodeNames), len(nodes))
    print(len(set(allNodeNames)), len(set(nodes)))
    print(len(set(allNodeNames) & set(nodes)))

    with open('monarch-kg_nodes_all_edited_wO_MGI.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(newF)

    return set(nodes)

def readEdges(edgesF, nodeNames):
    with open(edgesF, 'r', encoding='utf8') as f:
        rd = csv.reader(f, delimiter='\t')
        c = 0
        newEdges = []
        edgeNodeNames = []
        sourceNodes = []
        desNodes = []
        for row in rd:
            if c ==0:
                newEdges.append(row)
            # source and destination must be present
            if row[19] in nodeNames and row[18] in nodeNames:
                edgeNodeNames.append(row[19])
                edgeNodeNames.append(row[18])
                sourceNodes.append(row[19])
                desNodes.append(row[18])
                newEdges.append(row)
            c +=1
    print(len(newEdges))
    print(len(nodeNames))

    for node in edgeNodeNames:
        if node not in nodeNames:
            print('NOPE')


    with open('monarch-kg_edges_all_edited_withO_MGI.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(newEdges)


def change_node_types():
    nodes = []
    with open('monarch-kg_nodes_all_edited_wO_MGI.tsv', 'r', encoding='utf8') as f:
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

    with open('monarch-kg_nodes_nameChange_ALL_woMGI.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(nodes)
    return

def removeRandomEdges(subsetGraphEdges, graphEdgesF, nodeNames):
    # given a graph without a node class
    removedEdges = []
    keptEdges = []
    with open(subsetGraphEdges, 'r', encoding='utf8') as inf:
        rd = csv.reader(inf, delimiter=',')
        c = 0
        sourceNodes = []
        desNodes = []
        m = 0
        for row in rd:
            sourceNodes.append(row[18])
            desNodes.append(row[19])

            if row[18] not in nodeNames or row[19] not in nodeNames:
                print('missing node')
                m+=1
            # count number of edges with type interacts_with, associated_with, has_phenotype
            if row[2] == 'biolink:has_phenotype' or row[2] == 'biolink:interacts_with' \
                    or row[2] == 'biolink:associated_with':
                if row[18].split(':')[0] == 'HGNC' or row[19].split(':')[0] == 'HGNC':
                    # randomly remove 10% of the edges
                    # keep list of removed edges
                    if random.randint(0,9) < 2:
                        removedEdges.append(row)
                    else:
                        keptEdges.append(row)
                    c+=1
                else:
                    keptEdges.append(row)
            else:
                keptEdges.append(row)

    print(m)
    # edit graphs with and without node class to not have list of edges
    graphFile = open(graphEdgesF, 'r')
    graphEdges = list(csv.reader(graphFile, delimiter='\t'))
    graphFile.close()
    #print(len(graphEdges))
    for edge in removedEdges:
        graphEdges.remove(edge)
    #resEdges = list(filter(lambda i: i not in removedEdges, graphEdges))
    #print(len(resEdges))

    # keep list of removed edges
    # output graphs
    # return list of removed edges
    #print(len(removedEdges))
    return removedEdges, keptEdges, graphEdges

def writeRemovedEdgeFiles(folder, removedE, keptE, resE):
    with open(folder+'removedEdges.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(removedE)

    with open(folder+'keptEdges.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(keptE)

    with open(folder + 'resEdges.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(resE)

folder = 'editedMonarchGraphs/'
mEdgesF = 'monarch-kg_edges.tsv'
mNodesF = 'monarch-kg_nodes.tsv'
nodeNames = readNodes(mNodesF)
#readEdges(mEdgesF, nodeNames)
#change_node_types()


# randomly remove edges and keep list of those removed
# remove edges that are of type
organismFolder = folder + 'graphsEdgesRemoved/MGI_withOC/HGNC_edges'
subGraph = 'monarch-kg_edges_all_edited_withO_MGI.tsv'
graph = 'monarch-kg_edges.tsv'
removedEdges, keptEdges, resEdges = removeRandomEdges(subGraph, graph, nodeNames)
writeRemovedEdgeFiles(organismFolder, removedEdges, keptEdges, resEdges)

def line_prepender(filename, headerF):
    with open(headerF, 'r') as hf:
        header = hf.readline()

    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(header.rstrip('\r\n') + '\n' + content)

line_prepender(organismFolder+'removedEdges.tsv', organismFolder+'resEdges.tsv')


# look at intersection of nodes in edges file (source and destination)
    # orginal nodes and edges file as well as edited one