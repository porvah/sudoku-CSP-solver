from logic.solver import Solver

class GridVerifier(Solver):
    def __init__(self, grid):
        self.solutions = 0
        super().__init__(grid)

    # performs backtracking but stopping when 2 solutions are found instead of 1
    # this helps identify whether the generated grid has unique and valid solution or not
    def verify_grid(self):
        empty = self.select_MRV() 
        if not empty:
            self.solutions += 1
            return self.solutions < 2

        vrow, vcol = empty
        domain_backup = self.domains[vrow][vcol].copy()

        for value in self.get_LCV((vrow, vcol)):
            self.grid[vrow][vcol] = value
            domain_backup.remove(value)
            if self.arc_consistency_check():
                if not self.verify_grid():
                    return False
            self.grid[vrow][vcol] = 0
            self.domains[vrow][vcol] = domain_backup

        return self.solutions < 2
    
    def solve(self):
        if not self.arc_consistency_check():
            return False

        if self.verify_grid():
            return self.solutions == 1
        return False
        
        
