class Parameters:
    #define necessary parameters
    N = 200
    m =int(0.01*N)
    num_influencers=0
    num_antiinfluencers = int(num_influencers/2)
    num_iterations = 50
    media_activity = 0.8
    nonmedia_activity = 0.5
    op_amp = 0.15
    weight_of_influence = 0#1.8/num_influencers
    media_node_degree_pc = 0.7
    eps = 0.5