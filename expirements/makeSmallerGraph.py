import csv, random


def readNodes(mNodesF, subsetNodes, folder):
    newF = []
    nodes = []
    allNodeNames = []
    with open(mNodesF, 'r', encoding='utf8') as f:
        rd = csv.reader(f, delimiter='\t')
        c =0
        for row in rd:
            allNodeNames.append(row[0])
            if c ==0:
                newF.append(row)
            # only keep model organism nodes
            if row[0] in subsetNodes:
                newF.append(row)
                nodes.append(row[0])
            c+=1

    print(len(newF))
    with open(folder+'monarch-kg_nodes_EDS_VWsubset.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(newF)

    return set(nodes)

def readEdges(edgesF, nodeNames, folder):
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

    with open(folder + 'monarch-kg_edges_EDS_VWsubset.tsv', 'w', encoding='utf8', newline='') as of:
        writer = csv.writer(of)
        writer.writerows(newEdges)


with open('expirements\eds_vw_3hop_allNodes.csv', 'r') as f:
    lines = f.readline()
    hopNodes = set(lines.strip().split(','))
    print(len(hopNodes))

folder = 'expirements/monarch20231028/'
mEdgesF = folder + 'monarch-kg_edges.tsv'
mNodesF = folder + 'monarch-kg_nodes.tsv'
nodeNames = readNodes(mNodesF, hopNodes, folder)
print(len(nodeNames))
readEdges(mEdgesF, nodeNames, folder)
