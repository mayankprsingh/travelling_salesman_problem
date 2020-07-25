import itertools
import math
import sqlite3 as lite
from tkinter import Tk, Label, Button, Radiobutton, IntVar, messagebox
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt


city = ['Ludhiana','Jalandhar','Amritsar','Chandigarh','Patiala']
lud_distance = ['0','61','140','106','93']
jal_distance=['61','0','80','149','154']
amr_distance=['140','80','0','229','235']
chan_distance=['106','149','229','0','75']
pat_distance=['93','154','235','75','0']
distance=['61','140','106','93','80','149','154','229','235','75']
co_or=[]
n=5
distance_matrix = {}
b = {}
dist=[]
l=0

f1 = open("city.txt", "w")
f1.write(str(city))
f1.close()


def value():
    global l
    dis = distance[l]
    while(l<10):
        l=l+1
        break
    return dis


def shortest_path():
    for z in range(n):
        distance_matrix[z, z] = 0
        for j in range(z + 1,n):
            distance_matrix[z, j] = int(value())
            distance_matrix[j, z] = distance_matrix[z, j]

    city_list = [x for x in range(n)]

    city_list[city.index(start_city)]=0
    city_list[0] = city.index(start_city)
    
    b = list(itertools.permutations(city_list))

    p = math.factorial(n - 1)

    b = b[:p]

    lst = n - 1

    for i in range(p):
        add = 0
        j = 0
        while (j < lst):
            temp = b[i][j]
            u = j+1
            temp1 = b[i][u]
            add = add + distance_matrix[temp, temp1]
            if(j==0):
                temp = b[i][lst]
                temp1 = b[i][0]
                add = add + distance_matrix[temp, temp1]
            j = j + 1
        dist.append(add)

    small = min(dist)
    ref = []
    count = 0
    for k in range(1,p):
        if dist[k] == small:
            ref.append(k)
            count = count + 1

    print ('\nAvailable Shortest Paths')
    for i in range(count):
        path=[]
        for j in b[ref[i]]:
            path.append(city[j])
        print('\n')
        print(path)

    print ('\nShortest Distance = ' + str(small))


con = lite.connect('TSP.db')
c=con.cursor()

def table_city():
    c.execute('CREATE TABLE City(City TEXT,Ludhiana TEXT,Jalandhar TEXT,Amritsar TEXT,Chandigarh TEXT,Patiala TEXT)')
    for i in range(len(city)):
        con.execute('INSERT INTO City(City,Ludhiana,Jalandhar,Amritsar,Chandigarh,Patiala) VALUES(?,?,?,?,?,?)',(city[i],lud_distance[i],jal_distance[i],amr_distance[i],chan_distance[i],pat_distance[i]))

table_city()


print('                 >>>>>> Travelling Salesman Problem <<<<<<')
print(' \nThese are the available cities with their respectable distances','\n')

f1 = open("city.txt", "r")
print(f1.read())


c.execute('SELECT * FROM City')
for row in c.fetchall():
    print(row)
con.commit()
con.close()
print('\n')

G = nx.DiGraph()

G.add_nodes_from([1, 2, 3, 4, 5])
H = nx.relabel_nodes(G, {1: 'Ludhiana', 2: 'Jalandhar', 3: 'Amritsar', 4: 'Chandigarh',5:'Patiala'})
nx.draw(H,with_labels=True)
plt.savefig("city.png")
#root = tk.Tk()
#image = tk.PhotoImage(file="city.png")
#label = tk.Label(image=image)
#label.pack()
#root.mainloop()
plt.show()


z=input('Do you wan to continue\n')

if(z=='Yes'):
    root=Tk()
    root.geometry('500x300')
    root.title('TSP')

    def tsp():
        message=messagebox.showinfo('TSP','Welcome to TSP module')
        root.destroy()

    def ask_starting_city(prompt, options):
        if prompt:
            Label(root, text=prompt).pack()
        v = IntVar()
        for i, option in enumerate(options):
            Radiobutton(root, text=option, variable=v, value=i).pack(anchor="w")
        Button(text="Submit", command=tsp,bg='white').pack()
        root.mainloop()
        if v.get() == 0: return 'Ludhiana'
        return options[v.get()]

    result = ask_starting_city(
        "Select the starting city",
        [
            "Ludhiana",
            "Jalandhar",
            "Amritsar",
            "Chandigarh",
            "Patiala"
        ]
    )

    if(result=='Ludhiana'):
        start_city="Ludhiana"
        shortest_path()
        L = nx.DiGraph()
        L.add_nodes_from([1, 2, 3, 4,5])
        L.add_edges_from([(1,5),(5,4),(4,2),(2,3),(3,1)])
        L1 = nx.relabel_nodes(L, {1: 'Start  Ludhiana', 2: 'Jalandhar', 3: 'Amritsar', 4: 'Chandigarh',5: 'Patiala'})
        nx.draw(L1,with_labels=True)
        plt.savefig("Ludhiana.png")
        #plt.show()
        root = tk.Tk()
        root.title('Shortest Path')
        image1 = tk.PhotoImage(file="Ludhiana.png")
        label1 = tk.Label(image=image1)
        label1.pack()
        root.mainloop()
        #plt.show()
    elif(result=='Jalandhar'):
        start_city="Jalandhar"
        shortest_path()
        L = nx.DiGraph()
        L.add_nodes_from([1, 2, 3, 4,5])
        L.add_edges_from([(2,3),(3,1),(1,5),(5,4),(4,2)])
        L1 = nx.relabel_nodes(L, {1: 'Ludhiana', 2: 'Start  Jalandhar', 3: 'Amritsar', 4: 'Chandigarh',5: 'Patiala'})
        nx.draw(L1,with_labels=True)
        plt.savefig("Jalandhar.png")
        root = tk.Tk()
        root.title('Shortest Path')
        image = tk.PhotoImage(file="Jalandhar.png")
        label = tk.Label(image=image)
        label.pack()
        root.mainloop()
        #plt.show()
    elif(result=='Amritsar'):
        start_city="Amritsar"
        shortest_path()
        L = nx.DiGraph()
        L.add_nodes_from([1, 2, 3, 4,5])
        L.add_edges_from([(3,2),(2,4),(4,5),(5,1),(1,3)])
        L1 = nx.relabel_nodes(L, {1: 'Ludhiana', 2: 'Jalandhar', 3: 'Start   Amritsar', 4: 'Chandigarh',5: 'Patiala'})
        nx.draw(L1,with_labels=True)
        plt.savefig("Amritsar.png")
        root = tk.Tk()
        root.title('Shortest Path')
        image = tk.PhotoImage(file="Amritsar.png")
        label = tk.Label(image=image)
        label.pack()
        root.mainloop()
        #plt.show()
    elif(result=='Chandigarh'):
        start_city="Chandigarh"
        shortest_path()
        L = nx.DiGraph()
        L.add_nodes_from([1, 2, 3, 4,5])
        L.add_edges_from([(4,5),(5,1),(1,3),(3,2),(2,4)])
        L1 = nx.relabel_nodes(L, {1: 'Ludhiana', 2: 'Jalandhar', 3: 'Amritsar', 4: 'Start   Chandigarh',5: 'Patiala'})
        nx.draw(L1,with_labels=True)
        plt.savefig("Chandigarh.png")
        root = tk.Tk()
        root.title('Shortest Path')
        image = tk.PhotoImage(file="Chandigarh.png")
        label = tk.Label(image=image)
        label.pack()
        root.mainloop()
        #plt.show()
    else:
        start_city="Patiala"
        shortest_path()
        L = nx.DiGraph()
        L.add_nodes_from([1, 2, 3, 4,5])
        L.add_edges_from([(5,4),(4,2),(2,3),(3,1),(1,5)])
        L1 = nx.relabel_nodes(L, {1: 'Ludhiana', 2: 'Jalandhar', 3: 'Amritsar', 4: 'Chandigarh',5: 'Start   Patiala'})
        nx.draw(L1,with_labels=True)
        plt.savefig("Patiala.png")
        root = tk.Tk()
        root.title('Shortest Path')
        image = tk.PhotoImage(file="Patiala.png")
        label = tk.Label(image=image)
        label.pack()
        root.mainloop()
        #plt.show()

else:
    exit()


f2 = open('distance_matrix.txt','w')
f2.write(str(distance_matrix))
f2.close()

#f2 = open('distance_matrix.txt','r')
#print(f2.read())
