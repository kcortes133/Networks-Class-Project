import time

import pandas as pd
import csv
import grape
from embiggen.embedding_transformers import EdgeTransformer
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine
from embiggen.edge_prediction import PerceptronEdgePrediction
from ensmallen.datasets import get_graph_okapi_tfidf_weighted_textual_embedding
from grape.edge_prediction import PerceptronEdgePrediction
from embiggen.embedders.ensmallen_embedders import FirstOrderLINEEnsmallen
from grape import GraphVisualizer
from embiggen.embedders.ensmallen_embedders import DeepWalkGloVeEnsmallen, DeepWalkSkipGramEnsmallen
from embiggen.embedders.ensmallen_embedders import TransEEnsmallen, LaplacianEigenmapsEnsmallen, ScoreSPINE, Node2VecCBOWEnsmallen

def getGeneMappings():
    mappingsF = 'http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/quarterly/tsv/hgnc_complete_set_2022-04-01.txt'
    mappingDB = pd.read_csv(mappingsF, sep='\t')
    return mappingDB[['hgnc_id', 'symbol']]


def graphEmbedding(g, embeddingOutFile):
    embedding = DeepWalkSkipGramEnsmallen().fit_transform(g)
    visualizer = GraphVisualizer(g)
    visualizer.fit_nodes(embedding)
    visualizer.plot_node_types()
    plt.show()
    GraphVisualizer(g).fit_and_plot_all(embedding)
    humanGenes = g.get_node_names_from_node_curie_prefixes(['HGNC'])
    embeddingDF = embedding.get_all_node_embedding()[0]
    embeddingDF.to_csv(embeddingOutFile)

    simGenes = cosineSimGenes(embeddingDF, humanGenes)
    simRange = list(simGenes.values())
    plt.hist(simRange)
    plt.show()
    rankedGenes = sorted(simGenes.items(), key=lambda item: item[1], reverse=False)
    for gene in rankedGenes[:100]:
        if 'HGNC' in gene[0]:
            print(gene[0])

    return embeddingDF, rankedGenes

def embeddingResults(df, cosSims, g):
    df['CosineSimilarity'] = cosSims
    df['DestinationNodeNames'] = [
        g.get_node_name_from_node_id(nodeID) for nodeID in df.destinations
    ]
    df.sort_values('CosineSimilarity')
    topGenes = df.sort_values('CosineSimilarity').head(20)['DestinationNodeNames'].tolist()
    geneMappings = getGeneMappings()
    geneMappingsDict = dict(zip(geneMappings['hgnc_id'], geneMappings['symbol']))
    for t in topGenes:
        print(geneMappingsDict[t])
    for gene in topGenes:
        p = g.get_shortest_path_node_names_from_node_names(
            src_node_name=gene,
            dst_node_name="MONDO:0007523",
        )
        print(p)


def pickEmbedding(g):
    #embedding = FirstOrderLINEEnsmallen().fit_transform(g)
    embedding = DeepWalkSkipGramEnsmallen().fit_transform(g)
    # has a wider variety of cosine distance
    #embedding = TransEEnsmallen().fit_transform(g)
    #embedding = ScoreSPINE().fit_transform(g)
    visualizer = GraphVisualizer(g)
    #visualizer.fit_nodes(embedding)
    #visualizer.plot_node_types()
    #plt.show()
    GraphVisualizer(g).fit_and_plot_all(embedding)
    plt.show()
    visualizer.fit_nodes(embedding)
    visualizer.plot_node_types()
    plt.show()


def cosineSimGenes(graph, all_human_genes):
    # ehlers danlos
    eds_curie = "MONDO:0020066"
    # ehlers danlos hypermobility type
    eds4_curie = "MONDO:0007523"
    fa_curie = 'MONDO:0019391'
    nf_cure = 'MONDO:0021061'
    cosine_sims_eds_vs_genes = {}
    for this_gene_curie in all_human_genes:
        cosine_sims_eds_vs_genes[this_gene_curie] = cosine(graph.loc[eds4_curie], graph.loc[this_gene_curie])
    return cosine_sims_eds_vs_genes


# get_unchecked_edge_prediction_metrics

def shortestPaths(topGenes, g, destinationNode):
    # look at what types of nodes are seen most frequelnty
    # group nodes that go through similar paths
    # see how many paths are less than length n
    # nodes with more short paths are less significant
    topGenesPathInfo = {}
    for gene in topGenes:
        topGenesPathInfo[gene] = {}
        shortestPath = g.get_shortest_path_node_names_from_node_names(
            src_node_name=gene,
            dst_node_name="MONDO:0007523")
        topGenesPathInfo[gene]['Shortest Path'] = shortestPath

        multiShortestPaths = g.get_k_shortest_path_node_names_from_node_names(
            k=10,
            src_node_name='HGNC:2201',
            dst_node_name="MONDO:0007523")
        topGenesPathInfo[gene]['Multi Shortest Paths'] = multiShortestPaths

        neighborNodes = g.get_neighbour_node_names_from_node_name(
            node_name='HGNC:9023')
        topGenesPathInfo[gene]['Neighbors'] = neighborNodes

    return topGenesPathInfo


def loadEmbedding(embeddingFile):
    embeddingDF = pd.read_csv(embeddingFile)

    return embeddingDF


def getTopGenes(embeddingDF, g):
    topGenes = {}
    humanGenes = g.get_node_names_from_node_curie_prefixes(['HGNC'])
    simGenes = cosineSimGenes(embeddingDF, humanGenes)
    simRange = list(simGenes.values())
    plt.hist(simRange)
    plt.show()
    rankedGenes = sorted(simGenes.items(), key=lambda item: item[1], reverse=False)
    for gene in rankedGenes[:100]:
        if 'HGNC' in gene[0]:
            topGenes[gene[0]] = gene[1]
    return topGenes


# go through kept edges list
# see how many of kept edges predicted these are true positives

def evaluateEmbeddings(embedding, removedEdges):
    truePos = 0
    with open(embedding, 'r') as f:
        nodes = list(csv.reader(f, delimiter=','))
        nodes.pop(0)
    nodesCoords = {}
    for node in nodes:
        nodesCoords[node[0]] = list(map(float,node[1:]))

    with open(removedEdges, 'r') as f:
        edges = list(csv.reader(f, delimiter=','))
        edges.pop(0)

    scores = []
    c = 0
    notThere = 0
    for edge in edges:
        node1 = edge[-1]
        node2 = edge[-2]
        if node1 in nodesCoords and node2 in nodesCoords:
            simScore = cosine(nodesCoords[node1], nodesCoords[node2])
            scores.append(simScore)
            if simScore < 0.5: c+=1
        else: notThere +=1

    # calculate cosine Sim between ALL nodes
    # get edges predicted to be there
    # calculate how many removed edges are predicted vs not
    #
    print(notThere)

    print(c)
    print(len(scores))
    plt.hist(scores)
    plt.show()
    return truePos


edgeFile = 'editedMonarchGraphs/graphsEdgesRemoved/MGI_withOC/removedEdges.tsv'
graph = 'embeddingDeepWalkSkipGramEnsmallenMonarch_edited_WO_SGD.csv'
graph = 'embeddingDeepWalkSkipGramEnsmallenMonarch_edited_WO_SGDedges.csv'
graph = 'embeddingDeepWalkSkipGramEnsmallenMonarchWOMGI_edges.csv'

evaluateEmbeddings(graph, edgeFile)
