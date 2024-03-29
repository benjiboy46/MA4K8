from parameters import Parameters
from graphOWNMODEL import model3

#Call this function to run the SMA-WHK Model

def run_model3(dummy):
    
    iterations = model3.iteration_bunch(Parameters().num_iterations)

    print('Iteration is done')

    # Simulation execution
    return iterations