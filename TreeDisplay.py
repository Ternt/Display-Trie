import networkx as nx
import matplotlib.pyplot as plt

def readPaths():
    f = open("tree.txt", "r")
    pathList = []
    
    for i in f:
        path = ""
        x = 1
        while(i[x] != "]"):
            if(i[x]==','):
                x+=1
            path += i[x]
            x += 1
        print(path)
        pathList.append(path)
        
    return pathList

path = readPaths()
G = nx.prefix_tree(path)
G.remove_node(-1)

print(G.edges)
print(G.nodes.data('source'))

nx.draw_networkx(G, with_labels=True, node_size = 1500, arrows=False, width=3)
plt.show()
