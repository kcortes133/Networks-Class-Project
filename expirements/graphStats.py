import matplotlib.pyplot as plt
from collections import Counter

# compute eccentricity for each node
# count how many times a node shows up in the paths
# count how many times a node type shows up
# compare with what should be the average to see how over/underrepresented the node/type is
def computeEccentricityAllNodes(graph, types=True):
    nodeNames = graph.get_node_ids()
    nodeTypes = graph.get_unique_node_type_names()
    nodeTypeDict = {i: 0 for i in nodeTypes}

    for sourceNode in nodeNames:
        # gives tuple[int, int] if unweighted eccentricity and most distant node id
        eccentricity, distantNode = graph.get_unchecked_eccentricity_and_most_distant_node_id_from_node_id(sourceNode)
        if eccentricity != 0:
            path = graph.get_shortest_path_node_ids_from_node_ids(sourceNode, distantNode)
            for pathNode in path:
                pathNodeType = graph.get_node_type_names_from_node_id(pathNode)
                nodeTypeDict[pathNodeType[0]] +=1
    return nodeTypeDict

def eccentricityPlot(g):
    eccentrocityCount = computeEccentricityAllNodes(g)
    labels = []
    for key in eccentrocityCount.keys():
        labels.append(key.split(':')[-1])

    plt.bar(labels, eccentrocityCount.values())
    plt.xlabel('Node Type')
    plt.ylabel('Number of times in Eccentricity')
    plt.xticks(rotation=15)
    plt.title('Eccentricity Node Type Count')
    plt.show()


#eccentricityPlot()

# could make predictions for diseases of interest
# remove random set of edges (from one type of node) see how predictions change
# how much new information is a model organism providing to the graph

# oblation/removal test
# remove one model organism nodes/edges and see how summary statistics change

def singletonNodes(graph, modelOrgs):
    nodeTypes = graph.get_unique_node_type_names()
    nodeTypeDict = {i: 0 for i in nodeTypes}

    singleNodes = graph.get_singleton_node_ids()
    for s in singleNodes:
        nodeType = graph.get_node_type_names_from_node_id(s)[0]
        nodeTypeDict[nodeType] +=1

    print(nodeTypeDict)
    labels = []
    for key in nodeTypeDict.keys():
        labels.append(key.split(':')[-1])
    plt.bar(labels, nodeTypeDict.values())
    plt.ylabel('Number of Nodes')
    plt.xlabel('Node Type')
    plt.title('Number of Singleton Nodes per Type')
    plt.show()

#singletonNodes(g, modelOrgsNodeNames)

def getComponentsInfo(g):
    components = g.get_node_connected_component_ids()

    componentsCountDict = Counter(components)
    print(g.get_connected_components())
    top = dict(sorted(componentsCountDict.items(), key=lambda item:item[1], reverse=True)[:5])
    print(top)
    nodeIDs = g.get_node_ids()
    nodeTypeComponents = {}
    for node in range(len(components)):
        componentID = components[node]
        if componentID in top:
            nodeID = nodeIDs[node]
            nodeType = g.get_node_type_names_from_node_id(nodeID)[0]
            if nodeType not in nodeTypeComponents:
                nodeTypeComponents[nodeType] = {}
            if componentID in nodeTypeComponents[nodeType]:
                nodeTypeComponents[nodeType][componentID]+=1
            else:
                nodeTypeComponents[nodeType][componentID] = 0
    print(nodeTypeComponents)
    for nodeType in nodeTypeComponents:
        print(nodeTypeComponents[nodeType])


# get nodes in largest component see what type  most are




def plotNodetypeNum(graph, modelOrgs):
    counts = []
    titles = []
    for org in modelOrgs:
        nodeCount = graph.get_node_count_from_node_type_name(org)
        #nodeCount = graph.get_edge_count_from_edge_type_name(org)
        counts.append(nodeCount)
        titles.append(org.split(':')[-1].replace('_', ' '))
    plt.bar(titles, counts)
    #plt.ylabel('Number of Edges')
    plt.ylabel('Number of Nodes')
    #plt.xlabel('Edge type')
    plt.xlabel('Node type')
    #plt.title('Number of Edges per Type')
    plt.title('Number of Nodes per Type')
    plt.xticks(rotation=15)
    plt.show()

    return

