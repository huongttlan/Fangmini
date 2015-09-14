import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import time as tm
import re
from itertools import combinations
import matplotlib.pyplot as plt
import networkx as nx

##################### make a graph, find the degree of nodes ##########
G=nx.Graph()
caption2 = pd.read_pickle('caption2').reset_index('drop=Ture')
name_list = [item for sublist in caption2.names.tolist() for item in sublist]
name_list = set(name_list)
G.add_nodes_from(name_list)
for names in caption2.names:
    G.add_edges_from(combinations(names, 2))

print len(G.nodes())
print len(G.edges())

degree = G.degree(G.nodes())
dgree_df = pd.DataFrame(degree.items(), columns = ['name', 'degree'])
top100 = dgree_df.sort('degree', ascending = 0).reset_index().ix[0:99]
print top100.degree.mean()
print top100.degree.std()
print top100.degree.min()
print top100.degree.max()
print top100.degree.quantile(.25)
print top100.degree.quantile(.5)
print top100.degree.quantile(.75)
subset = top100[['name', 'degree']]
tuples = [tuple(x) for x in subset.values]


########### find the pagerank of top 100 person ##########
pr = nx.pagerank(G, alpha=0.85)
dgree_df = pd.DataFrame(pr.items(), columns = ['name', 'pg'])
top100 = dgree_df.sort('pg', ascending = 0).reset_index().ix[0:99]
print top100.pg.mean()
print top100.pg.std()
print top100.pg.min()
print top100.pg.max()
print top100.pg.quantile(.25)
print top100.pg.quantile(.5)
print top100.pg.quantile(.75)
subset = top100[['name', 'pg']]
tuples = [tuple(x) for x in subset.values]
tuples

##################### make a multigraph, find the best friends ##########
G=nx.MultiGraph()
caption2 = pd.read_pickle('caption2').reset_index('drop=Ture')
name_list = [item for sublist in caption2.names.tolist() for item in sublist]
name_list = set(name_list)
G.add_nodes_from(name_list)
G.number_of_nodes()
for names in caption2.names:
    G.add_edges_from(combinations(names, 2))

degree = G.degree(G.nodes())
question3 = pd.Series(G.edges()).value_counts().head(100)
dgree_df = pd.DataFrame(question3.to_dict().items(), columns = ['name', 'edge'])
top100 = dgree_df.sort('edge', ascending = 0).reset_index().ix[0:99]
print top100.edge.mean()
print top100.edge.std()
print top100.edge.min()
print top100.edge.max()
print top100.edge.quantile(.25)
print top100.edge.quantile(.5)
print top100.edge.quantile(.75)
subset = top100[['name', 'edge']]
tuples = [tuple(x) for x in subset.values]
tuples





