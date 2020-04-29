# Pathfinding algorithms visualization
Visualization of A* and Dijkstra search algorithms made with pygame, with the possibility to draw obstacles and see how the algorithms search for the best path.

## Info
A* is an informed search algorithm, or a best-first search, meaning that it is formulated in terms of weighted graphs: starting from a specific starting node of a graph, it aims to find a path to the given goal node having the smallest cost (least distance travelled, shortest time, etc.). It does this by maintaining a tree of paths originating at the start node and extending those paths one edge at a time until its termination criterion is satisfied.
Dijkstra's algorithm, as another example of a uniform-cost search algorithm, can be viewed as a special case of A* where h(x) = 0 for all x. [WIKI](https://en.wikipedia.org/wiki/A*_search_algorithm)

## Preview
### A*  
![astar](http://g.recordit.co/phfFL5uHwO.gif)

### Dijkstra
![dijkstra](http://g.recordit.co/JrMaXw6vGS.gif)

## How to use it
Run *main.py*, draw the obstacles and press the Spacebar. By default it will run A*, to run Dijkstra, just put
```python
board = Board(dijkstra=True)
board.main()
```

## Requirements
Python version: 3
Libraries: pygame

## License
This project is licensed under the **MIT License** - see the *LICENSE.md* file for details
