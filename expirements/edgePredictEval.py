from grape.edge_prediction import edge_prediction_evaluation
from embiggen.edge_prediction import edge_prediction_evaluation

from grape.embedders import Node2VecCBOWEnsmallen, Node2VecGloVeEnsmallen, Node2VecSkipGramEnsmallen
from grape.embedders import DeepWalkCBOWEnsmallen, DeepWalkGloVeEnsmallen, DeepWalkSkipGramEnsmallen
from grape.embedders import FirstOrderLINETensorFlow, SecondOrderLINETensorFlow
from grape.embedders import NMFADMMKarateClub, RandNEKarateClub
from grape.embedders import WalkletsSkipGramEnsmallen
from grape.embedders import GLEEEnsmallen, HOPEEnsmallen
from grape.embedders import Role2VecKarateClub, GraRepKarateClub
from embiggen.embedders.ensmallen_embedders import TransEEnsmallen, ScoreSPINE, Node2VecCBOWEnsmallen
from embiggen.embedders.ensmallen_embedders import FirstOrderLINEEnsmallen

from grape.edge_prediction import DecisionTreeEdgePrediction, PerceptronEdgePrediction, RandomForestEdgePrediction,\
    ExtraTreesEdgePrediction, MLPEdgePrediction, GradientBoostingEdgePrediction

import pandas as pd
from tqdm.auto import tqdm, trange
from ensmallen import Graph


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

#graph.remove_disconnected_nodes()

def graph_callback(graph):
    """Returns standardized graph."""
    if graph.get_name() == "MP":
        return graph
    graph = graph.filter_from_names(min_edge_weight=700)
    graph.enable()
    return graph

results = pd.concat([
    edge_prediction_evaluation(
        holdouts_kwargs=dict(train_size=0.8),
        graphs=[g],
        #graph_callback=graph_callback,
        models=[
            #DecisionTreeEdgePrediction(edge_embedding_method="Hadamard"),
            PerceptronEdgePrediction(
                edge_features=None,
                edge_embeddings="Hadamard"
            ),
            DecisionTreeEdgePrediction(),
            RandomForestEdgePrediction(),
            ExtraTreesEdgePrediction(),
            MLPEdgePrediction(),
            GradientBoostingEdgePrediction(),
        ],
        number_of_holdouts=2,
        node_features=EmbeddingMethod(),
        # Right now we have enabled the smoke test to rapidly run and
        # test that everything works. To reproduce the results,
        # do set the smoke test flag to `False`.
        smoke_test=False,
        enable_cache=True
    )
    for EmbeddingMethod in tqdm((
        #Node2VecCBOWEnsmallen, Node2VecGloVeEnsmallen, Node2VecSkipGramEnsmallen,
        #DeepWalkCBOWEnsmallen, DeepWalkGloVeEnsmallen,
        #DeepWalkSkipGramEnsmallen,
        ScoreSPINE,
        TransEEnsmallen,
        FirstOrderLINEEnsmallen,
        #WalkletsSkipGramEnsmallen,
    ), desc="Running experiment")
])


results.to_csv('DWSG_part1_prediction_eval_results10-28-2023.csv')
