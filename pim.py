#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 16:00:00 2018

@author: clementgrisi
"""

#%% PIM

from utils import *
from dumb import *

we_are_dumb = False
dist_matrix = DistMatrix('pim')
nb_distribution = nbDistribution('pim')

if (we_are_dumb):
    dumb_architecture = dumb_solution('pim')

##

#%% descente dans reseau

# old_res = []
# new_res = []
# architecture_depart = read_solution('pim')
# print('cout depart')
# print(cout_architecture(architecture_depart, dist_matrix))
#
# for i in range(nb_distribution):
#     old_res.append(architecture_depart.pop(0))
#
# new_res.append(descente_rap_reseau(old_res[0], dist_matrix, 10000))
#
# for i in range(1, nb_distribution):
#     new_res.append(descente_rap_reseau(old_res[i], dist_matrix, 10000))
#
# architecture_arrivee = [new_res[k] for k in range(len(new_res))]
# print('cout arrivee')
# print(cout_architecture(architecture_arrivee, dist_matrix))

#%% descente dans architecture

architecture_depart = read_solution('pim')
#print(architecture_depart)
print('cout depart')
print(cout_architecture(architecture_depart, dist_matrix))
architecture_arrivee = descente_rap_architecture(architecture_depart, dist_matrix, 1000)
print('cout arrivee')
print(cout_architecture(architecture_arrivee, dist_matrix))
#print(architecture_arrivee)

#%% recuit simule dans architecture

# print('début recuit simulé')
# architecture_depart = read_solution('pim')
# print('cout depart')
# print(cout_architecture(architecture_depart, dist_matrix))
# architecture_arrivee = recuit_simule_architecture(architecture_depart, dist_matrix, nb_it = 1000, k=15, Tinit=2000)
# print('cout arrivee')
# print(cout_architecture(architecture_arrivee, dist_matrix))


#write_solution(architecture_arrivee, nb_distribution, 'pim')
