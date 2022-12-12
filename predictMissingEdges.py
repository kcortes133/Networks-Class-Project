import copy
import time
from grape import Graph, GraphVisualizer

import matplotlib.pyplot as plt
import pandas as pd
import random, statistics
import igraph as ig


def getGraphNBD(graphURL, metadataURL):
    metadataDF = pd.read_csv(metadataURL, sep=' ', encoding='iso8859_10')
    metadata = dict(zip(metadataDF.id, metadataDF.gender))

    edgeDict = {}
    edgeList = pd.read_csv(graphURL, sep=' ', header=None)
    edgeList.astype('int')
    for index, row in edgeList.iterrows():
        if row[0] in edgeDict:
            edgeDict[int(row[0])].append(int(row[1]))
        else:
            edgeDict[int(row[0])] = [int(row[1])]

    return edgeDict, metadata


def getGraphMal(graphURL, metadataURL):
    metadataDF = pd.read_csv(metadataURL, header=None)
    metadataDF.index = metadataDF.index +1
    metadata = metadataDF.to_dict()[0]

    edgeDict = {}
    edgeList = pd.read_csv(graphURL, sep=',', header=None)
    edgeList.astype('int')
    for index, row in edgeList.iterrows():
        if row[0] in edgeDict:
            edgeDict[int(row[0])].append(int(row[1]))
        else:
            edgeDict[int(row[0])] = [int(row[1])]
        if int(row[1]) not in edgeDict:
            edgeDict[row[1]] = []

    return edgeDict, metadata




def calcSmoothingH(network, missingNLs, labels):
    correct = 0
    total = 0
    for node in network:
        # get all neighbors
        neighbors = network[node]
        observedLs = []
        actualLs = []
        for n in neighbors:
            if n not in missingNLs:
                observedLs.append(labels[n])
            else:
                actualLs.append(n)
        if len(neighbors) > 0:
            if len(observedLs) > 0:
                predicted = statistics.mode(observedLs)
            else:
                predicted = 1

        for l in actualLs:
            if labels[l] == predicted:
                correct += 1
            total +=1
    return correct/total


def calcDegreeProd(network, removedEdges, emptyEdges):
    scoreTP = []
    scoreTN = []
    for edge in emptyEdges:
        node1 = edge[0]
        node2 = edge[1]
        if edge in removedEdges:
            scoreTP.append(len(network[node1])*len(network[node2]) + random.uniform(0, 0.0000000000001))
        else:
            scoreTN.append(len(network[node1])*len(network[node2]) + random.uniform(0, 0.0000000000001))

    return scoreTP, scoreTN


def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    if union == 0:
        return 0
    return float(intersection / union)


def calcJaccard(network, removedEdges, emptyEdges):
    scoreTP = []
    scoreTN = []

    for edge in emptyEdges:
        node1 = edge[0]
        node2 = edge[1]
        if edge in removedEdges:
            scoreTP.append(jaccard(network[node1], network[node2]) + random.uniform(0, 0.0000000000001))
        else:
            scoreTN.append(jaccard(network[node1], network[node2]) + random.uniform(0, 0.0000000000001))

    return scoreTP, scoreTN


def calcShortPath(network, removedEdges, emptyEdges):
    scoreTP = []
    scoreTN = []
    graph = ig.Graph().ListDict(network)
    # for missing edge
    # get shortest path between the nodes that actually exists
    # divide 1/shortest path
    numEdges = len(emptyEdges)
    n = 0
    s = time.time()
    for edge in emptyEdges:
        node1 = edge[0]
        node2 = edge[1]
        if n%100000 ==0:
            print(n, time.time()-s)

        shortPaths = graph.get_shortest_paths(node1, to=node2)
        if len(shortPaths[0]) == 0:
            shortestPath = -1
        else:
            shortestPath = len(shortPaths[0])

        if edge in removedEdges:
            scoreTP.append(1/shortestPath + random.uniform(0, 0.0000000000001))
        else:
            scoreTN.append(1/shortestPath + random.uniform(0, 0.0000000000001))
        n+=1

    return scoreTP, scoreTN


def randomlyRemoveEdges(network, numRand):
    allPossibleEdges = []
    nodes = network.keys()
    edges = []
    newNetwork = copy.deepcopy(network)

    for node1 in nodes:
        for node2 in nodes:
            allPossibleEdges.append((node1, node2))

    for n1 in network:
        for n2 in network[n1]:
            edges.append((n1, n2))

    # randomly remove edges

    removedEdges = list(random.sample(edges, k=int((1-numRand)*len(edges))))
    for edge in removedEdges:
        newNetwork[edge[0]].remove(edge[1])

    # take all possible and subtract the ones in the graph, add back the ones we 'removed'
    emptyEdges = set(allPossibleEdges) - set(edges)
    emptyEdges.update(set(removedEdges))

    return removedEdges, list(emptyEdges), newNetwork


def randomizeEdges(network, numRand):
    edges = []
    nodes = network.keys()
    for n1 in network:
        for n2 in network[n1]:
            edges.append((n1, n2))

    # randomly remove edges
    smallerGraph = list(random.sample(edges, k=int(numRand*len(edges))))

    # randomly add edges back in
    for n in range(int((1-numRand)*len(edges))):
        newEdge = random.sample(nodes, k=2)
        smallerGraph.append((newEdge[0], newEdge[1]))
        smallerGraph.append((newEdge[1], newEdge[0]))

    newNetwork = {}
    for edge in smallerGraph:
        if edge[0] in newNetwork:
            newNetwork[edge[0]].append(edge[1])
        else:
            newNetwork[edge[0]] = [edge[1]]

        if edge[1] not in newNetwork:
            newNetwork[edge[1]] = []

    return newNetwork


def calcAUC(scoresTP, scoresTN):
    # zip scores with 1 or 0 depending on n or p and then sort all
    # iterate through until seen all true positives
    score = 0
    sTPs = list(zip(scoresTP, [1]*len(scoresTP)))
    sTNs = list(zip(scoresTN, [0]*len(scoresTN)))
    sTPs.extend(sTNs)
    orderdSTs = sorted(sTPs, key=lambda tup:tup[0], reverse=True)
    totTPs = len(scoresTP)
    totFPs = len(scoresTN)

    truePRs = []
    falsePRs = []

    numTPs = 0
    numFPs = 0
    prevFPR = 0
    tpr = 0
    fpr = 0
    auc = 0
    curr = 0
    aucFPRs = []
    aucTPRs = []
    step=0.1
    for s in orderdSTs:
        # if true positive
        if s[1] == 1:
            numTPs += 1
            tpr = (numTPs)/totTPs

        else:
            numFPs +=1
            fpr = (numFPs)/totFPs

        truePRs.append(tpr)
        falsePRs.append(fpr)
        if fpr > curr:
            aucFPRs.append(fpr)
            aucTPRs.append(tpr)

            curr+= step

        auc = auc + (tpr * (fpr-prevFPR))
        prevFPR = fpr
    print(auc)
    #plt.plot(falsePRs, truePRs)
    #plt.title('ROC Curve')
    #plt.xlabel('True Positive Rate(TPR)')
    #plt.ylabel('False Positive Rate(FPR)')
    #plt.show()


    return auc, aucFPRs, aucTPRs


def getAUCs(file):
    aucs = []
    f = []
    with open(file, 'r') as inF:
        lines = inF.readlines()
        for l in lines:
            l = l.strip().split('\t')
            f.append(float(l[0]))
            aucs.append(float(l[1]))
    return f, aucs



exp2 = False
if exp2:
    f = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
    outFile = 'Norwegian_'
    edgeDict, genderDict = getGraphNBD(norwegianBoardofDirURL, genderID)
    outFile = outFile + 'ShortestPath.txt'

    aucs = []
    for i in f:
        print('f: ', i)
        avgAuc = []
        for j in range(1):
            removedEdges, emptyEdges, newNetwork = randomlyRemoveEdges(edgeDict, i)

            #scoreTP, scoreTN = calcJaccard(newNetwork, removedEdges, emptyEdges)
            #scoreTP, scoreTN = calcDegreeProd(newNetwork, removedEdges, emptyEdges)
            scoreTP, scoreTN = calcShortPath(newNetwork, removedEdges, emptyEdges)
            # zip scores with 1 or 0 depending on n or p and then sort all
            # iterate through until seen all true positives

            auc, falsePRs, truePRs = calcAUC(scoreTP, scoreTN)
            avgAuc.append(auc)
        # plt.plot(falsePRs, truePRs)
        # plt.title('ROC Curve')
        # plt.xlabel('True Positive Rate(TPR)')
        # plt.ylabel('False Positive Rate(FPR)')
        # plt.show()
        aucs.append(statistics.mean(avgAuc))

        #plt.hist(scoreTN, weights=np.ones(len(scoreTN))/len(scoreTN))
        #plt.hist(scoreTP, weights=np.ones(len(scoreTP))/len(scoreTP))
        #plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        #plt.show()
    outputInfo = zip(f, aucs)
    with open(outFile, 'w') as of:
        for n, h in outputInfo:
            of.write(str(n) + '\t' + str(h) + '\n')

    plt.plot(f, aucs)
    plt.show()


exp2Plot = False
if exp2Plot:
    malDP = 'Malaria_DegreeProduct.txt'
    malJacc = 'Malaria_Jaccard.txt'
    malSP = 'Malaria_ShortestPath.txt'

    fMDP, aucMDP = getAUCs(malDP)
    fMJ, aucMJ = getAUCs(malJacc)
    fMSP, aucMSP = getAUCs(malSP)

    plt.plot(fMDP, aucMDP, marker='o')
    plt.plot(fMJ, aucMJ, marker='x')
    plt.plot(fMSP, aucMSP, marker='D')
    plt.ylim(0.5, 1)
    plt.xlabel('Fraction of Edges Observed (f)')
    plt.ylabel('AUC')
    plt.title('Malaria Network Edge Prediction AUC vs Edges Observed')
    plt.show()


    norDP = 'Norwegian_DegreeProduct.txt'
    norJacc = 'Norwegian_Jaccard.txt'
    norSP = 'Norwegian_ShortestPath.txt'

    fNDP, aucNDP = getAUCs(norDP)
    fNJ, aucNJ = getAUCs(norJacc)
    fNSP, aucNSP = getAUCs(norSP)

    plt.plot(fNDP, aucNDP, marker='o')
    plt.plot(fNJ, aucNJ, marker='x')
    plt.plot(fNSP, aucNSP, marker='D')
    plt.ylim(0.5, 1)
    plt.title('Norwegian Network Edge Prediction AUC vs Edges Observed')
    plt.xlabel('Fraction of Edges Observed (f)')
    plt.ylabel('AUC')
    plt.show()

extraCredit =True
if extraCredit:
    f = 0.8
    edgeDictN, genderDictN = getGraphNBD(norwegianBoardofDirURL, genderID)
    edgeDictM, genderDictM = getGraphMal(malariaURL, malariaMetadata)

    removedEdgesN, emptyEdgesN, newNetworkN = randomlyRemoveEdges(edgeDictN, f)
    removedEdgesM, emptyEdgesM, newNetworkM = randomlyRemoveEdges(edgeDictM, f)

    scoreTPJN, scoreTNJN = calcJaccard(newNetworkN, removedEdgesN, emptyEdgesN)
    scoreTPDPN, scoreTNDPN = calcDegreeProd(newNetworkN, removedEdgesN, emptyEdgesN)
    scoreTPSPN, scoreTNSPN = calcShortPath(newNetworkN, removedEdgesN, emptyEdgesN)

    scoreTPJM, scoreTNJM = calcJaccard(newNetworkM, removedEdgesM, emptyEdgesM)
    scoreTPDPM, scoreTNDPM = calcDegreeProd(newNetworkM, removedEdgesM, emptyEdgesM)
    scoreTPSPM, scoreTNSPM = calcShortPath(newNetworkM, removedEdgesM, emptyEdgesM)

    aucJN, falsePRJN, truePRJN = calcAUC(scoreTPJN, scoreTNJN)
    aucSPN, falsePRDPN, truePRDPN = calcAUC(scoreTPDPN, scoreTNDPN)
    aucSPN, falsePRSPN, truePRSPN = calcAUC(scoreTPSPN, scoreTNSPN)

    aucJM, falsePRJM, truePRJM = calcAUC(scoreTPJM, scoreTNJM)
    aucSPM, falsePRDPM, truePRDPM = calcAUC(scoreTPDPM, scoreTNDPM)
    aucSPM, falsePRSPM, truePRSPM = calcAUC(scoreTPSPM, scoreTNSPM)

    plt.plot(falsePRJN, truePRJN, color='orange', marker='x')
    plt.plot(falsePRDPN, truePRDPN, color='orange', marker='o')
    plt.plot(falsePRSPN, truePRSPN, color='orange', marker='D')

    plt.plot(falsePRJM, truePRJM, color='blue', marker='x')
    plt.plot(falsePRDPM, truePRDPM, color='blue', marker='o')
    plt.plot(falsePRSPM, truePRSPM, color='blue', marker='D')

    plt.title('ROC Curve')
    plt.ylabel('True Positive Rate(TPR)')
    plt.xlabel('False Positive Rate(FPR)')
    plt.show()
