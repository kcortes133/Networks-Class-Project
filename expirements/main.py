from ensmallen import Graph
import connectionTypes, edgePrediction, graphStats, centralityMeasures, embedding
import argparse



parser = argparse.ArgumentParser(description='')

def main():

    edgeFolder = 'expirements/monarch20231028/'
    nodesFolder = 'expirements/monarch20231028/'
    g = Graph.from_csv(
        directed=False,
        node_path= nodesFolder + 'monarch-kg_nodes_nameChange_ALL_xenbase.tsv',
        edge_path = edgeFolder + 'monarch-kg_edges_all_edited_withO_xenbase.tsv',
        #edge_path= edgeFolder + 'resEdges.tsv',
        node_list_separator=',',
        verbose=True,
        nodes_column='id',
        node_list_node_types_column='category',
        default_node_type='biolink:NamedThing',
        sources_column='subject',
        destinations_column='object',
        edge_list_edge_types_column='predicate',
        name='Monarch KG'
    )

    # remove true singleton nodes
    # get singleton node names
    # check if not in the removed edges file
    # remove if not in removed edges file
    #g = g.remove_singleton_nodes()
    #singletonNodes = g.get_singleton_node_ids()
    #graphFunctions.removeTrueSingletonNodes(singletonNodes)

    edgeTypes = g.get_unique_edge_type_names()
    nodeTypes = g.get_unique_node_type_names()
    allNodeIDs = g.get_node_ids()
    allNodeNames = g.get_node_names()

    nodeTypeIDsDict = {i: [] for i in nodeTypes}
    for node in allNodeIDs:
        nodeType = g.get_node_type_names_from_node_id(node)[0]
        nodeTypeIDsDict[nodeType].append(node)



    print(nodeTypes)
    print(edgeTypes)

    topNodes = g.get_top_k_central_node_names(10)
    print(topNodes)

    print(g.report())

    # return new graph with defined attributes
    # filter_from_names

    nodeDegrees = g.get_node_degrees

    # Could edit edges and nodes to get rid of non phenotype, non model organism, non disease nodes, and all connecting edges

    #modelOrgsNodeNames = ['biolink:Gene:ZFIN', 'biolink:Gene:Xenbase', 'biolink:Gene:WB', 'biolink:Gene:SGD', 'biolink:Gene:RGD', 'biolink:Gene:MGI', 'biolink:Gene:FB',
    #                      'biolink:Gene:PomBase', 'biolink:Gene:dictyBase']
    # removed : 'biolink:Gene:ZFIN','biolink:Gene:SGD',
    #modelOrgsNodeNames = ['biolink:Gene:ZFIN', 'biolink:Gene:Xenbase', 'biolink:Gene:WB', 'biolink:Gene:RGD', 'biolink:Gene:MGI', 'biolink:Gene:FB',
    #                      'biolink:Gene:dictyBase', 'biolink:Gene:PomBase','biolink:Gene:SGD', 'biolink:Gene:HGNC', 'biolink:Gene:NCBIGene']
    modelOrgsNodeNames = ['biolink:Gene:ZFIN', 'biolink:Gene:WB', 'biolink:Gene:RGD', 'biolink:Gene:MGI', 'biolink:Gene:FB',
                          'biolink:Gene:dictyBase', 'biolink:Gene:PomBase','biolink:Gene:SGD', 'biolink:Gene:HGNC', 'biolink:Gene:NCBIGene']
    #modelOrgs = ['Xenbase', 'WB', 'ZFIN', 'RGD', 'MGI', 'FB', 'PomBase', 'dictyBase', 'SGD', 'HGNC', 'NCBIGene']
    modelOrgs = [ 'WB', 'ZFIN', 'RGD', 'MGI', 'FB', 'PomBase', 'dictyBase', 'SGD', 'HGNC', 'NCBIGene']

    # compute eccentricity for each node
    # count how many times a node shows up in the paths
    # count how many times a node type shows up
    # compare with what should be the average to see how over/underrepresented the node/type is

    graphStats.eccentricityPlot(g)
    graphStats.plotNodetypeNum(g, modelOrgsNodeNames)
    graphStats.getComponentsInfo(g)

    centralityMeasures.centralityPlot(g, modelOrgs)
    centralityMeasures.harmonicCentralityPlot(g, modelOrgs)
    centralityMeasures.betweenessCentralityPlot(g, modelOrgs)

    # could make predictions for diseases of interest
    # remove random set of edges (from one type of node) see how predictions change
    # how much new information is a model organism providing to the graph

    # oblation/removal test
    # remove one model organism nodes/edges and see how summary statistics change

    # get information about edges per node type
    connectionTypes.edgeTypes(g, nodeTypes)

    # get nodes for each gene type
    # get edge types for nodes of each type

    edgePrediction.pickEmbedding(g)

    embeddingOutFile = 'embeddingFOLE1028_wO_xenbase.csv'
    df, cosSims = embedding.graphEmbedding(g, embeddingOutFile)

    g.get_edge_prediction_metrics()

    #multimodalGCN.multiMondalEdgePred(g)
    #embeddingFile = 'embeddingDeepWalkSkipGramEnsmallen.csv'
    #embeddingDF = embedding.loadEmbedding(embeddingFile)
    #topGenes = embedding.getTopGenes(embeddingDF, g)
    #edgeFile = 'editedMonarchGraphs/graphsEdgesRemoved/SGD_withOC/removedEdges.tsv'
    #graph = 'embeddingDeepWalkSkipGramEnsmallenMonarch_edited_WO_SGD.csv'
    #graph = 'embeddingDeepWalkSkipGramEnsmallenMonarch_edited_WO_ZFINedges.csv'

    #embedding.evaluateEmbeddings(graph, edgeFile)

main()
