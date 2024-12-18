class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.domains = self.get_domains()
        self.neighbors = self.gen_neighbors()

    def solve(self):
        if not self.arc_consistency_check():
            return False
        # <---- update grid here
        return self.backtrack()

    def select_MRV(self):
        var = None
        min_domain = 10
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0 and len(self.domains[row][col]) < min_domain:
                    var = (row, col)
                    min_domain = len(self.domains[row][col])
        return var

    def get_LCV(self, var):
        if var == None:
            return []
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

    def arc_consistency_check(self):
        q = []
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    for k, l in self.neighbors[i][j]:
                        if self.grid[i][j] == 0:
                            q.append([(i,j), (k, l)])
        
        while q:
            Xi, Xj = q.pop(0)
            if self.revise(Xi, Xj):
                rowi, coli = Xi
                if len(self.domains[rowi][coli]) == 0:
                    return False
                for Xk in self.neighbors[rowi][coli]:
                    if Xk != Xj and self.grid[Xk[0]][Xk[1]] != 0:
                        q.append((Xk, Xi))
        return True

    def revise(self, Xi, Xj):
        revised = False
        rowi, coli = Xi
        rowj, colj = Xj
        Di = self.domains[rowi][coli]
        Dj = self.domains[rowj][colj]
        for x in Di:
            if len(Dj) == 1 and x in Dj:
                self.domains[Xi[0]][Xi[1]].remove(x)
                revised = True
        return revised


        

    def backtrack(self):
        if self.complete_check():
            return True
        vrow, vcol = var = self.select_MRV()
        for assigned_value in self.get_LCV(var):
            self.grid[vrow][vcol] = assigned_value
            if self.arc_consistency_check():
                # <---- update grid here
                if self.backtrack():
                    return True
            self.grid[vrow][vcol] = 0
        return False

    
    def complete_check(self):
        return all(self.grid[row][col] != 0 for row in range(9) for col in range(9))
    
    def get_domains(self):
        res = [[ [i for i in range(1,10)] for _ in range(9)] for j in range(9)]
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    res[row][col] = [self.grid[row][col]]
        return res
    def gen_neighbors(self):
        res = [[0 for _ in range(9)]for i in range(9)]
        for row in range(9):
            for col in range(9):
                neighbors = []
                for i in range(9):
                    if i != col:
                        neighbors.append((row, i))
                    if i != row:
                        neighbors.append((i, col))

                subgrid_row_start = (row // 3) * 3
                subgrid_col_start = (col // 3) * 3

                for r in range(subgrid_row_start, subgrid_row_start + 3):
                    for c in range(subgrid_col_start, subgrid_col_start + 3):
                        if (r, c) != (row, col):
                            neighbors.append((r, c))
                res[row][col] = neighbors
        return res

grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
grid2 = [
    [5, 3, 9, 7, 9, 7, 4, 1, 1],
    [0, 1, 2, 7, 6, 1, 2, 8, 0],
    [7, 6, 9, 2, 5, 1, 6, 9, 8],
    [1, 6, 4, 3, 4, 2, 3, 9, 7],
    [5, 4, 7, 4, 6, 4, 6, 3, 3],
    [8, 7, 1, 2, 9, 6, 7, 9, 1],
    [6, 8, 5, 5, 4, 2, 6, 3, 2],
    [8, 9, 3, 8, 5, 3, 1, 8, 8],
    [3, 4, 7, 4, 5, 0, 8, 2, 5]
]
solver = Solver(grid)
print(solver.solve())
mat= solver.grid
for row in mat:
    print(row)
# print(solver.get_LCV((0,2)))