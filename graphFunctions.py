import grape


def removeTrueSingletonNodes(allSingletons, removedEdgesFile):
    with open(removedEdgesFile, 'r', encoding='utf8') as rEF:
       removedEdgeNodes = []
       lines = rEF.readlines()
       for line in lines:
           removedEdgeNodes.append(line[18])
           removedEdgeNodes.append(line[19])

    for singleNodes in allSingletons:
        trueSingle = []
        if singleNodes not in removedEdgeNodes:
            trueSingle.append(singleNodes)
            # TODO: Remove single node
    return
