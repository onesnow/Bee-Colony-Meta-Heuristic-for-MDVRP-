__author__ = 'Administrator'
import scipy as sp
import prep
import numpy as np
import bee
import localsearch as ls


population=20
capacity=100
iterations=500
filename="A-n32-k5"
depot=[0]
lamada=2
nn=1
local_search="on"

'''generate demandlist,citylist,citylist_tabu'''
demandlist=sp.genfromtxt("A-n32-k5_demand",delimiter="")[:,1]
citylist=sp.linspace(0,len(demandlist)-1,len(demandlist))
citylist_tabu=list(sp.copy(citylist))

'''Generate cordinates'''
cordinate,length=prep.data_clean(filename)

#call module prep::: function: data_clean

'''Generate distance matrix'''
reverse_distance_matrix,distance_matrix=prep.Distance_Matrix(cordinate,length)
#call module prep::: function: Distance_Matrix

'''Generate initial_fitness_matrix'''
#fitness_matrix=(sp.ones((length,length),dtype=float))*reverse_distance_matrix
fitness_matrix=reverse_distance_matrix
'''Solve VRP using ABC-Meta-Heuristic'''
###################################################
##################################################
compare_result=9999999
waggle_dance=0
for iter in range(iterations):
    '''run with multi replications to determine the iteration best result'''
    result_iter,tour_set_iter=bee.iteration(compare_result,depot,length,demandlist,capacity,citylist,citylist_tabu,distance_matrix,fitness_matrix,population,nn)

    if result_iter<compare_result:
        compare_result=result_iter
        compare_set=tour_set_iter
    else:
        pass
    print("iteration %i: "%iter,compare_result)

    '''waggle_dance'''
    for i in tour_set_iter:
        for count in range(len(tour_set_iter[i])-1):
            fitness_matrix[tour_set_iter[i][count]][tour_set_iter[i][count+1]] *=lamada #updata delta_tao matrix
            #fitness_matrix[compare_set[i][count+1]][compare_set[i][count]] *=lamada
    waggle_dance+=1
    if waggle_dance>200:
        fitness_matrix=reverse_distance_matrix
        waggle_dance=0
    else:
        pass
###################################################
####################################################

'''3-opt local search improvement to the final result'''
final_set = {}
final_result = 0
if local_search=="on":
    for i in compare_set:
        compare_tour=compare_set[i]
        length=len(compare_tour)
        improve=ls.TwoOptSwap(compare_tour,i,distance_matrix)
        final_set[improve.result]=improve.tour
        final_result+=improve.result
else:
    pass

print(final_result,"\n",final_set)


'''plot'''
prep.plot(final_set,cordinate,depot, filename)