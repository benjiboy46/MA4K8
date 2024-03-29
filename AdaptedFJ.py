from ndlib.models.DiffusionModel import DiffusionModel
import future.utils
import numpy as np
import random
from parameters import Parameters

class AdaptedFJ(DiffusionModel):

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
        self.name = "Adapted FJ"
    
    def set_initial_status(self, configuration):
        
        super(AdaptedFJ, self).set_initial_status(configuration)

        for node in self.status:
            if node < Parameters().N:
                self.status[node] = random.uniform(-1, 1)
        self.initial_status = self.status.copy()
   
    def clean_initial_status(self, valid_status=None):
        for n, s in future.utils.iteritems(self.status):
            if s > 1:
                self.status[n] = 1.0
            if s <-1:
                self.status[n] = -1.0
    
    def susceptibility_function(self, x): #define suscepibility function
        return (-x*x)+1 
    
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
        for i in range(0,NumNodes):
            n1 = list(self.graph.nodes)[np.random.randint(0, self.graph.number_of_nodes())]
            
            # if n1 isn't stubborn
            if self.params['nodes']['stubborn'][n1] == 0:
                neighbours = list(self.graph.predecessors(n1)) 
                sum_op = 0
               
                if len(neighbours) == 0:
                    continue

                for neigh in neighbours:
                    key = (neigh, n1)
                    weight = (self.params['edges']['weight'][key])
                    sum_op += weight*(actual_status[neigh]-actual_status[n1])

                new_op = actual_status[n1]+(self.susceptibility_function(actual_status[n1])*sum_op) #new opinion
                
            else:
            # opinion doesn't change if stubborn
                new_op = actual_status[n1]

            actual_status[n1] = new_op #update opinion
            
        self.status = actual_status
        self.actual_iteration += 1
        if node_status:
            return {"iteration": self.actual_iteration - 1, "status": self.status.copy(), "node_count": len(actual_status),
                    "status_delta": self.status.copy()}
        else:
            return {"iteration": self.actual_iteration - 1, "status": {}, "node_count": len(actual_status),
                    "status_delta": self.status.copy()}
