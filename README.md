# Display-Trie
A program I am working on while interning as a backend developer at a vietnamese company called Mobile World JSC. A while back I was tasked with writing a program to visualize data structures in a way that was easy to understand. Before, I was tasked with visualizing a perfect generic (k-ary) tree based on this problem[^1]. But due to the change in data structure, I am now working with tries (prefix trees). 

Originally I wanted to make a really general program that can take in any pair of preorder and postorder list and build a tree out of it, no matter the type. That proved quite challenging and I currently can't think of a solution to this. Also due to work, I had to change the program and implement something more specific, that being **tries** or **prefix trees**. 

Now, rather than taking in two arrays, 
1. the program reads from a text file which contains a set of paths
2. converts it into a list of strings, with each character representing a node
3. builds the graph node by node, edge by edge.

input: list of paths
```
[0.0_0, 150000.0_1, 350000.0_2, 500000.0_3]___500000.0
[0.0_0, 150000.0_1, 350000.0_3]___470000.0
[0.0_0, 150000.0_2, 300000.0_1, 500000.0_3]___500000.0
[0.0_0, 150000.0_2, 300000.0_3, 300000.0_1]___500000.0
[0.0_0, 150000.0_3, 270000.0_1]___470000.0
[0.0_0, 150000.0_3, 270000.0_1]___470000.0
[0.0_1, 200000.0_0, 350000.0_2, 500000.0_3]___500000.0
[0.0_1, 200000.0_0, 350000.0_3]___470000.0
[0.0_1, 200000.0_2, 350000.0_0, 500000.0_3]___500000.0
[0.0_1, 200000.0_2, 350000.0_3]___550000.0
[0.0_1, 200000.0_3]___520000.0
[0.0_1, 200000.0_3]___520000.0
[0.0_2, 150000.0_0, 300000.0_1, 500000.0_3]___500000.0
[0.0_2, 150000.0_0, 300000.0_3, 300000.0_1]___500000.0
[0.0_2, 150000.0_1, 350000.0_0, 500000.0_3]___500000.0
[0.0_2, 150000.0_1, 350000.0_3]___550000.0
[0.0_2, 150000.0_3, 350000.0_1]___550000.0
[0.0_2, 150000.0_3, 350000.0_1]___550000.0
[0.0_3, 320000.0_1]___520000.0
[0.0_3, 320000.0_1]___520000.0
[0.0_3, 320000.0_1]___520000.0
[0.0_3, 320000.0_1]___520000.0
[0.0_3, 320000.0_1]___520000.0
[0.0_3, 320000.0_1]___520000.0
```


output:

![Plotly trie graph](https://github.com/Ternt/Display-Trie/assets/45267060/a70d235e-dc5f-4b43-8534-d140e6e2959d)


[^1]: https://medium.com/trendyol-tech/how-do-we-calculate-promotions-in-the-cart-85e7b50af2b6
