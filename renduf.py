#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:37:35 2020

@author: yazaeld
"""
import queue
import inspect


def solver(arcs,domaines,contraintes,file):
    sol = AC3(arcs,domaines,contraintes,file)

    res = []

    for k in sol:
        if k == None:
            return k  # k= None alors inconstistance trouvée
        else:
            res = k

    return res[1]  # le domaine final est renvoyé

#fonction permettant de retourner un générateur (avec yield) à chaque étape de l'algorithme jusqu'au résultat final
def AC3(arcs,domaines,contraintes,file):

    #correspond à initQueue
    [file.put(arc) for arc in arcs]

    while not file.empty():
        (xi, xj) = file.get()

        if revise(xi, xj,contraintes):
            if len(domaines[xi]) == 0:
                # le domaine de xi est vide donc il y a une inconstistance (CSP non arc-cohérent)
                print('Le domaine de' , xi , 'est vide.')
                yield None
                break

            #on récupère les voisins de xj afin de les ajouter notre file (les voisins sont les les arcs ayant pour xi la valeur xj testée précédemment)
            #En effet on veut regarder si les valeurs de xj ont un suppoort
            voisins = [i for i in arcs if i[0] == xj]
            [file.put(voisin) for voisin in voisins]

            yield ((xi, xj), domaines, voisins)
        else:
            yield ((xi, xj), domaines, None)

    #yield final, qui nous renvoit les domaines réduits
    yield (None, domaines, None)

def revise(xi, xj,contraintes):
    change = False
    xi_domaine = D[xi]
    xj_domaine = D[xj]

    #on récupère dans une liste les contraintes où le tuple (xi,xj) est concerné
    cons = [contrainte for contrainte in contraintes if contrainte[0] == xi and contrainte[1] == xj]
    for x in xi_domaine[:]:
        con_bool = False  # Boolééen qui vérifie si il y a une valeur dans le domaine de xj qui satisfait la contrainte entre xi et xj

        for y in xj_domaine:
            for contrainte in cons:
                #permet de tester pour chaque contrainte si une valeur est présente
                #on teste alors x et y pour chaque contrainte
                test = contraintes[contrainte]
                if test(x, y):
                    con_bool = True

        if not con_bool:
            #affichage des explications et retrait d'une valeur dans le domaine de xi

            print('\n--------------------------- Retrait d\'une valeur ----------------------------------\n')
            print('Contrainte testée :' , inspect.getsource(contraintes[(xi,xj)]) )
            print('Valeur testée :' , x , 'appartenant au domaine de', xi)
            print('Domaine de la valeur testée : D(' + xi + ') :' , xi_domaine , '\nDomaine de' , xj , ': \t\t      D(' + xj + ') :' , xj_domaine, '\n')
            print('Si' , xi , '=' , x , ', aucune valeur du domaine de' , xj , 'ne peut satisfaire la contrainte.')
            print('Autrement dit, il faut enlever' , x , 'dans le domaine de' , xi ,
                  "car il n'a pas de support dans le domaine de", xj + '.')
            xi_domaine.remove(x)
            change = True
            print('\nNouveau domaine de' , xi , ': D(' + xi + ') :' , xi_domaine)

    return change

#Affichage du résultat final en fonction de sol (sol est soit un domaine valide ou None)
def affichage(sol):
            if sol == None:
                print('\nIl n\'y a donc pas de solution à ce CSP car il est impossible de rendre ce CSP arc-cohérent.')
            else:
                print('\n\n\n\t\t\t Le CSP est désormais arc-cohérent.')


if __name__=='__main__':
    #arcs = [('a', 'b'), ('b', 'a'),('b', 'c'), ('c', 'b'), ('c', 'a'), ('a', 'c')]
#
#    #déclaration des domaines
#    domaines = {
#        'x': [0,1],
#        'y': [1,2]
#    }
#
#    #déclaration des contraintes
#    contraintes = {
#        ('x', 'y'): lambda x, y: x > y,
#        ('y', 'x'): lambda y, x: y < x,
#    }

#    arcs = [('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'b'), ('c', 'a'), ('a', 'c')]


    D = {
        'a': [0,1],
        'b': [1,2]
        
    }


#     constraints:
#     b = 2*a
#     a = c
#     b >= c - 2
#     b <= c + 2
    C = {
        ('a', 'b'): lambda a, b: a>b,
        ('b', 'a'): lambda b, a: b<a
        
    }
    #déclaration des arcs qui constitue le CSP
    A=[i for i in C]

    #initialisation d'une file vide
    file=queue.Queue()

    #sol permettra de savoir si le CSP est arc-cohérent ou non
    sol = solver(A,D,C,file)
        
    #affiche si le CSP est arc-cohérent ou non (sol est-il égal à None ou non)
    affichage(sol)
