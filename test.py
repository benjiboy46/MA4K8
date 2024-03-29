import importlib
from multiprocessing import Pool
import runWHK
import runOWN
import runFJ
import parameters
from customcolour import OpinionEvolution
import customcolour
importlib.reload(customcolour)
import pandas as pd
from parameters import Parameters

NumTask = 50 #number of realisations
NumPro = 4 #number of processors used

def testAdaptedFJ():

    if __name__ == "__main__":
        num_processes = NumPro
        num_tasks = NumTask

        with Pool(num_processes) as p:
            results = p.map(runFJ.run_model, [None] * num_tasks)
            
  

    finalresults = [0]*NumTask
    
    for i in range(NumTask):
        finalresults[i]= results[i][-1]['status'].values()
        
    happy_array =[]
    for i in range(NumTask):
        counter = 0
        for happynodes in finalresults[i]:
            if happynodes >0:
                counter +=1
        
        happy_array.append(counter-Parameters.num_influencers)
    viz = OpinionEvolution(runFJ.model, results[0])
    if Parameters.num_influencers == 2:
        viz.plot('FJ_num2BA.pdf')
    elif Parameters.num_influencers == 4:
        viz.plot('FJ_num4BA.pdf')
    elif Parameters.num_influencers == 6:
        viz.plot('FJ_num6BA.pdf')
    elif Parameters.num_influencers == 8:
        viz.plot('FJ_num8BA.pdf')
    elif Parameters.num_influencers == 10:
        viz.plot('FJ_num10BA.pdf')
    elif Parameters.num_influencers == 12:
        viz.plot('FJ_num12BA.pdf')
    elif Parameters.num_influencers == 14:
        viz.plot('FJ_num14BA.pdf')
    elif Parameters.num_influencers == 16:
        viz.plot('FJ_num16BA.pdf')
    elif Parameters.num_influencers == 18:
        viz.plot('FJ_num18BA.pdf')
    elif Parameters.num_influencers == 20:
        viz.plot('FJ_num20BA.pdf')
    elif Parameters.num_influencers == 0:
        viz.plot('FJ_testtestnosus.pdf')
    return(happy_array)

def testAdaptedWHK():

    if __name__ == "__main__":
        num_processes = NumPro
        num_tasks = NumTask

        with Pool(num_processes) as p:
            results = p.map(runWHK.run_model2, [None] * num_tasks)
            
  
    happy_array = []
    finalresults = [0]*NumTask
  
    for i in range(NumTask):
        finalresults[i]= results[i][-1]['status'].values()
       

    for i in range(0,NumTask):
        counter = 0
        for happynodes in finalresults[i]:
            if happynodes >0:
                counter +=1
        
        happy_array.append(counter-Parameters.num_influencers)
    viz = OpinionEvolution(runWHK.model1, results[0])
    if Parameters.num_influencers == 2:
        viz.plot('WHK_num2BA.pdf')
    elif Parameters.num_influencers == 4:
        viz.plot('WHK_num4BA.pdf')
    elif Parameters.num_influencers == 6:
        viz.plot('WHK_num6BA.pdf')
    elif Parameters.num_influencers == 8:
        viz.plot('WHK_num8BA.pdf')
    elif Parameters.num_influencers == 10:
        viz.plot('WHK_num10BA.pdf')
    elif Parameters.num_influencers == 12:
        viz.plot('WHK_num12BA.pdf')
    elif Parameters.num_influencers == 14:
        viz.plot('WHK_num14BA.pdf')
    elif Parameters.num_influencers == 16:
        viz.plot('WHK_num16BA.pdf')
    elif Parameters.num_influencers == 18:
        viz.plot('WHK_num18BA.pdf')
    elif Parameters.num_influencers == 20:
        viz.plot('WHK_num20BA.pdf')
    return(happy_array)

def testOwnModel():
    if __name__ == "__main__":
        num_processes = NumPro
        num_tasks = NumTask

        with Pool(num_processes) as p:
            results = p.map(runOWN.run_model3, [None] * num_tasks)
            
  

    finalresults = [0]*NumTask
 
    for i in range(NumTask):
        finalresults[i]= results[i][-1]['status'].values()
       
    happy_array=[]
    for i in range(NumTask):
        counter = 0
        for happynodes in finalresults[i]:
            if happynodes >0:
                counter +=1
        #print('Test3: Number of positive opinions', counter-num_paidposts, 'from a total number of', Parameters().N, 'people')
        happy_array.append(counter-Parameters.num_influencers)
    viz = OpinionEvolution(runOWN.model3, results[0])
    if Parameters.num_influencers == 2:
        viz.plot('OWNM_num2BA.pdf')
    elif Parameters.num_influencers == 4:
        viz.plot('OWNM_num4BA.pdf')
    elif Parameters.num_influencers == 6:
        viz.plot('OWNM_num6BA.pdf')
    elif Parameters.num_influencers == 8:
        viz.plot('OWNM_num8BA.pdf')
    elif Parameters.num_influencers == 10:
        viz.plot('OWNM_num10BA.pdf')
    elif Parameters.num_influencers == 12:
        viz.plot('OWNM_num12BA.pdf')
    elif Parameters.num_influencers == 14:
        viz.plot('OWNM_num14BA.pdf')
    elif Parameters.num_influencers == 16:
        viz.plot('OWNM_num16BA.pdf')
    elif Parameters.num_influencers == 18:
        viz.plot('OWNM_num18BA.pdf')
    elif Parameters.num_influencers == 20:
        viz.plot('OWNM_num20BA.pdf')
    elif Parameters.num_influencers == 0:
        viz.plot('OWNM_completegraph.pdf')
    return(happy_array)

#initalise arrays for results 
array_of_results_FJ = []
array_of_results_WHK = []
array_of_results_OWN = []

importlib.reload(runFJ)
importlib.reload(parameters)
from parameters import Parameters #refresh parameters

#get number of positive opinions for each run and number of influencers for FJ
happy_FJ = testAdaptedFJ()
average_happy_FJ = sum(happy_FJ)/ len(happy_FJ)
print(happy_FJ)
#add to array for each parameter num_influencers

array_of_results_FJ.append([Parameters.num_influencers, average_happy_FJ])
print(array_of_results_FJ)
df = pd.DataFrame(array_of_results_FJ)
df.to_csv('array_of_results_FJBA.csv', index=False, header=False)

importlib.reload(runWHK)
importlib.reload(parameters)
from parameters import Parameters #refresh parameters

#get number of positive opinions for each run and number of influencers for WHK
happy_WHK = testAdaptedWHK()
average_happy_WHK = sum(happy_WHK)/ len(happy_WHK)
print(happy_WHK)
#add to array for each parameter num_influencers

array_of_results_WHK.append([Parameters.num_influencers, average_happy_WHK])
print(array_of_results_WHK)
df1 = pd.DataFrame(array_of_results_WHK)
df1.to_csv('array_of_results_WHKBA.csv', index=False, header=False) 

importlib.reload(runOWN)
importlib.reload(parameters)
from parameters import Parameters #refresh parameters

#get number of positive opinions for each run and number of influencers for OWN
happy_OWN = testOwnModel()
average_happy_OWN = sum(happy_OWN)/len(happy_OWN)
print(happy_OWN)
#add to array for each parameter num_influencers

array_of_results_OWN.append([Parameters.num_influencers, average_happy_OWN])
print(array_of_results_OWN)
df2 = pd.DataFrame(array_of_results_OWN)
df2.to_csv('array_of_results_OWNBA.csv', index=False, header=False)
