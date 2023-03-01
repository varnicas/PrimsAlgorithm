# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:25:44 2022

@author: varni
"""


def main():
    
    vertices,arcs,edges = readFromFile()
    graph = createDict(vertices,arcs,edges)
    print(f"Graph: {graph}")
    print("--------------------------------------------")
    print(f"All nodes that are in tree {primsAlgorithm(graph)}")


def readFromFile():
    f = open("airports-split.net","r")
    row = []
    lista = []
    for line in f:
        row = []
        row = line.split()
        row = [i for i in row]
        lista.append(row)
    
    arcs_index = 0
    edges_index = 0
        
    for i in range(0,len(lista)):
        if lista[i][0].lower() == "*arcs":
            arcs_index = i
        if lista[i][0].lower() == "*edges":
            edges_index = i
   
    vertices = lista[1:arcs_index]
    
    if arcs_index != 0:
        if edges_index != 0:
            arcs = lista[arcs_index+1:edges_index]
        else:
            arcs = lista[arcs_index+1:]
    else:
        arcs = []
    if edges_index != 0:
        edges = lista[edges_index+1:]
    else:
        edges = []
    
    
    return vertices,arcs,edges
            

def createDict(vertices,arcs,edges):

    flights = {}
    if len(arcs) != 0:
        if len(arcs[0]) != 2:
            for i in arcs:
                if int(i[0]) in flights:
                    tup = int(i[1]),int(i[2])
                    flights[int(i[0])].append(tup)
                else:
                    tup = int(i[1]),int(i[2])
                    flights[int(i[0])]=[tup]
        else:
            for i in arcs:
                if int(i[0]) in flights:
                    tup = int(i[1]),1
                    flights[int(i[0])].append(tup)
                else:
                    tup = int(i[1]),1
                    flights[int(i[0])]=[tup]
    else:
        if len(edges[0]) == 3:
            for i in edges:
                if int(i[0]) in flights:
                    tup = int(i[1]),int(i[2])
                    flights[int(i[0])].append(tup)
                else:
                    tup = int(i[1]),int(i[2])
                    flights[int(i[0])] = [tup]
            for i in edges:
                if int(i[1]) in flights:
                    tup = int(i[0]),int(i[2])
                    flights[int(i[1])].append(tup)
                else:
                    tup = int(i[0]),int(i[2])
                    flights[int(i[1])] = [tup]
        else:
            for i in edges:
                if int(i[0]) in flights:
                    tup = int(i[1]),1
                    flights[int(i[0])].append(tup)
                else:
                    tup = int(i[1]),1
                    flights[int(i[0])] = [tup]
            for i in edges:
                if int(i[1]) in flights:
                    tup = int(i[0]),1
                    flights[int(i[1])].append(tup)
                else:
                    tup = int(i[0]),1
                    flights[int(i[1])] = [tup]
    return flights


def primsAlgorithm(graph):
    
    print("Connected nodes and distance between them")
    tree = [list(graph.keys())[0]]
    bridovi = []
    #adding edges of first node
    for keys,values in graph.items():
        if keys == tree[0]:
            for i in values:
                bridovi.append(i[1])
    while len(tree) != len(graph):
        tree,bridovi = findNext(tree,graph,bridovi)
        
        for keys,values in graph.items():
            #adding edges from last node in tree
            if tree[-1] == keys:
                for i in values:
                    #if node is already in tree dont add his edges again
                    if i[0] in tree:
                        continue
                    else:
                        #if edge is already in list of edges
                        if i[1] in bridovi:
                            continue
                        else:
                            bridovi.append(i[1])
    print("--------------------------------------------")
    return tree
    
def findNext(tree,graph,bridovi):
    #check if edge connects two nodes who are already in tree
    bridovi = checkIfNodesInTree(bridovi,tree,graph)
    mini1 = min(bridovi)
   
    tree1 = tree
    for i in tree:
        for keys,values in graph.items():
            if i == keys:
                for j in values:
                    if j[1] == mini1:
                        if j[0] in tree:
                            continue
                        else:
                            print(f"{i} - {j[0]}, ({mini1})")
                            tree1.append(j[0])
                            index1 = bridovi.index(mini1)
                            bridovi.pop(index1)
                            break
                        
            
    return tree1,bridovi

def checkIfNodesInTree(bridovi,tree,graph):
    mini1 = min(bridovi)
    for keys,values in graph.items():
            for k in values:
                if mini1 == k[1]:
                    #if min edge connects two nodes that are already in tree, delete edge from list of edges
                    if keys in tree and k[0] in tree:
                        index1 = bridovi.index(mini1)
                        bridovi.pop(index1)
                        return bridovi
                    else:
                        return bridovi




if __name__ == "__main__":
    main()