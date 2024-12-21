from logic.solver import Solver

class SudokuVerifier(Solver):
    def __init__(self, grid):
        self.solutions = 0
        super().__init__(grid)

    def solve_for_verification(self):
        empty = self.select_MRV() 
        if not empty:
            self.solutions += 1
            # Stop searching if more than one solution is found
            return self.solutions < 2

        vrow, vcol = empty
        domain_backup = self.domains[vrow][vcol].copy()

        for value in self.get_LCV((vrow, vcol)):
            self.grid[vrow][vcol] = value
            domain_backup.remove(value)
            # Propagate constraints
            if self.arc_consistency_check():
                if not self.solve_for_verification():
                    return False
            # Restore grid state
            self.grid[vrow][vcol] = 0
            self.domains[vrow][vcol] = domain_backup

        return self.solutions < 2

    def solve(self):
        # Perform arc consistency
        if not self.arc_consistency_check():
            return False

        if self.solve_for_verification():
            return self.solutions == 1
        return False