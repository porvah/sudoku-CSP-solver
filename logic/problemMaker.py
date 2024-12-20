from logic.solver import Solver


class problemMaker(Solver):
    def __init__(self):
        empty_grid = [[0 for _ in range(9)] for _ in range(9)]
        super().__init__(empty_grid)
        self.solve() # gets a valid solution

    

    
    