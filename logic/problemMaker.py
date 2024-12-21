import copy
from logic.solver import Solver


class problemMaker(Solver):
    def __init__(self):
        empty_grid = [[0 for _ in range(9)] for _ in range(9)]
        super().__init__(empty_grid)
        self.solve() # gets a valid solution
        self.is_unique = False

    def generative_backtrack(self):
        if self.complete_check():
            return True , None
        vrow, vcol = var = self.select_MRV()
        backup_grid = copy.deepcopy(self.grid)
        backup_domain = copy.deepcopy(self.domains)
        for assigned_value in self.get_LCV(var):
            self.grid[vrow][vcol] = assigned_value
            if self.arc_consistency_check():
                self.update_grid()
                val , _ = self.generative_backtrack()
                if val:
                    if not self.is_unique:
                        print("123")
                        self.is_unique = True
                    else:
                        print("1234")
                        return True , False
            self.grid = backup_grid
            self.domains = backup_domain
            if self.is_unique:
                return True , True
            else:
                return False , False
        return False , False
    
    def make_game(self):
        pass




    

    
    