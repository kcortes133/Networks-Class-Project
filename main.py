from ensmallen import Graph
import connectionTypes, edgePrediction, graphStats, centralityMeasures


g = Graph.from_csv(
    directed=False,
    node_path='monarch-kg_nodes_nameChange_withHGNC.tsv',
    edge_path='monarch-kg_edges_edited_withHGNC.tsv',
    verbose=True,
    nodes_column='id',
    node_list_node_types_column='category',
    default_node_type='biolink:NamedThing',
    sources_column='subject',
    destinations_column='object',
    edge_list_edge_types_column='predicate',
    name='Monarch KG'
)

g = g.remove_singleton_nodes()
edgeTypes = g.get_unique_edge_type_names()
nodeTypes = g.get_unique_node_type_names()
allNodeIDs = g.get_node_ids()
allNodeNames = g.get_node_names()

nodeTypeIDsDict = {i: [] for i in nodeTypes}
for node in allNodeIDs:
    nodeType = g.get_node_type_names_from_node_id(node)[0]
    nodeTypeIDsDict[nodeType].append(node)



print(nodeTypes)

#topNodes = g.get_top_k_central_node_names(10)
#print(topNodes)

print(g.report())

# return new graph with defined attributes
# filter_from_names

#nodeDegrees = g.get_node_degrees

# Could edit edges and nodes to get rid of non phenotype, non model organism, non disease nodes, and all connecting edges

#modelOrgsNodeNames = ['biolink:Gene:ZFIN', 'biolink:Gene:Xenbase', 'biolink:Gene:WB', 'biolink:Gene:SGD', 'biolink:Gene:RGD', 'biolink:Gene:MGI', 'biolink:Gene:FB',
#                      'biolink:Gene:PomBase', 'biolink:Gene:dictyBase']
modelOrgsNodeNames = ['biolink:Gene:ZFIN', 'biolink:Gene:Xenbase', 'biolink:Gene:WB', 'biolink:Gene:SGD', 'biolink:Gene:RGD', 'biolink:Gene:MGI', 'biolink:Gene:FB',
                      'biolink:Gene:dictyBase', 'biolink:Gene:PomBase']
modelOrgs = ['ZFIN', 'Xenbase', 'WB', 'SGD', 'RGD', 'MGI', 'FB', 'PomBase', 'dictyBase']

# compute eccentricity for each node
# count how many times a node shows up in the paths
# count how many times a node type shows up
# compare with what should be the average to see how over/underrepresented the node/type is

#graphStats.eccentricityPlot(g)
#graphStats.plotNodetypeNum(g, modelOrgsNodeNames)
#graphStats.getComponentsInfo(g)

#centralityMeasures.centralityPlot(g, modelOrgs)
#centralityMeasures.harmonicCentralityPlot(g, modelOrgs)
#centralityMeasures.betweenessCentralityPlot(g, modelOrgs)

# could make predictions for diseases of interest
# remove random set of edges (from one type of node) see how predictions change
# how much new information is a model organism providing to the graph

# oblation/removal test
# remove one model organism nodes/edges and see how summary statistics change

# get information about edges per node type
#connectionTypes.edgeTypes(g, nodeTypes)

# get nodes for each gene type
# get edge types for nodes of each type

edgePrediction.pickEmbedding(g)

#edgePrediction.graphEmbedding(g)
#edgePrediction.embeddingResults(df, cosSims, g)

#g.get_edge_prediction_metrics()