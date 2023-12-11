import itertools

import neo4j, json
from neo4j import GraphDatabase

class MonarchConnection:

    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        self.driver.close()

    def query(self, query, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

conn = MonarchConnection("bolt://localhost:7687", "neo4j", "monarch133")
hEDSID = 'MONDO:0019391'
hVW = 'MONDO:0019565'

def getNodes3Hops(mondoID):
    query_string_1hop = '''
    MATCH (n:`biolink:Disease` {id:"''' + mondoID +'''"})-[p]-(o) 
    RETURN o.id
    '''
    query_string_2hop = '''
    MATCH (n:`biolink:Disease` {id:"''' + mondoID +'''"})-[*1..2]-(o) 
    RETURN o.id
    '''
    query_string_3hop = '''
    MATCH (n:`biolink:Disease` {id:"''' + mondoID +'''"})-[*1..3]-(o) 
    RETURN o.id
    '''
    db = 'monarch20230503'

    response = conn.query(query_string_1hop, db=db)
    nodes1 = [item for sublist in json.loads(json.dumps(response)) for item in sublist]

    response = conn.query(query_string_2hop, db=db)
    nodes2 = [item for sublist in json.loads(json.dumps(response)) for item in sublist]

    response = conn.query(query_string_3hop, db=db)
    nodes3 = [item for sublist in json.loads(json.dumps(response)) for item in sublist]

    allNodes = set(nodes1 + nodes2 + nodes3)
    return allNodes

edsNodes = getNodes3Hops(hEDSID)
vwNodes = getNodes3Hops(hVW)
nodeIntersection = list(edsNodes & vwNodes)
nodesTotal = edsNodes.union(vwNodes)
print(len(nodeIntersection))

with open('expirements\eds_vw_3hop_intersection.csv', 'w') as of:
    for node in nodeIntersection:
        of.write(node + ',')

with open('expirements\eds_vw_3hop_allNodes.csv', 'w') as of:
    for node in nodesTotal:
        of.write(node + ',')



#print(len(allNodes))

with open('expirements\VW_3hop_nodes.csv', 'w') as f:
    for node in vwNodes:
        f.write(node + ',')

# clique / weakly connected component
# CALL gds.wcc.stream(
#   graphName: String,
#   configuration: Map
# )



# get list of nodesIDs from subgraph
# calculate WCC return nodeIDs and component ID