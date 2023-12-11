import matplotlib.pyplot as plt

def harmonicCentralityPlot(graph, modelOrgs):
    nodeNames = graph.get_node_names()
    degreeCent = graph.get_harmonic_centrality()
    # go through node names and corresponding
    centDict = {i: [] for i in modelOrgs}
    for node in range(len(nodeNames)):
        orgType = nodeNames[node].split(':')[0]
        if orgType in modelOrgs:
            centDict[orgType].append(degreeCent[node])


    for org in centDict:
        print(org, len(centDict[org]))
        plt.hist(centDict[org])
        plt.xlabel('Degree Centrality Score')
        plt.ylabel('Number of Nodes')
        plt.yscale('log')
        plt.ylim([0,1000000])
        #plt.xlim([0,65000])
        plt.title('Harmonic Centrality Node Distribution for ' + org)
        plt.show()
    return


def centralityPlot(graph, modelOrgs):
    nodeNames = graph.get_node_names()
    degreeCent = graph.get_degree_centrality()
    # go through node names and corresponding
    centDict = {i: [] for i in modelOrgs}
    for node in range(len(nodeNames)):
        orgType = nodeNames[node].split(':')[0]
        if orgType in modelOrgs:
            centDict[orgType].append(degreeCent[node])

    for org in centDict:
        print(org, len(centDict[org]))
        plt.hist(centDict[org])
        plt.xlabel('Degree Centrality Score')
        plt.ylabel('Number of Nodes')
        plt.yscale('log')
        plt.ylim([0,1000000])
        #plt.xlim([0,0.1])
        plt.title('Degree Centrality Node Distribution for ' + org)
        plt.show()
    return


def closenessCentralityPlot(graph, modelOrgs):
    nodeNames = graph.get_node_names()
    degreeCent = graph.get_closeness_centrality()
    # go through node names and corresponding
    centDict = {i: [] for i in modelOrgs}
    for node in range(len(nodeNames)):
        orgType = nodeNames[node].split(':')[0]
        if orgType in modelOrgs:
            centDict[orgType].append(degreeCent[node])

    for org in centDict:
        print(org, len(centDict[org]))
        plt.hist(centDict[org])
        plt.xlabel('Degree Centrality Score')
        plt.ylabel('Number of Nodes')
        plt.yscale('log')
        plt.title('Closeness Centrality Node Distribution for ' + org)
        plt.show()
    return


def betweenessCentralityPlot(graph, modelOrgs):
    nodeNames = graph.get_node_names()
    degreeCent = graph.get_betweenness_centrality()
    # go through node names and corresponding
    centDict = {i: [] for i in modelOrgs}
    for node in range(len(nodeNames)):
        orgType = nodeNames[node].split(':')[0]
        if orgType in modelOrgs:
            centDict[orgType].append(degreeCent[node])

    for org in centDict:
        print(org, len(centDict[org]))
        plt.hist(centDict[org])
        plt.xlabel('Degree Centrality Score')
        plt.ylabel('Number of Nodes')
        plt.yscale('log')
        plt.ylim([0, 150000000])
        #plt.xlim([0, 1e7])
        plt.title('Betweeness Centrality Node Distribution for ' + org)
        plt.show()
    return

