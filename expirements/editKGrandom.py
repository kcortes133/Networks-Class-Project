# Author: Katherina Cortes
# Date: 5/23/2024
# Purpose: remove nodes of specified types from Monarch KG, as well as random edges for
#   testing
import csv
import os.path
import random


###
# remove nodes of nonspecified types
# @param mNodesF: file of all nodes in graph
# @param keepNodeTypes: list of node types to keep in new graph
# @param excludeModeOrganismType: list of model organisms to exclude
# @returns set of node names in new graph
# @outputs a file of nodes in new graph with their metadata
###
def removeSpecifiedNodeTypes(mNodesF, newNodesF, keepNodeTypes, excludeModelOrganismType):
    newF = []
    nodes = []
    allNodeNames = []
    with open(mNodesF, 'r', encoding='utf8') as f:
        rd = csv.reader(f, delimiter='\t')
        c =0
        for row in rd:
            allNodeNames.append(row[0])
            # keep column headings
            if c ==0:
                newF.append(row)

            # only keep model organism nodes
            # exclude specified model organism(s)
            if row[1] =='biolink:Gene' and row[0].split(':')[0] not in excludeModelOrganismType:
                newF.append(row)
                nodes.append(row[0])

            # keep other specified node types
            if row[1] in keepNodeTypes:
                newF.append(row)
                nodes.append(row[0])

            c+=1

    # write new nodes and metadata to specified file as tsv
    with open(newNodesF, 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(newF)

    return set(nodes)


###
# keep only edges connected to two nodes still in new graph
# remove floating edges
# @param edgesF: file containing all edges from originl graph
# @param newEdgesF: file to put edges for new graph
# @param nodeNames: list of node names in new graph
# @output newEdgesF: file of new edges and metadata
###
def removeExtraEdges(edgesF, newEdgesF, nodeNames):
    with open(edgesF, 'r', encoding='utf8') as f:
        rd = csv.reader(f, delimiter='\t')
        c = 0
        newEdges = []
        for row in rd:
            # keep edge file header
            if c ==0:
                newEdges.append(row)
            # source and destination nodes must both be present
            if row[18] in nodeNames and row[17] in nodeNames:
                newEdges.append(row)
            c +=1

    # print kept edges to file
    with open(newEdgesF, 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(newEdges)
    return


# change node names to reflect model organism
# @param nodesF: new nodes of specified types from removeSpecifiedNodeTypes()
# @output newNodeNamesF: file of nodes with new names and metadata
def change_node_types(nodesF, newNodeNamesF):
    nodes = []
    with open(nodesF, 'r', encoding='utf8') as f:
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

    with open(newNodeNamesF, 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(nodes)
    return


###
# @param subsetGraphEdges: file of all edges in new graph
# @param graphEdgesF: file of all edges in original graph
# @return
# @return
# @return
###
def removeRandomEdges(subsetGraphEdges, graphEdgesF):
    # given a graph without a node class
    removedEdges = []
    keptEdges = []
    with open(subsetGraphEdges, 'r', encoding='utf8') as inf:
        rd = csv.reader(inf, delimiter=',')
        c = 0
        sourceNodes = []
        desNodes = []
        for row in rd:
            sourceNodes.append(row[17])
            desNodes.append(row[18])

            # count number of edges with type interacts_with, associated_with, has_phenotype
            if row[2] == 'biolink:has_phenotype' or row[2] == 'biolink:interacts_with' \
                    or row[2] == 'biolink:associated_with':
                if row[17].split(':')[0] == 'HGNC' or row[18].split(':')[0] == 'HGNC':
                    # randomly remove 10% of the edges
                    # keep list of removed edges
                    if random.randint(0,9) < 1:
                        removedEdges.append(row)
                    else:
                        keptEdges.append(row)
                    c+=1
                else:
                    keptEdges.append(row)
            else:
                keptEdges.append(row)

    #edit original graph to remove same set of edges for comparison purposes
    graphFile = open(graphEdgesF, 'r')
    graphEdges = list(csv.reader(graphFile, delimiter='\t'))
    graphFile.close()

    #for edge in removedEdges:
    #    graphEdges.remove(edge)

    graphEdgesSet = set(map(tuple, graphEdges))
    removedEdgesSet = set(map(tuple, removedEdges))

    newGraphEdges = graphEdgesSet - removedEdgesSet
    newGraphEdges = list(map(list, newGraphEdges))



    #newGraphEdges = [x for x in graphEdges if x not in removedEdges]

    # list of removed edges
    # list of new graphs kept edges
    # list of original graphs kept edges
    return removedEdges, keptEdges, newGraphEdges

def writeRemovedEdgeFiles(folder, removedE, keptE, resE):
    # removed edges
    with open(folder+'removedEdges.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(removedE)

    # edges kept in new graph
    with open(folder+'keptEdges.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(keptE)

    # edges kept in original graph
    with open(folder + 'resEdges.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(resE)
    return


folder = 'editedMonarchGraphs/'
kgFolder = 'expirements/monarch20231028/'
mEdgesF = kgFolder + 'monarch-kg_edges.tsv'
mNodesF = kgFolder + 'monarch-kg_nodes.tsv'
newNodesF = kgFolder + 'monarch-kg_nodes_all_edited.tsv'
newEdgesF = kgFolder + 'monarch-kg_edges_all_edited.tsv'
newNodeNamesF = kgFolder + 'monarch-kg_nodes_nameChange_all.tsv'

keepNodes = ['biolink:PhenotypicFeature', 'biolink:Disease', 'biolink:OntologyClass']
excludeMO = ['']
nodeNames = removeSpecifiedNodeTypes(mNodesF, newNodesF, keepNodes, excludeMO)

removeExtraEdges(mEdgesF, newEdgesF, nodeNames)

change_node_types(newNodesF, newNodeNamesF)

# randomly remove edges and keep list of those removed
# remove edges that are of type
organismFolder = kgFolder + 'graphsEdgesRemoved/MGI_withOC/HGNC_edges'
subGraph = kgFolder + 'monarch-kg_edges_all_edited_withO_Xenbase.tsv'
graph = kgFolder + 'monarch-kg_edges.tsv'
if not os.path.exists(organismFolder):
    os.makedirs(organismFolder)
removedEdges, keptEdges, resEdges = removeRandomEdges(subGraph, graph)
writeRemovedEdgeFiles(organismFolder, removedEdges, keptEdges, resEdges)

# fix file headers
#def line_prepender(filename, headerF):
#    with open(headerF, 'r') as hf:
#        header = hf.readline()

#    with open(filename, 'r+') as f:
#        content = f.read()
#        f.seek(0, 0)
#        f.write(header.rstrip('\r\n') + '\n' + content)

#line_prepender(organismFolder+'removedEdges.tsv', organismFolder+'resEdges.tsv')


# look at intersection of nodes in edges file (source and destination)
# orginal nodes and edges file as well as edited one
