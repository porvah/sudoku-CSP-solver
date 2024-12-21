import copy
from logic.solver import Solver


class problemMaker(Solver):
    def __init__(self):
        empty_grid = [[0 for _ in range(9)] for _ in range(9)]
        super().__init__(empty_grid)
        self.solve() # gets a valid solution

    def generative_backtrack(self):
        if self.complete_check():
            return 1  # Valid solution found
        var = self.select_MRV()
        if not var:
            return 0  # No variables to assign, but not complete
        
        vrow, vcol = var
        backup_grid = copy.deepcopy(self.grid)
        backup_domain = copy.deepcopy(self.domains)
        count = 0

        for assigned_value in self.get_LCV(var):
            self.grid[vrow][vcol] = assigned_value
            if self.arc_consistency_check():
                self.update_grid()
                val = self.generative_backtrack()
                count += val  # Add the number of solutions found
                if count > 1:
                    return 2  # More than one solution
            # Restore state
            self.grid = copy.deepcopy(backup_grid)
            self.domains = copy.deepcopy(backup_domain)

        return count

    
    def make_game(self):
        pass




    

    
    