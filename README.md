# Display-Trie
A program I am working on while interning as a backend developer at a vietnamese company called Mobile World JSC. A while back I was tasked with writing a program to visualize data structures in a way that was easy to understand. Before, I was tasked with visualizing a perfect generic (k-ary) tree based on this problem[^1]. But due to the change in data structure, I am now working with tries (prefix trees). 

Originally I wanted to make a really general program that can take in any pair of preorder and postorder list and build a tree out of it, no matter the type. That proved quite challenging and I currently I can't think of a solution to this. Also due to work, I had to change the program and implement something more specific, that being **tries** or **prefix trees**. 

Now, rather than taking in two arrays, 
1. the program reads from a text file which contains a set of paths
2. converts it into a list of strings, with each character representing a node
3. builds the graph node by node, edge by edge.

input: list of paths

![image](https://github.com/Ternt/Display-Tree/assets/45267060/eaebb8a5-88b5-4a62-a860-79ad78972cf7)

output:

![Screenshot_4](https://github.com/Ternt/Display-Tree/assets/45267060/f5485b56-205f-4a09-a001-50650973aa15)

[^1]: https://medium.com/trendyol-tech/how-do-we-calculate-promotions-in-the-cart-85e7b50af2b6
