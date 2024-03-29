from parameters import Parameters
from graphWHK import model1

#Call this function to run the WHK Model

def run_model2(dummy):
    
    iterations = model1.iteration_bunch(Parameters().num_iterations)

    print('Iteration is done')

    # Simulation execution
    return iterations