import grape
from ensmallen import Graph
import matplotlib.pyplot as plt
import pandas as pd



def plotTypeNum(titles, counts, plotTitle):
    plt.bar(titles, counts, width=0.95)
    plt.xticks(fontsize=6)
    plt.ylabel('Number of Types')
    plt.xlabel('Type')
    plt.title(plotTitle)
    plt.xticks(rotation=90)
    plt.show()
    return


with open('expirements\eds_vw_3hop_allNodes.csv', 'r') as f:
    lines = f.readline()
    hopNodes = lines.strip().split(',')


# load monarch graph
# calculate centrality measure for whole graph
# calculate centrality nodes for nodes from EDS hops
# compare to rest of graph
folder = 'expirements/monarch20230503/'
g = Graph.from_csv(
    directed=False,
    node_path=folder+'monarch-kg_nodes_EDS_VWsubset.tsv',
    edge_path=folder+'monarch-kg_edges_EDS_VWsubset.tsv',
    node_list_separator=',',
    edge_list_separator=',',
    verbose=True,
    nodes_column='id',
    node_list_node_types_column='category',
    default_node_type='biolink:NamedThing',
    sources_column='subject',
    destinations_column='object',
    edge_list_edge_types_column='predicate',
    name='Monarch KG'
)

def getEdgeandNodeCounts():
    edgeTypes = g.get_unique_edge_type_names()
    nodeTypes = g.get_unique_node_type_names()
    titles = []
    counts = []
    for e in edgeTypes:
        count = g.get_edge_count_from_edge_type_name(e)
        titles.append(e.split(':')[1])
        counts.append(count)
    plotTypeNum(titles, counts, 'Edge Type Counts')

    titles = []
    counts = []
    for n in nodeTypes:
        count = g.get_node_count_from_node_type_name(n)
        titles.append(n.split(':')[1])
        counts.append(count)
    plotTypeNum(titles, counts, 'Node Type Counts')


print(g.report())
#getEdgeandNodeCounts()

def centralityCalc(nodeNames, degreeCent, specificNodes):
    # go through node names and corresponding

    centDict = []
    for node in range(len(nodeNames)):
        nodeName = nodeNames[node]
        if nodeName in specificNodes:
            centDict.append(degreeCent[node])
    s = pd.Series(centDict)
    print(s.describe())
    return

nodeNames = g.get_node_names()
#degreeCent = g.get_degree_centrality()

#centralityCalc(nodeNames, degreeCent, nodeNames)
#centralityCalc(nodeNames, degreeCent, hopNodes)


# intersection nodes
# get degree centrality of the nodes. high or low comparatively
# genes? phenotypes?
# GO enrichment of genes get all hgnc nodes

with open('expirements\HGNC_intersection_nodes_EDS_VW.txt', 'w') as of:
    for node in hopNodes:
        if node.split(':')[0] == 'HGNC':
            of.write(node + '\n')



