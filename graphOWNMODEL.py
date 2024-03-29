import networkx as nx
import importlib
import ndlib.models.ModelConfig as mc
import numpy as np
import random
import OwnModel
importlib.reload(OwnModel)

from OwnModel import SocialMediaModel
from parameters import Parameters
my_instance = Parameters()

# Network topology
N = my_instance.N
m = my_instance.m
num_paidposts = my_instance.num_influencers
num_antiinfluencers = my_instance.num_antiinfluencers

#create graph
list_of_new_edges = []
g1= nx.barabasi_albert_graph(N,3) #nx.connected_watts_strogatz_graph(N, m, 0.1, tries=100)
g2=nx.to_directed(g1)
g = nx.DiGraph(g2)

original_edges = list(g.edges)

#add vertices that will be set to media/antimedia
for i in range(0,num_paidposts):
    g.add_node(N+i)
    for b in range(N):
        if random.uniform(0,1)<Parameters.media_node_degree_pc:
            g.add_edge(N+i,b)
            list_of_new_edges.append((N+i,b))

for i in range(0,num_antiinfluencers):
    g.add_node(N+num_paidposts+i)
    for b in range(N):
        if random.uniform(0,1)<Parameters.media_node_degree_pc:
            g.add_edge(N+num_paidposts+i,b)
            list_of_new_edges.append((N+num_paidposts+i,b))

# Model selection
model3 = SocialMediaModel(g)

# Model Configuration
config = mc.Configuration()

#assign media/antimedia
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

#set weights
for e in edges:    
    if e in original_edges:
        config.add_edge_configuration("weight", e, random.uniform(0,1))
    elif e in list_of_new_edges:
        config.add_edge_configuration("weight", e, Parameters.weight_of_influence)

#set media to stubborn    
for n in nodes:
    if n >N:
        config.add_node_configuration("stubborn",n,1)
    else:
        config.add_node_configuration("stubborn",n,0)

model3.set_initial_status(config)
print('graphOWNMODEL is done')
