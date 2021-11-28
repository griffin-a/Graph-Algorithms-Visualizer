# A Graph Algorithm Visualizer
## _W.I.P. pygame simulation app for graph algorithms_

My attempt at a graph algorithm visualizer in pygame. To be extended in the future. 
Determines the shortest path from source to end (solves the SSSP to accomplish this).

## Current Features

- Grid visualization of Dijkstra's Algorithm using Euclidean distance.
- Ability to add walls to grid for the algorithm to navigate past to get to destination.

## Running the program
### SimplifiedVersion branch
Please ensure that you are on the "SimplifiedVersion" branch; run the main method in "main.py".

Left clicking enables you to set the "start", "end" and any "wall" squares in that order. Note that you must first set the "start" square before you can set the "end" square; you also must set the "end" square before you can create any walls.

To start the algorithm visualization, press space once you have set all of the desired squares. Please note that at this stage, error handling isn't fully implemented. Deletion of squares is not yet completed either. 

### Main branch

## Credit/References
The "main" branch has code based on an MVC structure for pygame as outlined by [wesleywerner](https://github.com/wesleywerner) on Github. All credit goes to [wesleywerner](https://github.com/wesleywerner) for his work on an MVC design pattern implementation for pygame.

Please refer to this repository to see his work: [mvc-game-design](https://github.com/wesleywerner/mvc-game-design).

