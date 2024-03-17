# 15-Puzzle-Game


# 15 Puzzle Game
Assignment for Laboratory of Artificial Intelligence Class, 2º Year,2º Semester, Bachelor in Artificial Intelligence and Data Science Project 2 – Use different algorithms to solve the 15 puzzle game

# Summary

In this project we implemented a simple interface so we can play the game and some algorithms and heuristics to be able to get to the solution in the minimum number os steps required.


**Autors**:
- [Rui Coelho](https://github.com/ruipmc)
- [Alexandre Marques]
- [Miguel Silva]


# Requirements

To install the requirements run:

```bash
pip install tk
```

# Usage

To use our project you need to give some arguments when running the main file:
- Initial configuration of the puzzle (all numbers from 0 to 15 with spaces between them with the order you choose)
- Final configuration of the puzzle (similar to the initial one, generaly it is 1 to 15 and 0 at the end)
- The algorithm you want to use:
  -- A* algorithm with the mannhatan distance heuristic -> A*-Manhattan
  -- A* algorithm with the sum of all pieces out of place heuristic -> A*-misplaced
  -- Greedy algorithm with the mannhatan distance heuristic -> Greedy-Manhattan
  -- Greedy algorithm with the sum of all pieces out of place heuristic -> Greedy-misplaced
  -- Iterative deepening search -> IDFS
  -- Depth first search -> DFS (takes too long to reach the answer)
  -- Depth first search -> depth (alternative to DFS)
  -- Breadth first search -> BFS
