import copy
import random
from logic.verifier import SudokuVerifier
from logic.solver import Solver
from logic.difficulty import Difficulty

class SudokuGenerator(Solver):
    def __init__(self):
        super().__init__([[0 for _ in range(9)] for _ in range(9)])

    def fill_grid(self):
        if not self.backtrack():
            raise ValueError("Failed to generate a complete Sudoku grid.")
        print(self.grid)
        return self.grid

    def has_unique_solution(self):
        verifier = SudokuVerifier(copy.deepcopy(self.grid))
        
        return verifier.solve() and verifier.solutions == 1

    def generate_puzzle(self, difficulty=Difficulty.MED):
        self.fill_grid()
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        clues_to_remove = 81- difficulty
        for row, col in cells:
            if clues_to_remove <= 0:
                break

            backup = self.grid[row][col]
            self.grid[row][col] = 0
            if not self.has_unique_solution():
                self.grid[row][col] = backup  
            else:
                clues_to_remove -= 1


        return self.grid

