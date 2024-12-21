import copy
from logic.solver import Solver


class problemMaker(Solver):
    def __init__(self):
        empty_grid = [[0 for _ in range(9)] for _ in range(9)]
        super().__init__(empty_grid)
        self.solve() # gets a valid solution

    def generative_backtrack(self):
        # Check if the grid is completely filled with valid values
        if self.complete_check():
            print("Solution found:", self.grid)
            return 1  # Valid solution found

        # Select the next variable using MRV heuristic
        var = self.select_MRV()
        if not var:
            print("No variables left but incomplete grid.")
            return 0  # No variables to assign, but not complete
        
        vrow, vcol = var
        backup_grid = copy.deepcopy(self.grid)
        backup_domain = copy.deepcopy(self.domains)
        count = 0

        # Iterate over the values using LCV heuristic
        for assigned_value in self.get_LCV(var):
            print(f"Trying value {assigned_value} for cell ({vrow}, {vcol})")
            self.grid[vrow][vcol] = assigned_value
            if self.arc_consistency_check():
                print(f"Grid after assigning {assigned_value}:\n{self.grid}")
                self.update_grid()
                val = self.generative_backtrack()
                count += val  # Add the number of solutions found
                if count > 1:
                    print("More than one solution found. Terminating...")
                    return 2  # More than one solution found, terminate early
            # Restore the grid and domains
            print(f"Restoring grid after trying {assigned_value}")
            self.grid = copy.deepcopy(backup_grid)
            self.domains = copy.deepcopy(backup_domain)

        return count

    
    def make_game(self):
        pass




    

    
    