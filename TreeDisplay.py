import networkx as nx
import matplotlib.pyplot as plt #Currently unused. Another way to display the Graph
import plotly.graph_objects as go

# Class for displaying the tree as a proper hierarchical structure.
class displayTree:
    G = nx.DiGraph()
    
    def __init__(self, graph):
        self.G = graph
 
    
    def _hierarchy_pos(self, root=0, width=1, vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        """Reposition nodes from a networkx Graph object into a hierarchical structure by calculating a position map.

        Args:
            G (DiGraph): Tree
            root (any): Root node key
            width (int, optional): width between nodes. Defaults to 1..
            vert_gap (float, optional): the vertical distance between each layer. Defaults to 0.2.
            vert_loc (int, optional): _description_. Defaults to 0.
            xcenter (float, optional): horizontal center of the tree. Defaults to 0.5.
            pos (dict, optional): A dictionary which maps a vertex to its position coordinate. Defaults to None.
            parent (any, optional): value of the parent node. Defaults to None.

        Returns:
            pos: dictionary containing coordinate tuples which maps the position of the nodes into a hierarchical structure.
        """
        
        if self.G.size == 0:
            return Exception("No nodes in the graph, please build graph first.")
        
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(self.G.neighbors(root))
        if not isinstance(self.G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = self._hierarchy_pos(child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos


    def _makeAnnotations(self, pos, text=None, color='white', size=15):
        """Goes through each vertex and label them accordingly. text (array) parameter needs to be in preorder.
        
        Args:
            pos (dict): A dictionary containing the xy-coordinates of each Vertex in the graph.  
            text (list): An array of lables as strings. Array length is equal to the number of vertices. Defaults to None.
            color (string): A hex string (e.g. '#ff0000') or more...\n
            etc:\n               
                        - An rgb/rgba string (e.g. 'rgb(255,0,0)')           
                        - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')     
                        - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')     
                        - A named CSS color:
                        Defaults to 'white'.\n
            size (int): Size of font. Defaults to 15.

        Returns:
            annotations (list): Array of string, which represents annotations.
        """
        
        Length = len(pos)
        # if len(text) != Length:
        #     raise ValueError('The lists pos and text must have the same len')
        
        annotations = []
        for k in G.nodes:
            annotations.append(dict(
            text=self.switchLabels(k, text),
            x=pos[k][0], y=pos[k][1],
            xref='x1', yref='y1',
            font=dict(color=color, size=size),
            showarrow=False
        ))

            
        return annotations


    def switchLabels(self, label, labelArray):
        """Helper function to handle logic to switch between different labels.\n
        Args:
            label (any): String or integer.
            labelArray (list): Array of labels.

        Returns:
            Any: return either an element in G.nodes or an element in the array of labels.
        """
        
        if labelArray == self.G.nodes or labelArray == None:
            return label
        else:
            return labelArray[label]

    
    def display(self):    
        """A method to display trees in a proper hierarchical structure. Graphs are made using networkx and plotly is used to display.
        """
        pos = self._hierarchy_pos(0)
        nx.draw_networkx(self.G, pos, with_labels=True, node_size = 1500, arrows=False, width=3)
        config = {'scrollZoom': True, 
                  'displaylogo': False,
                  'modeBarButtonsToRemove':['lasso2d']}
        
        ##################################
        #--------EDGE INFORMATION--------#
        ##################################
        edge_x = []
        for (n0, n1) in self.G.edges:
            for x in (pos[n0][0], pos[n1][0], None):
                edge_x.append(x)

        edge_y = []
        for (n0, n1) in self.G.edges:
            for y in (pos[n0][1], pos[n1][1], None):
                edge_y.append(y)


        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='rgb(0,0,0)'),
            hoverinfo='none',
            mode='lines')

        ##################################
        #--------NODE INFORMATION--------#
        ##################################
        node_x = []
        node_y = []

        for node in self.G.nodes():
            x,y = pos[node]

            node_x.append(x)
            node_y.append(y)
            
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(color='rgb(0,0,0)',
                size=40),
                line_width=2)

        #############################
        #--------DRAW FIGURE--------#
        #############################
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(annotations=self._makeAnnotations(pos, self.G.nodes, 'white', 15),
                             showlegend = False,
                             xaxis=dict(showgrid=True, zeroline=True, showticklabels=False),
                             yaxis=dict(showgrid=True, zeroline=True, showticklabels=False,))
        )
        
        fig.show(config=config)


class Tree:
    G = nx.DiGraph()
    preorder = []
    postorder = []
    display = displayTree(G)

    def __init__(self, graph, preorder, postorder):
        self.G = graph
        self.preorder = preorder
        self.postorder = postorder
        self.display = displayTree(self.G).display
        
    # Check if the tree is built. Displays if it is.
    def display(self):
        self.display

    
    def buildTree(self, pIndex, start, end, dict, n):
        """_summary_

        Args:
            preorder (list): _description_
            pIndex (int): _description_
            start (int): _description_
            end (int): _description_
            d (dict): _description_
            count (int): _description_

        Returns:
            root (int): key value of current node
            pIndex (int): index of preorder list
        """
        
        # Consider the next item from the given preorder sequence.
        # This item would be the root node of the subtree formed by
        # the `postorder[start, end]` and increment `pIndex`
        root = self.preorder[pIndex]
        self.G.add_node(root)
        pIndex = pIndex + 1
        
        # return if all keys are processed
        #print(pIndex, len(preorder))
        if pIndex == len(self.preorder):
            return root, pIndex, n

        # find the next key index in the postorder sequence to determine the
        # boundary of the left and right subtree of the current root node
        index = dict.get(self.preorder[pIndex])
        #print("root", root,"| start:", start,"end:", end ,"next node:", self.preorder[pIndex],"index:", index, "n:", n)

        for i in range(n):
            n -= 1
                
            # Need this while loop to only iterate over subtrees with more than one neighbour
            if(start <= index and index <= end):
                startSubtree = start
                endSubtree = index
                
                if i > 0:
                    startSubtree = index + 1
                    endSubtree = end - 1
                
                # build the left subtree
                node, pIndex, n = self.buildTree(pIndex, startSubtree, endSubtree, dict, n)
                #print(node, pIndex, n)
                self.G.add_edge(root, node)
                
                if(start == index):
                    break
        
        #print(root, "is returned with pIndex:", pIndex, "n:", n)
        return root, pIndex, n + 1

    # Construct a full generic tree from preorder and postorder sequence
    def buildGenericTree(self):
        """_summary_

        Args:
            preorder (list): Array of elements from a tree obtained from preorder traversal.
            postorder (list): Array of elements from a tree obtains from postorder traverasl.

        Returns:
            function: a fully built tree
        """
        
        # base case
        if not self.preorder or len(self.preorder) != len(self.postorder):
            return

        # postorder array is parsed into a dictionary to efficiently find the index of 
        # any element in the given postorder sequence
        dict = {}
        for i, e in enumerate(self.postorder):
            dict[e] = i

        # `pIndex` stores the index of the next node in the preorder sequence
        pIndex = 0

        # set range [start, end] for subtree formed by postorder sequence
        start = 0
        end = len(self.preorder) - 1

        # a rigid depth calculation function. Relies on 
        # the fact that combination trees are perfect.
        n=self.calculateDepth(pIndex, start, end, dict, 0)[0]
    
        return self.buildTree(pIndex, start, end, dict, n-1)[0]
    
    # A rigid depth calculation function to initiate building of true. 
    # Relies on the fact that combination trees are perfect.
    def calculateDepth(self, pIndex, start, end, dict, n):
        pIndex = pIndex + 1
        
        if pIndex == len(self.preorder):
            return pIndex, n

        index = dict.get(self.preorder[pIndex])
        #print("start:", start,"end:", end ,"next node:", self.preorder[pIndex],"index:", index, "n:", n)
        
        if(start <= index and index <= end):                
                # build the left subtree
                pIndex, n = self.calculateDepth(pIndex, start, index, dict, n)
                
    
        return (pIndex, n+1)
        

#####################################################################################################
##-------------------------------------------CLIENT CODE-------------------------------------------##
#####################################################################################################
G = nx.DiGraph()

# 0 is our root. If we move along our preorder list, 1 is a subtree. Any number below 1 are 
# children of 1, they are [4,10,5,11]. 4 is a subtree. Any number below 4 are children of 4, 
# in this case it is only [10]. 10 is not a subtree so we pop it off the stack.
postorder0 = [0]
preorder0 =  [0]

postorder1 = [1,0]
preorder1 =  [0,1]

postorder2 = [3,1,4,2,0]
preorder2 =  [0,1,3,2,4]

postorder3 = [10,4,11,5,1,12,6,13,7,2,14,8,15,9,3,0]
preorder3 =  [0,1,4,10,5,11,2,6,12,7,13,3,8,14,9,15]

postorder4 = [41,17,42,18,5,43,19,44,20,6,45,21,46,22,7,1,
            47,23,48,24,8,49,25,50,26,9,51,27,52,28,10,2,
            53,29,54,30,11,55,31,56,32,12,57,33,58,34,13,3,
            59,35,60,36,14,61,37,62,38,15,63,39,64,40,16,4,0]
preorder4 =  [0,1,5,17,41,18,42,6,19,43,20,44,7,21,45,22,46,
            2,8,23,47,24,48,9,25,49,26,50,10,27,51,28,52,
            3,11,29,53,30,54,12,31,55,32,56,13,33,57,34,58,
            4,14,35,59,36,60,15,37,61,38,62,16,39,63,40,64]

# TODO: Make a function which extracts values from an object for use as labels.
v_labels = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

tree = Tree(G, preorder4, postorder4)
tree.buildGenericTree()
tree.display()


######################################################################################################
##-------------------------------------------CODE ARCHIVE-------------------------------------------##
######################################################################################################

"""# Tree but letters
G.add_nodes_from(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p'])
G.add_edges_from([("a","b"), ("a","c"), ("a","d"), 
                  ("b","e"), ("b","f"), 
                  ("c","g"), ("c","h"), 
                  ("d","i"), ("d","j"), 
                  ("e","k"), 
                  ("f","l"), 
                  ("g","m"), 
                  ("h","n"),
                  ("i","o"),
                  ("j","p")])
"""

"""# Since our tree represents all possible combinations of n number of Promotions,
# if we use "P1", "P2", "P3", etc. as the key then eventually our key will be repeated. 
# Instead we'll use numbers as the key and use annotations to label the nodes as P1, P2, P3.
# Currently this relies on data in a list as input.
G.add_nodes_from([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
adjacency_list = [[1,2,3], [4,5], [6,7], [8,9], [10], [11], [12], [13], [14], [15]]

def _buildTree(adj_list):
    for k in range(len(adj_list)):
        for i in adj_list[k]:
            G.add_edge(k,i)
            
_buildTree(adjacency_list)"""

"""# Tree visualization using igraph instead of networkx
import igraph as ig
from igraph import Graph, EdgeSeq

n_vertices = 10
G = Graph.Tree(n_vertices,2)
lay = G.layout('rt')

print(lay[2])

position = {k: lay[k] for k in range(n_vertices)}
Y = [lay[k][1] for k in range(n_vertices)]
M = max(Y)

es = EdgeSeq(G)
E = [e.tuple for e in G.es]

L = len(position)
Xn = [position[k][0] for k in range(L)]
Yn = [2*M-position[k][1] for k in range(L)]

Xe = []
Ye = []
for edge in E:
    Xe+=[position[edge[0]][0],position[edge[1]][0], None]
    Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

print(position)
print(Xe)

fig = go.Figure()
fig.add_trace(go.Scatter(x=Xe, 
                         y=Ye,
                         mode='lines',
                         line=dict(color='rgb(0,0,0)', width=2),
                         hoverinfo='none'))

fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  name='bla',
                  marker=dict(symbol='circle-dot',
                                size=18,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  hoverinfo='text',
                  opacity=0.8
                  ))
"""