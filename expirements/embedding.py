import pandas as pd
import csv
import grape
import numpy as np
from embiggen.embedders.ensmallen_embedders import TransEEnsmallen, LaplacianEigenmapsEnsmallen, ScoreSPINE, Node2VecCBOWEnsmallen
from scipy.spatial.distance import cosine
from ensmallen import Graph
from embiggen.embedders.ensmallen_embedders import FirstOrderLINEEnsmallen
import matplotlib.pyplot as plt
from grape import GraphVisualizer
from embiggen.embedders.ensmallen_embedders import DeepWalkGloVeEnsmallen, DeepWalkSkipGramEnsmallen

def cosineSimGenes(graph, all_human_genes, disease_curie):
    # ehlers danlos
    eds_curie = "MONDO:0020066"
    # ehlers danlos hypermobility type
    eds4_curie = "MONDO:0007523"
    hVW_curie = 'MONDO:0019565'
    fa_curie = 'MONDO:0019391'
    nf_cure = 'MONDO:0021061'
    cosine_sims_eds_vs_genes = {}
    c=0
    for this_gene_curie in all_human_genes:
        try:
            cosine_sims_eds_vs_genes[this_gene_curie] = cosine(graph.loc[disease_curie], graph.loc[this_gene_curie])
        except:
            c+=1

    print(c)
    return cosine_sims_eds_vs_genes


def graphEmbedding(g):
    embedding = DeepWalkSkipGramEnsmallen().fit_transform(g)
    visualizer = GraphVisualizer(g)
    visualizer.fit_nodes(embedding)
    visualizer.plot_node_types()
    plt.show()
    GraphVisualizer(g).fit_and_plot_all(embedding)
    humanGenes = g.get_node_names_from_node_curie_prefixes(['HGNC'])
    embeddingDF = embedding.get_all_node_embedding()[0]
    embeddingOutFile = 'embeddingDeepWalkSkipGramEnsmallenMonarch20230503_nosingle.csv'
    embeddingDF.to_csv(embeddingOutFile)
    print(embeddingDF)

    simGenes = cosineSimGenes(embeddingDF, humanGenes)
    simRange = list(map(abs,simGenes.values()))
    plt.hist(simRange)
    plt.show()
    rankedGenes = sorted(simGenes.items(), key=lambda item: item[1], reverse=False)
    for gene in rankedGenes[:100]:
        if 'HGNC' in gene[0]:
            print(gene[0])

    return embeddingDF, rankedGenes


def predictions():
    humanGenes = g.get_node_names_from_node_curie_prefixes(['HGNC'])
    pathwayNodes = g.get_node_names_from_node_curie_prefixes(['REACT'])
    embeddingFile = 'expirements\embeddingDeepWalkSkipGramEnsmallenMonarch20230503_nosingle.csv'
    embeddingFile = 'embeddingDeepWalkSkipGramEnsmallenMonarch20230503_nosingle.csv'
    #embeddingFile = 'embeddingDeepWalkSkipGramEnsmallenMonarch20230503_nosingleDEEpWak.csv'
    #embeddingFile = 'embeddingDeepWalkSkipGramEnsmallenMonarch20230503_nosingleTransE.csv'
    embeddingDF = pd.read_csv(embeddingFile, index_col=0)
    print(embeddingDF)

    eds4_curie = "MONDO:0007523"
    hVW_curie = 'MONDO:0019565'
    hemoA_curie = 'MONDO:0010602'
    vw1_curie = 'MONDO:0008668'
    vw2_curie = 'MONDO:0013304'
    vw3_curie = 'MONDO:0010191'
    fa_curie = 'MONDO:0019391'
    diabetes_curie = 'MONDO:0005015'


    simGenes_EDS = cosineSimGenes(embeddingDF, pathwayNodes, fa_curie)
    rankedGenes = sorted(simGenes_EDS.items(), key=lambda item: item[1], reverse=False)
    edsGenes = []
    for gene in rankedGenes[:100]:
        if 'REACT' in gene[0]:
            edsGenes.append(gene[0])
            print(gene)


    simGenes_EDS = cosineSimGenes(embeddingDF, pathwayNodes, diabetes_curie)
    rankedGenes = sorted(simGenes_EDS.items(), key=lambda item: item[1], reverse=False)
    hvwGenes = []
    for gene in rankedGenes[:100]:
        if 'REACT' in gene[0]:
            hvwGenes.append(gene[0])
    intersectionGenes = list(set(edsGenes) & set(hvwGenes))
    for gene in intersectionGenes:
        print(gene)

def pickEmbedding(g):
    embedding = DeepWalkSkipGramEnsmallen().fit_transform(g)
    embeddingDF = embedding.get_all_node_embedding()[0]
    embeddingOutFile = 'embeddingDeepWalkSkipGramEnsmallenMonarch20230503_nosingleDEEpWak.csv'
    embeddingDF.to_csv(embeddingOutFile)
    visualizer = GraphVisualizer(g)
    GraphVisualizer(g).fit_and_plot_all(embedding)
    plt.show()
    visualizer.fit_nodes(embedding)
    visualizer.plot_node_types()
    plt.show()
    # has a wider variety of cosine distance
    embedding = TransEEnsmallen().fit_transform(g)
    embeddingDF = embedding.get_all_node_embedding()[0]
    embeddingOutFile = 'embeddingDeepWalkSkipGramEnsmallenMonarch20230503_nosingleTransE.csv'
    embeddingDF.to_csv(embeddingOutFile)
    visualizer = GraphVisualizer(g)
    GraphVisualizer(g).fit_and_plot_all(embedding)
    plt.show()
    visualizer.fit_nodes(embedding)
    visualizer.plot_node_types()
    plt.show()

folder = 'expirements/monarch20231028/'
g = Graph.from_csv(
    directed=False,
    node_path=folder+'monarch-kg_nodes.tsv',
    edge_path=folder+'monarch-kg_edges.tsv',
    node_list_separator='\t',
    edge_list_separator='\t',
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
print(g)
#df, cosSims = graphEmbedding(g)
#pickEmbedding(g)

#predictions()
