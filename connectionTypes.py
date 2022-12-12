import matplotlib.pyplot as plt

def edgeTypes(g, nodeTypes):
    edgeTypesINNodeTypes = {i: {} for i in nodeTypes}
    srcDesNodeTypes = {i: {} for i in nodeTypes}
    edgeIDS = g.get_edge_node_ids(directed=False)
    edgeTypeNames = g.get_edge_type_names()
    for e in range(len(edgeIDS)):
        edge = edgeIDS[e]
        srcNode = edge[0]
        desNode = edge[1]
        edgeType = edgeTypeNames[e]
        # get src and des node types
        srcType = g.get_node_type_names_from_node_id(srcNode)[0]
        desType = g.get_node_type_names_from_node_id(desNode)[0]
        if desType in srcDesNodeTypes[srcType]:
            srcDesNodeTypes[srcType][desType] +=1
        else:
            srcDesNodeTypes[srcType][desType] = 1

        if srcType in srcDesNodeTypes[desType]:
            srcDesNodeTypes[srcType][desType] +=1
        else:
            srcDesNodeTypes[srcType][desType] = 1

        # add edge type count to node type
        if edgeType in edgeTypesINNodeTypes[srcType]:
            edgeTypesINNodeTypes[srcType][edgeType] +=1
        else:
            edgeTypesINNodeTypes[srcType][edgeType] = 1

        # add edge type count to node type
        if edgeType in edgeTypesINNodeTypes[desType]:
            edgeTypesINNodeTypes[desType][edgeType] +=1
        else:
            edgeTypesINNodeTypes[desType][edgeType] = 1

    for nodeType in edgeTypesINNodeTypes:
        labels = edgeTypesINNodeTypes[nodeType].keys()
        labels = [l.split(':')[1] for l in labels]
        plt.bar(labels, edgeTypesINNodeTypes[nodeType].values())
        plt.xticks(rotation=15)
        plt.xlabel('Edge Types')
        plt.title(nodeType.split(':')[-1] + ' Edge Types')
        plt.show()

    for nodeType in srcDesNodeTypes:
        labels = srcDesNodeTypes[nodeType].keys()
        labels = [l.split(':')[-1] for l in labels]
        plt.bar(labels, srcDesNodeTypes[nodeType].values())
        plt.xticks(rotation=15)
        plt.xlabel('Node Types Connected')
        plt.title(nodeType.split(":")[-1] +' Connected to Node Types')
        plt.show()
