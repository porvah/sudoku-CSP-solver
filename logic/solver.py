from collections import deque
import copy
import random


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.domains = self.initialize_domains()
        self.neighbors = self.generate_neighbors()
        self.lines = []


    # performing arc consistency before backtracking to reduce domains
    def solve(self):
        if not self.arc_consistency_check():
            return False
        value = self.backtrack()
        with open("arc.txt", "w") as f:
            f.writelines(self.lines)
        return value

    # filling the domains matrix
    def initialize_domains(self):
        domains = [[[i for i in range(1, 10)] for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    domains[row][col] = [self.grid[row][col]]
                    for neighbor in self.get_neighbors(row, col):
                        if self.grid[neighbor[0]][neighbor[1]] == 0:
                            try:
                                domains[neighbor[0]][neighbor[1]].remove(self.grid[row][col])
                            except ValueError:
                                pass
        return domains

    # stores neighbors for each cell
    def generate_neighbors(self):
        neighbors = [[[] for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                neighbors[row][col] = self.get_neighbors(row, col)
        return neighbors

    # gets the neighbors of a cell
    def get_neighbors(self, row, col):
        neighbors = set()
        for i in range(9):
            if i != col:
                neighbors.add((row, i))
            if i != row:
                neighbors.add((i, col))
        
        subgrid_row_start = (row // 3) * 3
        subgrid_col_start = (col // 3) * 3
        for r in range(subgrid_row_start, subgrid_row_start + 3):
            for c in range(subgrid_col_start, subgrid_col_start + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))
        return list(neighbors)

    # performs arc consistency
    def arc_consistency_check(self):
        queue = deque()
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    for neighbor in self.neighbors[row][col]:
                        queue.append(((row, col), neighbor))
        
        while queue:
            (Xi, Xj) = queue.popleft()
            if self.revise(Xi, Xj):
                xi_row, xi_col = Xi
                if not self.domains[xi_row][xi_col]:
                    return False  # Domain is empty
                for Xk in self.neighbors[xi_row][xi_col]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True
    # arc consistency revise
    def revise(self, Xi, Xj):
        revised = False
        xi_row, xi_col = Xi
        xj_row, xj_col = Xj

        domain_Xi = self.domains[xi_row][xi_col]
        domain_Xj = self.domains[xj_row][xj_col]

        for value in domain_Xi[:]:  # Iterate over a copy
            if not any(value != neighbor_value for neighbor_value in domain_Xj):
                s = ''
                s += 'D_old'+str((xi_row, xi_col))+str(domain_Xi)+'  '
                domain_Xi.remove(value)
                s += 'D_new'+str((xi_row, xi_col))+str(domain_Xi)+'  '
                s += 'D'+str((xj_row, xj_col))+str(domain_Xj)+'\n'
                self.lines.append(s)
                revised = True
        return revised

    # performs backtracking on the stored self.grid
    def backtrack(self , rand = False):
        if self.is_complete():
            return True
        
        var = self.select_MRV(rand) # the rand parameter is used to choose whether or not to get a random variable or to use mrv
        if var is None:
            return False
        row, col = var
        for value in self.get_LCV(var):
            self.grid[row][col] = value
            backup_domains = copy.deepcopy(self.domains)
            self.domains[row][col] = [value]
            if self.arc_consistency_check() and self.backtrack():
                return True
            self.grid[row][col] = 0
            self.domains = backup_domains
        return False

    # check for board completion
    def is_complete(self):
        return all(self.grid[row][col] != 0 for row in range(9) for col in range(9))

    # selects the mrv by iterating through the domains of the cells and selecting the valid cell with the least domain size
    def select_MRV(self , rand = False):
        if rand: # selects a random valid cell instead (used in generation)
            row_val = random.randint(0, 8)
            col_val = random.randint(0, 8)
            
            while self.grid[row_val][col_val] != 0:
                row_val = random.randint(0, 8)
                col_val = random.randint(0, 8)
            selected = (row_val , col_val)
            return selected
        
        min_domain = float('inf')
        selected_var = None
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0 and len(self.domains[row][col]) < min_domain:
                    selected_var = (row, col)
                    min_domain = len(self.domains[row][col])
        return selected_var

    # select the least constrainig value by getting selecting the value that least affects its neighbors domains
    def get_LCV(self, var):
        row, col = var
        neighbors = self.neighbors[row][col]

        def lcv_score(value):
            score = 0
            for neighbor in neighbors:
                neighbor_row, neighbor_col = neighbor
                if value in self.domains[neighbor_row][neighbor_col]:
                    score += 1
            return score

        return sorted(self.domains[row][col], key=lcv_score)
