
# A python program for visualizing prefix trees.
# It reads paths from a text file, build the tree,
# and then display that prefix tree. The program uses
# networkx for building the prefix tree and plotly 
# for visualizing.


from collections import defaultdict
import networkx as nx
import plotly.graph_objects as go

from os import system, name
from time import sleep
    
def readPathsFromFile(filename = ""):
    """Method reads from a file the content of which is all the 
    paths of a trie. Reformats the data into a suitable format.
    Appends all those paths into a list and returns the list.
    
    Parameters
    ----------
    filename: str
        Name of the .txt file containing our trie paths.
    
    Returns
    -------
    pathList: list
        A list of all the trie paths.
    """
    f = open(textExtensionCheck(filename), "r")
    allPaths = []  
    # Iterates through every line in the file.
    for i in f:
        i = i.replace(" ", "")
        # If the line is empty, continue to next iteration.
        if(len(i.strip()) == 0):
            continue
        
        path = ""
        keys = []
        values = []
        index = 1
        
        # Given a string with the format: [0.0_0, ..., 500000.0_3]___500000.0 
        # First loop to iterate through the portion of the string that's between
        # the square brackets.
        while(index <= i.index("]")):  
            # Temporary variable to store a constructed string.
            temp = ""
            
            # Second loop to build up a string. Starts on the current index and
            # ends when the string is a ',' or ']'. The constructed string is 
            # stored in the variable temp. 
            # An example value for temp would be "0.0_0", "500000.0_3", or "350000.0_2"
            while(i[index] != ',' and i[index] != ']'):
                temp += i[index]
                index += 1
            
            # If the format is correct, then every value of temp should have an underscore,
            # separating the node key and the node value. Using this, we will split the key
            # and value into two arrays. The reason being, to make our next process easier. 
            keys.append(temp[temp.index("_")+1:])  
            values.append(temp[:temp.index("_")])
            index += 1
        # Because of how the algorithm, the algorithm that provides our program the path file, works, 
        # the data that we've been given is shifted. 
        
        '''Example:
        #      Keys   |    Values
        #   ----------------------
        #      0      |    0.0
        #      3      |    500000.0
        #      2      |    350000.0
        #
        # should be
        #      Keys   |    Values
        #   ----------------------
        #      null   |    0.0
        #      0      |    500000.0
        #      3      |    350000.0
        #      2      |    ...
        '''
        
        # This last portion of code is to 
        # 1. reshift the data so that they correspond to their correct values
        # 2. Build up each path and append them into pathList
        values.append(i[i.index("]")+4:-1])
        
        for i in range(len(keys)):              
            path += keys[i] + "_" + values[i+1] + " "
        path = path.split()
        allPaths.append(path)
    
    return allPaths


def textExtensionCheck(filename):
    """Method to make inputting the file name easier. Just in case
    I'm lazy and don't want to spend a few more milliseconds to
    type out the .txt extension.
    
    Parameters
    ----------
    filename: str
        Name of the .txt file containing our trie paths.
    
    Returns
    -------
    (string):
        The file name. Additionally concatenated with ".txt" extension if 
        the original does not have it.
    """
    if (not filename.__contains__(".txt")):
        return filename + ".txt"
    
    return filename
    
# Taken from networkx prefix_tree source code. Modified to be more specific to my program.
# source: https://networkx.org/documentation/stable/_modules/networkx/generators/trees.html#prefix_tree
def prefix_tree(trie, paths):
    """Creates a directed prefix tree from a list of paths.

    Usually the paths are described as strings or lists of integers.

    A "prefix tree" represents the prefix structure of the strings.
    Each node represents a prefix of some string. The root represents
    the empty prefix with children for the single letter prefixes which
    in turn have children for each double letter prefix starting with
    the single letter corresponding to the parent node, and so on.

    More generally the prefixes do not need to be strings. A prefix refers
    to the start of a sequence. The root has children for each one element
    prefix and they have children for each two element prefix that starts
    with the one element sequence of the parent, and so on.

    Note that this implementation uses integer nodes with an attribute.
    Each node has an attribute "source" whose value is the original element
    of the path to which this node corresponds. For example, suppose `paths`
    consists of one path: "can". Then the nodes `[1, 2, 3]` which represent
    this path have "source" values "c", "a" and "n".

    All the descendants of a node have a common prefix in the sequence/path
    associated with that node. From the returned tree, the prefix for each
    node can be constructed by traversing the tree up to the root and
    accumulating the "source" values along the way.

    The root node is always `0` and has "source" attribute `None`.
    The root is the only node with in-degree zero.
    The nil node is always `-1` and has "source" attribute `"NIL"`.
    The nil node is the only node with out-degree zero.


    Parameters
    ----------
    paths: iterable of paths
        An iterable of paths which are themselves sequences.
        Matching prefixes among these sequences are identified with
        nodes of the prefix tree. One leaf of the tree is associated
        with each path. (Identical paths are associated with the same
        leaf of the tree.)


    Returns
    -------
    tree: DiGraph
        A directed graph representing an arborescence consisting of the
        prefix tree generated by `paths`. Nodes are directed "downward",
        from parent to child. A special "synthetic" root node is added
        to be the parent of the first node in each path. A special
        "synthetic" leaf node, the "nil" node `-1`, is added to be the child
        of all nodes representing the last element in a path. (The
        addition of this nil node technically makes this not an
        arborescence but a directed acyclic graph; removing the nil node
        makes it an arborescence.)


    Notes
    -----
    The prefix tree is also known as a *trie*.


    Examples
    --------
    Create a prefix tree from a list of strings with common prefixes::

        >>> paths = ["ab", "abs", "ad"]
        >>> T = nx.prefix_tree(paths)
        >>> list(T.edges)
        [(0, 1), (1, 2), (1, 4), (2, -1), (2, 3), (3, -1), (4, -1)]

    The leaf nodes can be obtained as predecessors of the nil node::

        >>> root, NIL = 0, -1
        >>> list(T.predecessors(NIL))
        [2, 3, 4]

    To recover the original paths that generated the prefix tree,
    traverse up the tree from the node `-1` to the node `0`::

        >>> recovered = []
        >>> for v in T.predecessors(NIL):
        ...     prefix = ""
        ...     while v != root:
        ...         prefix = str(T.nodes[v]["source"]) + prefix
        ...         v = next(T.predecessors(v))  # only one predecessor
        ...     recovered.append(prefix)
        >>> sorted(recovered)
        ['ab', 'abs', 'ad']
    """
    def get_children(parent, paths):
        children = defaultdict(list)
        # Populate dictionary with key(s) as the child/children of the root and
        # value(s) as the remaining paths of the corresponding child/children
        count = 0
        while(count < len(paths)):
            path = paths[count]
            # If path is empty, we add an edge to the NIL node.
            if not path:
                trie.add_edge(parent, NIL)
                count += 1
                continue
            child = (path[0][0], path[0][path[0].index("_")+1:])
            rest = path[1:]
            # `child` may exist as the head of more than one path in `paths`.
            children[child].append(rest)
            count += 1
        return children
        
    
    # Initialize the prefix tree with a root node and a nil node.
    root = 0
    trie.add_node(root, source="Null", value='')
    NIL = -1
    trie.add_node(NIL, source="NIL")
    children = get_children(root, paths)   
    stack = [(root, iter(children.items()))]
    while stack:
        parent, remaining_children = stack[-1]
        try:
            child, remaining_paths = next(remaining_children)

        # Pop item off stack if there are no remaining children
        except StopIteration:
            stack.pop()
            continue
        # We relabel each child with an unused name.
        new_name = len(trie) - 1
        # The "source" node attribute stores the name of the parent node.
        # The "value" node attribute stores the value at that node.
        trie.add_node(new_name, source=child[0], value=child[1])
        trie.add_edge(parent, new_name)
        children = get_children(new_name, remaining_paths)
        stack.append((new_name, iter(children.items())))
             
   
# A function for calculating the layout for a tree. 
# source: https://www.cluzters.ai/forums/topic/459/can-one-get-hierarchical-graphs-from-networkx-with-python-3?c=1597
def hierarchy_pos(G, root, width = 1, vert_gap = 0.2, vert_loc = 0, xcenter = 0.5 ):
    '''If there is a cycle that is reachable from root, then result will not be a hierarchy.

    Parameters
    ----------
    G: DiGraph
        the graph
    
    root: any
        the root node of current branch
    
    width: int
        horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: int
        gap between levels of hierarchy
    
    vert_loc: int
        vertical location of root
    
    xcenter: int
        horizontal location of root
    '''
    def h_recur(G, root, width, vert_gap, vert_loc, xcenter, pos = None, parent = None, parsed = []):
        # check so that it would not infinitely recurse.      
        if(root not in parsed):
            parsed.append(root)
            if pos == None:
                pos = {root:(xcenter,vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)
            neighbors = list(G.neighbors(root))
            if len(neighbors)!=0:
                dx = width/len(list(neighbors))
                nextx = xcenter - width/2 - dx/2
                for neighbor in neighbors:
                    nextx += dx
                    pos = h_recur(G,neighbor, dx, vert_gap = vert_gap,
                                        vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos,
                                        parent = root, parsed = parsed)
        return pos
    return h_recur(G, root, width, vert_gap, vert_loc, xcenter)


def makeAnnotations(G, pos, labels=None, color='black', size=15):
    """The method labels all nodes in the trie.
    
    Parameters
    ----------
    pos: dictionary
        A dictionary containing the xy-coordinates of each Vertex in the graph.  
    
    labels: Array of strings
        An array of strings. Array length is equal to the number of 
        vertices.
    
    color: string 
    -     A hex string (e.g. '#ff0000')     
    -     An rgb/rgba string (e.g. 'rgb(255,0,0)')           
    -     An hsl/hsla string (e.g. 'hsl(0,100%,50%)')     
    -     An hsv/hsva string (e.g. 'hsv(0,100%,100%)')     
    -     A named CSS color: Defaults to 'white'
    
    size: int
        Size of font. Defaults to 15.
    
    Returns
    -------
    annotations:
        Array of string, which represents annotations.
    """
    annotations = []
    for k in G.nodes:
        annotations.append(dict(
        text=switchLabelling(G, k, labels),
        x=pos[k][0], y=pos[k][1],
        xref='x1', yref='y1',
        font=dict(color=color, size=size),
        showarrow=False
    ))
    return annotations


def switchLabelling(G, label, labelArray):
    """Helper function to handle logic for switching between different labels.
    If labelArray is None or G.nodes, then the trie will not be labelled.
    If labelArray is an array of elements, then the trie will be labelled 
    according to the array.
    
    Parameters
    ----------
    label: 
        String or integer.
    
    labelArray: array
        Array of labels.

    Returns
    -------
    Any: 
        return either an element in G.nodes or an element in the array of labels.
    """          
    if labelArray == G.nodes or labelArray == None:
        return label
    else:
        return labelArray[label]


def extractVertexData(G = nx.DiGraph()):
    """Get source and value attributes and store them in two arrays.
    These arrays are used for drawing.  

    Parameters
    ----------
    G: DiGraph 
        Defaults to nx.DiGraph().

    Returns
    -------
    (tuple): 
        returns a tuple containing two lists, source and value. 
        The lists contain the source and value attributes of a node.
    """
    sources = []
    values = []
    for i in G.nodes:
        sources.append(G.nodes[i]['source'])
        values.append(G.nodes[i]['value'])

    return sources, values


def draw(G):
    """A Method for drawing and rendering the trie. It gets data from
    the networkx tree and places them into arrays. These arrays are then
    passed into plotly, stored in dictionaries. Plotly will use this data
    to render the tree.  
    Resources: https://plotly.com/python/tree-plots/

    Parameters
    ----------
    G: DiGraph
        Tree needed for visualization.
    """
    G.remove_node(-1)
    pos = hierarchy_pos(G, 0, width=10, vert_gap=0.1)
    
    ###########################
    #--------EDGE DATA--------#
    ###########################
    
    #List of x edge positions.
    edge_x = []
    
    #List of y edge positions.
    edge_y = [] 
    
    for (n0, n1) in G.edges:
        for x in (pos[n0][0], pos[n1][0], None):
            edge_x.append(x)

    for (n0, n1) in G.edges:
        for y in (pos[n0][1], pos[n1][1], None):
            edge_y.append(y)
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='rgb(0,0,0)'),
        hoverinfo='none',
        mode='lines')

    ############################
    #--------LABEL DATA--------#
    ############################
    trieLabels = extractVertexData(G)

    ###########################
    #--------NODE DATA--------#
    ###########################
    
    #List of x node positions.
    node_x = []
    
    #List of y node positions.
    node_y = []

    for node in G.nodes():
        x,y = pos[node]

        node_x.append(x)
        node_y.append(y)
        
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',                 # Shape of a point https://plotly.com/python/marker-style/#:~:text=6-,Custom%20Marker%20Symbols,-The%20marker_symbol%20attribute
        hoverinfo='text',                
        text=trieLabels[1],
        texttemplate='%{text}',
        textposition="bottom center",
        marker=dict(color="rgba(195, 74, 54, 0.8)",
            size=25,
            line=dict(color="#4B4453", width=1)))

    #########################
    #--------DRAWING--------#
    #########################
    fig = go.Figure(
                data=[edge_trace, node_trace],
                layout=go.Layout(annotations=makeAnnotations(G, pos, trieLabels[0], 'white', 15),
                                showlegend = False,
                                xaxis=dict(showgrid=True, zeroline=True, showticklabels=False),
                                yaxis=dict(showgrid=True, zeroline=True, showticklabels=False,))
            )

    config = {'scrollZoom': True, 
                'displaylogo': False,
                'modeBarButtonsToRemove':['lasso2d']}
    
    fig.show(renderer="browser", config=config)

def buildTrie(trie, file_name):
    """Takes in a file name (string). Builds a prefix tree from that file.

    Args:
        String. The name of a file.

    Returns:
        A networkx DiGraph object.
    """
    paths = readPathsFromFile(file_name)
    trie = prefix_tree(trie, paths)

    return trie

def displayTrie(trie):
    """Takes in a tree and displays it.

    Args:
        trie: A DiGraph object from networkx.
    """
    draw(trie)

#####################################################################################################
##-------------------------------------------CLIENT CODE-------------------------------------------##
#####################################################################################################


if __name__ == '__main__':
    def clear(seconds):
        """A function to clear the terminal screen after n seconds.

        Parameters
        ----------
            seconds: how long before the terminal screen clears.
        """
        sleep(seconds)
        
        if name == 'nt':
            _ = system('cls')

        else:
            _ = system('clear')

    repeat = True
    while repeat:
        option1 = ""
        try:
            clear(0)
            file_name = input("Name of the file you want to open: ")
            
            trie = nx.DiGraph()
            buildTrie(trie, file_name)
            displayTrie(trie)
            
            option1 = input("Do you want to quit the program (Y/N)? ")
            if option1.capitalize() != "Y":
                continue
            clear(0)
            repeat = False
        except FileNotFoundError:
            print("File does not exist. Please try again.")
            clear(2)
        

