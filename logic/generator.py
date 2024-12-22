import copy
import random
from logic.solver import Solver
from logic.difficulty import Difficulty

class SudokuGenerator(Solver):
    def __init__(self):
        super().__init__([[0 for _ in range(9)] for _ in range(9)])
        self.saved_grid = None

    def fill_grid(self):
        if not self.solve():
            raise ValueError("Failed to generate a complete Sudoku grid.")
        self.saved_grid = copy.deepcopy(self.grid)
        return self.grid

    def generate_puzzle(self, difficulty=Difficulty.MED):
        print(difficulty)
        # Generate complete board
        self.fill_grid()

        # remove cells randomly
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        clues_to_remove = 81 - difficulty

        for row, col in cells:
            if clues_to_remove <= 0:
                break

            # Backup the current cell
            backup = self.grid[row][col]
            self.grid[row][col] = 0

            # Check if the board is solvable
            solver = Solver(copy.deepcopy(self.grid))
            if not solver.solve():
                # Restore the cell 
                self.grid[row][col] = backup
            else:
                clues_to_remove -= 1

        return self.grid
    
    # check if the user input is valid
    def is_valid_input(self ,board):
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0 and board[i][j] != self.saved_grid[i][j]:
                    return False
        return True


