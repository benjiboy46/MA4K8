from ndlib.models.DiffusionModel import DiffusionModel
import future.utils
import numpy as np
import random
from parameters import Parameters

class SocialMediaModel(DiffusionModel):

    def __init__(self, graph):

        super(self.__class__, self).__init__(graph)
        self.discrete_state = False

        self.available_statuses = {
            "Infected": 0,
            "Media":1,
            "AntiMedia":-1
        }

        
        self.parameters = {
            "model": {
            },
            
            "edges": {
                "weight": {
                    "descr": "Edge weight",
                    "range": [0, 1],
                    "optional": True,
                    "default": 0.1
                }
            },
            "nodes": {
                "stubborn": {
                    "descr": "The agent is stubborn or not",
                    "range": {0, 1},
                    "optional": True,
                    "default": 0
                },
            },
        }
        self.name = "Social Media "
    
    def set_initial_status(self, configuration):
        
        super(SocialMediaModel, self).set_initial_status(configuration)

        for node in self.status:
            if node < Parameters.N:
                self.status[node] = random.uniform(-1, 1)
        self.initial_status = self.status.copy()
   
    def clean_initial_status(self, valid_status=None):
        for n, s in future.utils.iteritems(self.status):
            if s > 1:
                self.status[n] = 1.0
            if s <-1:
                self.status[n] = -1.0
    
    
    def bernoulli_probability(self, node): # define bernoulli probability for function
        if node >= Parameters.N:
            if random.uniform(0,1)<Parameters.media_activity:
                return 1
            else:
                return 0
        else:
            if random.uniform(0,1) <Parameters.nonmedia_activity:
                return 1
            else:
                return 0

    def opinion_amplification(self, xop, amplificationconstant): # opinion amp constant
        if xop>0 and xop < 1-amplificationconstant:
            return amplificationconstant
        elif xop<0 and xop > -1+ amplificationconstant:
            return -amplificationconstant
        else:
            return 0
    
    def iteration(self, node_status=True):
        
        self.clean_initial_status(None)
        actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}

        if self.actual_iteration == 0:
    
            self.actual_iteration += 1
   
            if node_status:
                return {"iteration": 0, "status": self.status.copy(),
                        "node_count": len(self.status), "status_delta": self.status.copy()}
            else:
                return {"iteration": 0, "status": {},
                        "node_count": len(self.status), "status_delta": self.status.copy()}

        NumNodes = self.graph.number_of_nodes()  

        for _ in range(0,NumNodes):
           
            n1 = list(self.graph.nodes)[np.random.randint(0, self.graph.number_of_nodes())]
            
            # if n1 isn't stubborn
            if self.params['nodes']['stubborn'][n1] == 0:
                averageop = 0
                for i in range(Parameters.N):
                    averageop += actual_status[i]/(Parameters.N)

                neighbours = list(self.graph.predecessors(n1)) 
                sum_op = 0
               
                if len(neighbours) == 0:
                    continue

                counter = 0

                for neigh in neighbours:
                    key = (neigh, n1)
                    weight = (self.params['edges']['weight'][key])
                    activity = self.bernoulli_probability(neigh)
                    counter += activity
                    sum_op += weight*activity *(actual_status[neigh]+self.opinion_amplification(actual_status[neigh],Parameters.op_amp)) 
                
                if counter >0:
                    if actual_status[n1]>=0:
                        new_op = actual_status[n1] + ((sum_op/counter) *(1-actual_status[n1]))
                    else:
                        new_op = actual_status[n1] + ((sum_op/counter) *(1+actual_status[n1])) 
                else:
                    new_op = actual_status[n1]
            else:
            # opinion doesn't change if stubborn
                new_op = actual_status[n1]

            actual_status[n1] = new_op

        self.status = actual_status
        self.actual_iteration += 1
        if node_status:
            return {"iteration": self.actual_iteration - 1, "status": self.status.copy(), "node_count": len(actual_status),
                    "status_delta": self.status.copy()}
        else:
            return {"iteration": self.actual_iteration - 1, "status": {}, "node_count": len(actual_status),
                    "status_delta": self.status.copy()}