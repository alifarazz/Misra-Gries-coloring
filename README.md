# Misra-Gries edge coloring

An implementation of ["Misra & Gries edge coloring algorithm"](https://www.cs.utexas.edu/users/misra/psp.dir/vizing.pdf) in python ~~and networkX~~.

#### How to use
* **Input**: On the first line, type `|V|` and `|E|`. Then, for each line, type in the edges by the index of their end-point vertices. Vertex indices must be 0-based.

* **Output**: For the first line, the max degree of the graph (`Δ`) and max number of colors used (`ᵪ′`) is printed. For each next line, the first two integer represent the end-points of an edge in the input graph and the third integer its color.

Have a look at examples at [generated testcases](https://codeberg.org/alifara/Misra-Gries-coloring/src/branch/master/generated%20testcases) folder.

##### For example


```sh
$ python main.py
5 8
0 1
0 2
0 3
1 2
1 4
2 3
2 4
3 4

4 4
0 1 3
0 2 4
0 3 1
1 2 2
1 4 4
2 3 3
2 4 1
3 4 2
```


![plot of the exmaple graph and its coloring](.media/exmaple.png "plot of the graph in the exmaple")

### Notebook View

* [jupyter notebook/visual_implementation.ipynb](https://nbviewer.jupyter.org/urls/codeberg.org/alifara/Misra-Gries-coloring/raw/branch/master/jupyter%20notebook/visual_implementation.ipynb)
