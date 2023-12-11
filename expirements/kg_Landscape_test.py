import grape
import pandas as pd

def getGeneMappings():
    mappingsF = 'http://nlp.case.edu/public/data/GPKG-Predict/data/GP_KG.txt'
    mappingDB = pd.read_csv(mappingsF, sep='\t')
    return mappingDB

print(getGeneMappings())
