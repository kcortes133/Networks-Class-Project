import grape, re
import silence_tensorflow.auto
import pandas as pd
import matplotlib.pyplot as plt
from ensmallen.datasets.kgobo import MONDO
from ensmallen.datasets.monarchinitiative import Monarch
from ensmallen.datasets import get_kgobo_okapi_tfidf_weighted_textual_embedding
from ensmallen.datasets import get_okapi_tfidf_weighted_textual_embedding
from grape.embedders import DeepWalkSkipGramEnsmallen
import embiggen.edge_prediction
from grape.edge_prediction import KipfGCNEdgePrediction


def multiMondalEdgePred(g):

    graph_main_component = g.remove_components(top_k_components=1)
    graph_main_component.enable()

    biolink_specter = pd.read_csv(
        "https://github.com/LucaCappelletti94/biolink_embedding/blob/main/biolink_3.1.1_allenai_specter.csv.gz?raw=true",
        compression='gzip',
        index_col=[0]
    )

    node_type_features = pd.DataFrame(
        biolink_specter.loc[[
            re.sub(r"(\w)([A-Z])", r"\1 \2", node_type_name.split(":")[1]).lower()
            for node_type_name in graph_main_component.get_unique_node_type_names()
        ]].values,
        index=graph_main_component.get_unique_node_type_names()
    )
    path = 'monarch-kg_nodes_nameChange_withHGNC.tsv'
    print(len(g.get_node_names()))
    node_descriptions_embedding = pd.DataFrame(
        get_okapi_tfidf_weighted_textual_embedding(
            path,
            separator=',',
            header=True,
            #  k1 and b are BM25 params
            # may be tuned used hyper-parameter optimization techniques
            k1=1.5,
            b=0.75,
            columns=["id", "category", "name", "description", "provided_by"],
            # can use any bert based model from hugging face
            pretrained_model_name_or_path="allenai/scibert_scivocab_uncased"
        ),
        index=g.get_node_names()
    ).loc[graph_main_component.get_node_names()]

    # We import the topological embedding we want to use,
    # in this case a DeepWalk embedding

    # In this example we are running a lighter parametrization,
    # but you can and should explore more complex ones.
    deepwalk_embedding = DeepWalkSkipGramEnsmallen(
        embedding_size=100,
        iterations=1,
        epochs=10
    ).fit_transform(
        graph_main_component,
    )

    deepwalk_embedding = deepwalk_embedding.get_node_embedding_from_index(0)

    model = KipfGCNEdgePrediction(
        # We run only 20 epochs in this example.
        # Likely you will want to run more!
        epochs=20,
        # For embedding the edges, we use Hadamard, i.e. element-wise products
        edge_embedding_method="Hadamard",
        # We use two GCN layers
        number_of_graph_convolution_layers=3,
        # And two dense layers on top
        number_of_ffnn_head_layers=2,
        # We allow the model to use traditional edge metrics
        # such as Adamic-Adar and Jaccard
        use_edge_metrics=True,
        # We make also a node embedding layer, so the GCN
        # can learn its own node embedding.
        use_node_embedding=True,
        # We make also a node type embedding layer, so the GCN
        # can learn its own node type embedding.
        use_node_type_embedding=True,
        # We provide the name of the node features for visualization
        # purposes.
        node_feature_names=["Node descriptions Specter", "DeepWalk"],
        # We provide the name of the node-type features for visualization
        # purposes.
        node_type_feature_names=["Biolink Specter"],
        # We show the loading bars while training
        verbose=True
    )

    # And we train the model!
    model.fit(
        graph=graph_main_component,
        node_features=[node_descriptions_embedding, deepwalk_embedding],
        node_type_features=node_type_features
    )

    model.plot()
    plt.show()


