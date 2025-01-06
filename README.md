# Cagey-Grids
AI Course Assignment on Heuristics and Propagators
Assignment Created by Christian Muise at Queen's University

# Propagators
Both plain backtracking propagation and forward checking propagation with pruning

# Heuristics
Variable ordering heuristic that chooses based on the Degree heuristic (DH).
Variable ordering heuristic that chooses based on the  Minimum-Remaining-Value (MRV) heuristic.

# Tasks
Build:
A model of a Cagey grid (without cage constraints) built using only binary not-equal constraints for both the row and column constraints.

A model of a Cagey grid (without cage constraints) built using only n-ary all-different constraints for both the row and column constraints.

A model built using above constraints for the grid, together with cage constraints.

![Screen Shot 2025-01-05 at 8 18 37 PM](https://github.com/user-attachments/assets/864e829a-c5fb-41b8-ad87-0fb48f0634d2)

Cagey grid columns and rows have numbers 1 - n, where n x n is the size of the grid.
The grid is further broken down into multiple sections. Each section has a target number and an operator.
All the numbers in the section must equal the target number using the operator.
