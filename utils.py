import numpy as np
import csv
import re
import random as rd
import copy

# fonction ecrivant automatiquement une solution dans un fichier .txt
def write_solution(architecture, nbDistribution, ville):
    file = 'solutions/' + ville + '.txt'
    solution = open(file, 'w+')
    solution.truncate(0)
    for i in range(nbDistribution):
        for j in range(len(architecture[i])):
            if (j==0):
                solution.write('b')
                for k in range(len(architecture[i][j])):
                    solution.write(' ' + '%d' %architecture[i][j][k])
                solution.write("\n")

            else:
                solution.write('c')
                for k in range(len(architecture[i][j])):
                    solution.write(' ' + '%d' %architecture[i][j][k])
                solution.write("\n")

# fonction qui lit un fichier solution pour en faire une architecture2

def read_solution(ville):
    file = 'solutions/' + ville + '.txt'
    solution = open(file, 'r')
    nbDistribution = 0

    for row in solution:
        if (row[0] == 'b'):
            nbDistribution += 1

    nb_chaines = [0]*nbDistribution
    architecture = []
    reseau = []
    boucles = [[]]*nbDistribution
    chaines = [[]]*nbDistribution

    solution = open(file, 'r')
    rows = [row.rstrip('\n') for row in solution]
    for row in rows:
        if (row[0] == 'b'):
            k = 1
            i = rows.index(row)
            while(i<len(rows)-1 and rows[i+k][0] == 'c'):
                k=k+1
                nb_chaines[i]+=1

    for i in range(nbDistribution):
        chaines[i] = [[]]*nb_chaines[i]

    solution = open(file, 'r')
    count_b = 0
    old_b = 0
    count_c = 0
    boucle = []
    temp = []

    for row in solution:
        row = row.rstrip('\n')
        for antenne in re.split(' ', row[2:]):
            if (row[0] == 'b'):
                boucle.append(int(antenne))
            elif (row[0] == 'c'):
                temp.append(int(antenne))
        boucles[count_b] = [boucle[k] for k in range(len(boucle))]
        # print('old_b')
        # print(old_b)
        # print('count_c')
        # print(count_c)
        # print(temp)
        if (count_c < len(chaines[old_b])):
            chaines[old_b][count_c] = [temp[k] for k in range(len(temp))]
        temp = []
        boucle = []
        if (row[0] == 'b'):
            old_b = count_b
            count_b += 1
            count_c = 0
        elif (row[0] == 'c'):
            count_c += 1

    #print(boucles)

    for i in range(len(boucles)):
        reseau.append(boucles[i])
        for k in range(nb_chaines[i]):
            reseau.append(chaines[i][k])
        architecture.append(reseau)
        reseau = []

    return(architecture)


# fonctions de louis

def cout_reseau(reseau, distances):
    """prend en entree un reseau de la forme : reseau = [[boucle],[chemin1],...,[cheminkR]]
    et renvoie le cout associe"""
    cout_res = 0
    boucle = reseau[0]
    for k in range(len(boucle)-1):
        cout_res = cout_res + distances[boucle[k]][boucle[k+1]]
    cout_res = cout_res + distances[boucle[-1]][boucle[0]]
    nb_chaine = len(reseau)-1
    for k in range(nb_chaine):
        chaine_k = reseau[k+1]
        for l in range(len(chaine_k)-1):
            cout_res = cout_res+distances[chaine_k[l]][chaine_k[l+1]]
    return cout_res

# OK

def cout_architecture(architecture, distances):
    cout_arch = 0
    for reseau in architecture:
        cout_arch = cout_arch + cout_reseau(reseau, distances)
    return(cout_arch)

# OK

def insert_plus_proche(antenne, reseau, distances):
    boucle = reseau[0]
    noeud_proche = boucle[0]
    d_min = distances[noeud_proche][antenne]
    num_chem = 0
    for x in boucle:
        if(distances[x][antenne]<d_min):
            noeud_proche = x
            d_min = distances[x][antenne]
    # en sortie de ce for, noeud_proche contient l'element de la boucle le plus proche de l'antenne a inserer
    for k in range(len(reseau)-1):
        chaine_k = reseau[k+1]
        if(distances[chaine_k[-1]][antenne]<d_min and len(chaine_k)<5):
            noeud_proche = chaine_k[-1]
            d_min = distances[noeud_proche][antenne]
            num_chem = k+1
    if(num_chem == 0):
        reseau.append([noeud_proche, antenne])
    else:
        reseau[num_chem].append(antenne)

# OK

# swap dans reseau : échange deux éléments d'un reseau
# soit deux éléments de la boucle
# soit un élément de la boucle avec l'élément à la fin d'une chaine

def swap_dans_reseau(reseau, distances, i, j, meilleur = True):
    ancien_cout = cout_reseau(reseau, distances)
    boucle = reseau[0]
    if(i in boucle and j in boucle):
        new_boucle = [reseau[0][k] for k in range (len(boucle))]
        index_i = new_boucle.index(i)
        index_j = new_boucle.index(j)
        new_boucle[index_i] = j
        new_boucle[index_j] = i
        new_chaines = [reseau[k] for k in range(1, len(reseau))]
        new_reseau = [new_boucle]
        new_reseau.extend(new_chaines)
        nouv_cout = cout_reseau(new_reseau, distances)
        if(nouv_cout < ancien_cout):
            return(new_reseau)
        else:
            return(reseau)
        # elif(meilleur == False):
        #     reseau = new_reseau
        #     return(nouv_cout-ancien_cout)

    elif(i in boucle):
        new_boucle = [reseau[0][k] for k in range (len(boucle))]
        index_i = new_boucle.index(i)
        new_boucle[index_i] = j
        antennes_a_attacher = [i]
        new_reseau = [new_boucle]
        for k in range(len(reseau)-1):
            chaine_k = reseau[k+1]
            antennes_a_attacher.extend(chaine_k[1:])
        antennes_a_attacher.remove(j)
        for a in antennes_a_attacher:
            insert_plus_proche(a, new_reseau, distances)
        nouv_cout = cout_reseau(new_reseau, distances)
        if(nouv_cout < ancien_cout):
            return(new_reseau)
        else:
            return(reseau)
        # elif(not meilleur):
        #     reseau = Nouv_Res
        #     return(nouv_cout-ancien_cout)



def mod_taille_boucle(reseau , antenne_dans_c, distances, meilleur = True):
    ancien_cout = cout_reseau(reseau, distances)
    new_boucle = reseau[0]
    index_ant = new_boucle.index(antenne_dans_c)
    antenne = new_boucle.pop(index_ant)
    antennes_a_attacher = [antenne]
    new_reseau = new_boucle + [reseau[k] for k in range(1, len(reseau))]
    for k in range(len(new_reseau)-1):
        chaine_k = new_reseau[k+1]
        if(chaine_k[0] == antenne):
            new_reseau[k+1].pop(0)
            antennes_fils = new_reseau.pop(k+1)
            antennes_a_attacher.extend(antennes_fils)
    for ant in antennes_a_attacher:
        insert_plus_proche(ant, new_reseau, distances)
    nouv_cout = cout_reseau(new_reseau, distances)
    if(nouv_cout < ancien_cout):
        reseau = new_reseau
        return(nouv_cout-ancien_cout)
    elif(meilleur == False):
        reseau = new_reseau
        return(nouv_cout-ancien_cout)


def descente_rap_boucle(reseau, distances, nb_swap):
    step = 0
    boucle = reseau[0]
    temp = reseau
    ancien_cout = cout_reseau(reseau, distances)
    while(step < nb_swap):
            index1 = rd.randint(1,len(boucle)-1)
            index2 = rd.randint(1,len(boucle)-1)
            while(index1 == index2):
                index2 = rd.randint(1,len(boucle)-1)
            res = swap_dans_reseau(temp, distances, boucle[index1], boucle[index2])
            nouv_cout = cout_reseau(res, distances)
            if (nouv_cout < ancien_cout):
                temp = res
                ancien_cout = nouv_cout
                step = step + 1
            else:
                step = step + 1
    return(temp)

def descente_rap_reseau(reseau, distances, nb_swap):
    step = 0
    boucle = reseau[0]
    temp = [reseau[k] for k in range(len(reseau))]
    ancien_cout = cout_reseau(reseau, distances)
    if (len(reseau) > 1):
        while(step < nb_swap):
            index1 = rd.randint(1,len(boucle)-1)
            random_chaine = reseau[rd.randint(1,len(reseau)-1)]
            num2_dans_chaine = rd.randint(0, len(random_chaine)-1)
            while (num2_dans_chaine == boucle[0]):
                num2_dans_chaine = rd.randint(0, len(random_chaine)-1)
            res = swap_dans_reseau(reseau, distances, boucle[index1], random_chaine[num2_dans_chaine])
            nouv_cout = cout_reseau(res, distances)
            if (nouv_cout < ancien_cout):
                temp = res
                ancien_cout = nouv_cout
                step = step + 1
            else:
                step = step + 1
    return(temp)


def swap_entre_deux_res(architecture, i, j, distances, meilleur = True):
    ancien_cout_arch = cout_architecture(architecture, distances)
    reseau_i = architecture[i]
    reseau_j = architecture[j]
    #temp = [architecture[k] for k in range(len(architecture))]
    temp = copy.deepcopy(architecture)
    if (len(reseau_i) > 1 ):
        # new_reseau_i = [reseau_i[k] for k in range(len(reseau_i))]
        # new_reseau_j = [reseau_j[k] for k in range(len(reseau_j))]
        new_reseau_i = copy.deepcopy(reseau_i)
        new_reseau_j = copy.deepcopy(reseau_j)
        num_chaine = rd.randint(1, len(reseau_i)-1)
        while (new_reseau_i[num_chaine] == []):
            num_chaine = rd.randint(1, len(reseau_i)-1)
        antenne_transferer = new_reseau_i[num_chaine].pop(-1)
        insert_plus_proche(antenne_transferer, new_reseau_j, distances)
        nouv_cout_arch = ancien_cout_arch - cout_reseau(reseau_i, distances) - cout_reseau(reseau_j, distances) + cout_reseau(new_reseau_i, distances) + cout_reseau(new_reseau_j, distances)
        if(nouv_cout_arch < ancien_cout_arch):
            temp[i] = new_reseau_i
            temp[j] = new_reseau_j
    return(temp2)
    # elif(meilleur == False):
    #     architecture[i] = new_reseau_i
    #     architecture[j] = new_reseau_j
    #     return(nouv_cout_arch-ancien_cout_arch)


def descente_rap_architecture(architecture, distances, nb_swap):
    step = 0
    ancien_cout = cout_architecture(architecture, distances)
    temp = architecture
    while(step < nb_swap):
        indice_reseau_1 = rd.randint(0, len(architecture)-1)
        indice_reseau_2 = rd.randint(0, len(architecture)-1)
        while (indice_reseau_1 == indice_reseau_2):
            indice_reseau_2 = rd.randint(0, len(architecture)-1)
        res = swap_entre_deux_res(temp, indice_reseau_1, indice_reseau_2, distances)
        nouv_cout = cout_architecture(res, distances)
        if (nouv_cout < ancien_cout):
            temp = res
            ancien_cout = nouv_cout
            step = step + 1
        else:
            step = step + 1
    return(temp)