import grape
from ensmallen import Graph
import connectionTypes, edgePrediction, graphStats, centralityMeasures, multimodalGCN, embedding
import graphFunctions

edgeFolder = 'editedMonarchGraphs/graphsEdgesRemoved/MGI_withOC/'
nodesFolder = 'editedMonarchGraphs/'
g = Graph.from_csv(
    directed=False,
    #node_path= nodesFolder + 'monarch-kg_nodes_nameChange.tsv',
    node_path= 'monarch-kg_nodes.tsv',
    edge_path= edgeFolder + 'resEdges.tsv',
    node_list_separator='\t',
    verbose=True,
    nodes_column='id',
    node_list_node_types_column='category',
    default_node_type='biolink:NamedThing',
    sources_column='subject',
    destinations_column='object',
    edge_list_edge_types_column='predicate',
    name='Monarch KG'
)
