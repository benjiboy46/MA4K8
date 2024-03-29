import networkx as nx
import importlib
import ndlib.models.ModelConfig as mc
import numpy as np
import random
import AdaptedFJ
importlib.reload(AdaptedFJ)

from AdaptedFJ import AdaptedFJ
from parameters import Parameters
my_instance = Parameters()

# Network topology - initialise parameters
N = my_instance.N
m = my_instance.m
num_paidposts = my_instance.num_influencers
num_antiinfluencers = my_instance.num_antiinfluencers
weight_of_inf = my_instance.weight_of_influence

#create graph
list_of_new_edges = []
g1= nx.connected_watts_strogatz_graph(N, m, 0.1, tries=100) #nx.barabasi_albert_graph(N,3)
g2=nx.to_directed(g1)
g = nx.DiGraph(g2)

original_edges = list(g.edges) #keep track for later

#add vertices that will be assigned to media and antimedia
if num_paidposts>0:
    for i in range(0,num_paidposts):
        g.add_node(N+i)
        for b in range(N):
            if random.uniform(0,1)<Parameters.media_node_degree_pc:
                g.add_edge(N+i,b)
                list_of_new_edges.append((N+i,b))
if num_antiinfluencers >0:
    for i in range(0,num_antiinfluencers):
        g.add_node(N+num_paidposts+i)
        for b in range(N):
            if random.uniform(0,1)<Parameters.media_node_degree_pc:
                g.add_edge(N+num_paidposts+i,b)
                list_of_new_edges.append((N+num_paidposts+i,b))

# Model selection
model = AdaptedFJ(g)

config = mc.Configuration()
#initilaise model -set media and antinmedia vertices
if num_paidposts>0:
    list1 =[]
    for i in range(0, num_paidposts):
        list1.append(N+i)
    config.add_model_initial_configuration("Media", list1)
if num_antiinfluencers>0:
    antilist=[]
    for i in range(0, num_antiinfluencers):
        antilist.append(N+num_paidposts+i)
    config.add_model_initial_configuration("AntiMedia", antilist)
    

# Setting the edge parameters
if isinstance(g, nx.Graph):
    edges = g.edges
    nodes = g.nodes
else:
    nodes = [v['name'] for v in g.vs]
    edges = [(g.vs[e.tuple[0]]['name'], g.vs[e.tuple[1]]['name']) for e in g.es]

matrix = np.zeros((N+num_paidposts+num_antiinfluencers, N+num_paidposts+num_antiinfluencers))

# Assign random numbers to edges
for i in range(N):
    for j in range(N):
        matrix[i, j] = random.uniform(0,1)

    for j in range(N,N+num_antiinfluencers+num_paidposts):
        matrix[i, j] = weight_of_inf

# Normalize rows in a vectorized manner - normalising the weights
row_sums = matrix.sum(axis=1, keepdims=True)
non_zero_rows = row_sums[:, 0] > 0  # Rows with non-zero sum
matrix[non_zero_rows] /= row_sums[non_zero_rows]

for e in edges:
        (i,j)= e
        config.add_edge_configuration("weight", e, matrix[j,i])

#set media to stubborn
for n in nodes:
    if n >N:
        config.add_node_configuration("stubborn",n,1)
    else:
        config.add_node_configuration("stubborn",n,0)

model.set_initial_status(config)
print('graphFJ is done')
   