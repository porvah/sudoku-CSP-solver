from collections import deque
import copy


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.domains = self.initialize_domains()
        self.neighbors = self.generate_neighbors()
        self.lines = []

    def solve(self):
        if not self.arc_consistency_check():
            return False
        with open("arc.txt", "w") as f:
            f.write(self.lines)
        return self.backtrack()

    def initialize_domains(self):
        # Initialize domains with possible values (1-9) and reduce based on constraints
        domains = [[[i for i in range(1, 10)] for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    # Cell is pre-filled; set domain to its value and propagate constraints
                    domains[row][col] = [self.grid[row][col]]
                    for neighbor in self.get_neighbors(row, col):
                        if self.grid[neighbor[0]][neighbor[1]] == 0:
                            try:
                                domains[neighbor[0]][neighbor[1]].remove(self.grid[row][col])
                            except ValueError:
                                pass
        return domains

    def generate_neighbors(self):
        # Precompute neighbors for each cell
        neighbors = [[[] for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                neighbors[row][col] = self.get_neighbors(row, col)
        return neighbors

    def get_neighbors(self, row, col):
        # Find all neighbors of a cell in its row, column, and 3x3 subgrid
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

    def backtrack(self):
        if self.is_complete():
            return True
        
        var = self.select_MRV()
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

    def is_complete(self):
        return all(self.grid[row][col] != 0 for row in range(9) for col in range(9))

    def select_MRV(self):
        min_domain = float('inf')
        selected_var = None
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0 and len(self.domains[row][col]) < min_domain:
                    selected_var = (row, col)
                    min_domain = len(self.domains[row][col])
        return selected_var

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
