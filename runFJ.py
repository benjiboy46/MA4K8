from parameters import Parameters
from graphFJ import model

#Call this function to run the Adapted DeGroot Model

def run_model(dummy): 
    
    iterations = model.iteration_bunch(Parameters().num_iterations)
    print('Iteration is done')

    # Simulation execution
    return iterations

