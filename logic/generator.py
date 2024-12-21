import random
import copy
from logic.verifier import SudokuVerifier
from logic.difficulty import Difficulty

class SudokuGenerator:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, row, col, value):
        if value in self.grid[row]:
            return False
        if value in [self.grid[r][col] for r in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.grid[r][c] == value:
                    return False
        return True

    def fill_grid(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for num in numbers:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.fill_grid():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def has_unique_solution(self):
        verifier = SudokuVerifier(copy.deepcopy(self.grid))
        return verifier.solve() and verifier.solutions == 1

    def make_puzzle(self, num_clues=Difficulty.MED):
        self.fill_grid()
       
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        removed_cells = 81 - int(num_clues)
        for row, col in cells:
            if removed_cells <= 0:
                break
            backup = self.grid[row][col]
            self.grid[row][col] = 0
            if not self.has_unique_solution():
                self.grid[row][col] = backup  
            else:
                removed_cells -= 1
        
        return self.grid