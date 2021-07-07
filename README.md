# nballsnscale

GOAL
----
Solving puzzles of type "There are N identical balls, except that one weighs imperceptibly less / more / differently; you can make W weighings on a two-plate precision scale. Identify the different ball (and tell if it is lighter or heavier)."

ALGORITHM
---------
The class GameSolver tries to solve the game by means of a fully deterministic algorithm identifying in any situation which possible weighing is the optimal one and then making all possible deductions from the outcome of the weighing. At every point of the game, it tracks the list of still possible solutions, such as: ball X could be lighter, ball Y could be heavier,  ball Z could be lighter or heavier, ...

To keep the search space of possible weighings manageably small, it considers just one weighing for each class of weighings that would deliver equivalent information content; in other words, it removes permutations of balls on which the same information is already known.

The weighings are ranked so as to maximize the minimum [information content](https://en.wikipedia.org/wiki/Information_content) yielded by any of their possible outcomes in the unluckiest possible circumstances, recursively; in other words, each weighing is scored by the vector of its descending outcome frequencies (based on the remaining possible solutions) and the lowest vector, sorting in the natural order, is preferred. Furthermore, the number of balls being weighted is used as a secondary rank to distinguish between weighings with the same primary rank, so that a weighing involving fewer balls is preferred.

TESTING
-------
The main script main.py tests the algorithm by testing all possible solutions on two different problems of this type:
1. 12 balls, of which one weighs sligthly differently, either less or more; this problem can be solved correctly with 100% probability.
2. 13 balls, of which one weighs sligthly differently, either less or more; this problem can be solved correctly only with 96.15% probability.
