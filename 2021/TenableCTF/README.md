# Is the King in Check? (Coding - 200 pts)

This chall is fairly simple, it can be solved by checking for threats from enemy pieces:
- For enemy queen, rooks, bishops: check the closest piece in all horizontal, vertical and diagonal directions
- For enemy knights: check all 8 possible attacking positions
- For enemy pawns: check 2 possible attacking positions

Full solver code: [kingcheck_solve.py](kingcheck_solve.py)
(Boundary checks can be ignored, test cases do not include them. Code can be shortened further, but this was how our team solved the chall :P)
