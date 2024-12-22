from logic.solver import Solver
import copy
# for player mode
class gridVerifier:
    def verify_grid(grid):
        print(grid)
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != 0:
                    count += 1

        if count < 17:
            return False
        
        solver = Solver(copy.deepcopy(grid))
        return solver.solve()
        
        
