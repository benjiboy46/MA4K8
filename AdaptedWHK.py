from ndlib.models.DiffusionModel import DiffusionModel
import future.utils
import numpy as np
import random
from sklearn.metrics import jaccard_score
from parameters import Parameters

__author__ = 'Cecilia Toccaceli' #original author - I have edited this code to add/consider media nodes - other models are based off this one but are my own.
__license__ = "BSD-2-Clause"


class WHKModel2(DiffusionModel):
    """
    Model Parameters to be specified via ModelConfig
    :param epsilon: bounded confidence threshold from the HK model (float in [0,1])
    :param weight: the weight of edges (float in [0,1])
    :param stubborn: The agent is stubborn or not ( in {0,1}, default 0)
 
    """

    def __init__(self, graph):
        """
        Model Constructor
        :param graph: A networkx graph object
        """
        super(self.__class__, self).__init__(graph)
        self.discrete_state = False

        self.available_statuses = {
            "Infected": 0,
            "Media":1,
            "AntiMedia":-1
        }

        self.parameters = {
            "model": {
                "epsilon": {
                    "descr": "Bounded confidence threshold",
                    "range": [0, 1],
                    "optional": False,
                },
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
        self.name = "Weight HK"

    def set_initial_status(self, configuration=None):
        """
        Override behaviour of methods in class DiffusionModel.
        Overwrites initial status using random real values.
        """
        super(WHKModel2, self).set_initial_status(configuration)

        # set node status
        
        for node in self.status:
            if node < Parameters.N:
                self.status[node] = random.uniform(-1, 1)
        self.initial_status = self.status.copy()

    '''
    For each node n, check the status s
  
    '''

    def clean_initial_status(self, valid_status=None):
        for n, s in future.utils.iteritems(self.status):
            if s > 1:
                self.status[n] = 1.0
            if s <-1:
                self.status[n] = -1.0
  

    def iteration(self, node_status=True):

        '''
        Execute a single model iteration

        :return: Iteration_id, Incremental node status (dictionary code -> status)
        '''
        # An iteration changes the opinion of the selected agent 'i' using the following procedure:
        # if i is stubborn then its status doesn't change, else
        # - select all its neighbors
        # - if between each pair of agents, there is a smaller distance than epsilon, then
        # the state of the agent change, becoming the sum between its initial opinion and
        # the average of weighted opinions of its neighbors
        # multiplied by a different factor based on the sign of the agent's (i) opinion.

        self.clean_initial_status(None)
        actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}
        '''
        - select a random agent n1
        - if it is stubborn:
            its status doesn't change 
        - else:
            - select all its neighbors
            - for each neighbor, diff_opinion is compute
            - if diff_opinion < epsilon then:
                sum the weighted opinion of the neighbor to the sum_op
            - compute new_op (updated opinion of n1)
        '''
        
        for i in range(0, self.graph.number_of_nodes()):
            # select a random node
            n1 = list(self.graph.nodes)[np.random.randint(0, self.graph.number_of_nodes())]
            
            # if n1 isn't stubborn
            if self.params['nodes']['stubborn'][n1] == 0:
                # select neighbors of n1
                neighbours = list(self.graph.predecessors(n1)) 
                media_neighbours = list(self.graph.predecessors(n1))
                media_neighbours = [x for x in media_neighbours if x >= Parameters.N and x<Parameters.N+Parameters.num_influencers]
                nonmedia_neighbours = [x for x in neighbours if x < Parameters.N]
                antimedia_neighbours = [x for x in neighbours if x >= (Parameters.N+Parameters.num_influencers)]
                sum_op = 0
                count_in_eps = 0
              
                if len(neighbours) == 0:
                    continue

                for neigh in media_neighbours or antimedia_neighbours:
                    key = (neigh, n1)
                    weight = (self.params['edges']['weight'][key])
                    sum_op += (actual_status[neigh] * weight)
                    # count_in_eps is the number of neighbors in epsilon and media
                    count_in_eps += 1

                for neigh in nonmedia_neighbours:
                    key = (neigh, n1)

                    # compute the difference between opinions
                    diff_opinion = np.abs((actual_status[n1]) - (actual_status[neigh]))
                    if diff_opinion < self.params['model']['epsilon']:
            
                        weight = (self.params['edges']['weight'][key])
                        sum_op += (actual_status[neigh] * weight)
                        # count_in_eps is the number of neighbors in epsilon
                        count_in_eps += 1

                if (count_in_eps > 0):
                    if actual_status[n1] > 0:
                        new_op = actual_status[n1] + ((sum_op / count_in_eps)* (1 - actual_status[n1]))
                    elif actual_status[n1] <= 0:
                        new_op = actual_status[n1] + ((sum_op / count_in_eps)* (1 + actual_status[n1]))

                else:
                    # if there aren't neighbors in epsilon, the status of n1 doesn't change
                    new_op = actual_status[n1]
            # if n1 is stubborn
            else:
                # opinion doesn't change
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


