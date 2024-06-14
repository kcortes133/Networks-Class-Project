import pandas as pd
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
from embiggen.embedders.ensmallen_embedders import DeepWalkSkipGramEnsmallen
from embiggen.embedders.ensmallen_embedders import TransEEnsmallen, ScoreSPINE, Node2VecCBOWEnsmallen

def getGeneMappings():
    mappingsF = 'http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/quarterly/tsv/hgnc_complete_set_2022-04-01.txt'
    mappingDB = pd.read_csv(mappingsF, sep='\t')
    return mappingDB[['hgnc_id', 'symbol']]

def graphEmbedding(g):
    #embedding = get_graph_okapi_tfidf_weighted_textual_embedding(name='Monarch',
    #                                                             repository='monarchinitiative',
    #                                                             pretrained_model_name_or_path='allenai/scibert_scivocab_uncased')
    #embedding = ScoreSPINE().fit_transform(g)
    #embedding = TransEEnsmallen().fit_transform(g)
    embedding = DeepWalkSkipGramEnsmallen().fit_transform(g)
    #embedding = FirstOrderLINEEnsmallen().fit_transform(g)
    visualizer = GraphVisualizer(g)
    visualizer.fit_nodes(embedding)
    visualizer.plot_node_types()
    plt.show()
    GraphVisualizer(g).fit_and_plot_all(embedding)
    humanGenes = g.get_node_names_from_node_curie_prefixes(['HGNC'])
    embeddingDF = embedding.get_all_node_embedding()[0]
    print(embeddingDF)
    simGenes = cosineSimGenes(embeddingDF, humanGenes)
    simRange = list(simGenes.values())
    plt.hist(simRange)
    plt.show()
    rankedGenes = sorted(simGenes.items(), key=lambda item: item[1], reverse=False)
    for gene in rankedGenes[:100]:
        if 'HGNC' in gene[0]:
            print(gene[0])

    et = EdgeTransformer(method='CosineSimilarity', aligned_mapping=True)
    et.fit(embeddingDF)
    #print(embeddingDF)
    #print(et)
    cosSims = et.transform(sources=embeddingDF.iloc[:,0].to_numpy(), destinations=embeddingDF.iloc[:,0].to_numpy())
    plt.hist(cosSims)
    plt.show()
    return embeddingDF, cosSims

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
    embedding = FirstOrderLINEEnsmallen().fit_transform(g)
    #embedding = DeepWalkSkipGramEnsmallen().fit_transform(g)
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


def getGeneMappings():
    mappingsF = 'http://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/quarterly/tsv/hgnc_complete_set_2022-04-01.txt'
    mappingDB = pd.read_csv(mappingsF, sep='\t')
    return mappingDB[['hgnc_id', 'symbol']]


def cosineSimGenes(graph, all_human_genes):
    # ehlers danlos
    eds_curie = "MONDO:0020066"
    # ehlers danlos hypermobility type
    eds4_curie = "MONDO:0007523"
    fa_curie = 'MONDO:0019391'
    cosine_sims_eds_vs_genes = {}
    for this_gene_curie in all_human_genes:
        cosine_sims_eds_vs_genes[this_gene_curie] = cosine(graph.loc[eds4_curie], graph.loc[this_gene_curie])
    return cosine_sims_eds_vs_genes


# get_unchecked_edge_prediction_metrics

def getTopGenes(embeddingDF, g):
    humanGenes = g.get_node_names_from_node_curie_prefixes(['HGNC'])
    simGenes = cosineSimGenes(embeddingDF, humanGenes)
    simRange = list(simGenes.values())
    plt.hist(simRange)
    plt.show()
    rankedGenes = sorted(simGenes.items(), key=lambda item: item[1], reverse=False)
    for gene in rankedGenes[:100]:
        if 'HGNC' in gene[0]:
            print(gene[0])
