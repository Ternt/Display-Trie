# Display-Tree
A program I did while interning at a vietnamese company called Mobile World JSC. During the internship I was tasked with visualizing data structures in a way that was easy to understand. The data structure I had to visualize was a tree, or more specifcally, a trie. 

The program takes in two lists of vertices. One that is in preorder and the other in postorder. The program then iterates through these two lists to then build the tree and finally display it. The tree is built using networkx and displayed using plotly. 

Example input:  
```
postorder3 = [10,4,11,5,1,12,6,13,7,2,14,8,15,9,3,0]
preorder3 =  [0,1,4,10,5,11,2,6,12,7,13,3,8,14,9,15]
```
Example output:
![Screenshot_3](https://github.com/Ternt/Display-Tree/assets/45267060/4893ea1f-88fa-43b2-a5b8-cd7bc9623a21)
