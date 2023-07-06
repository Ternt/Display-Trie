# Display-Tree
A program I am working on while interning as a backend developer at a vietnamese company called Mobile World JSC. A while back I was tasked with writing a program to visualize data structures in a way that was easy to understand. The data structure I had to visualize was a perfect generic (k-ary) tree based on this problem[^1]. Before, I didn't even know what the heck a generic tree was and now I have to build **AND** display it :|| 

Anyways, how it works is the program takes in two lists of vertices. One that is in preorder and the other in postorder. The program then recursively go through these two lists to build the tree, using the networkx python library, and finally display it, using the plotly python library.

Example input:  
```
postorder3 = [10,4,11,5,1,12,6,13,7,2,14,8,15,9,3,0]
preorder3 =  [0,1,4,10,5,11,2,6,12,7,13,3,8,14,9,15]
```
Example output:
![Screenshot_3](https://github.com/Ternt/Display-Tree/assets/45267060/4893ea1f-88fa-43b2-a5b8-cd7bc9623a21)

## TO DOs
1. As the program is built to depend on input to correctly build and display data, we need to make sure that that data being inputted is valid. Therefore, verification, validation, as well as error handling features will need to be implemented for the program to run smoothly.
   
2. Implement automated input of data. I have no idea what how to do this... But automation means less work **yay**!
3. Algorithm to relabel all the nodes. Should be simple assuming that the input contains label data.


[^1]: https://medium.com/trendyol-tech/how-do-we-calculate-promotions-in-the-cart-85e7b50af2b6
