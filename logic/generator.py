import copy
import random
from logic.grid_verifier import GridVerifier
from logic.solver import Solver
from logic.difficulty import Difficulty

class SudokuGenerator(Solver):
    def __init__(self):
        super().__init__([[0 for _ in range(9)] for _ in range(9)])
        self.saved_grid = None

    # performs backtracking to get a valid solution
    def fill_grid(self):
        if not self.backtrack(rand = True): # rand=true to get new puzzle solution each time
            raise ValueError("Failed to generate a complete Sudoku grid.")
        self.saved_grid = copy.deepcopy(self.grid)
        print(self.grid)
        return self.grid
    
    # uses verifier to check for puzzle uniqueness
    def has_unique_solution(self): 
        verifier = GridVerifier(copy.deepcopy(self.grid))

        return verifier.solve() and verifier.solutions == 1

    # gets a random puzzle by generating a random solution and taking away random cells
    # each time a cell is set to 0 a uniqueness is performed to ensure that the puzzle still has a unique solution
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
    
    # check if the user input is valid
    def is_valid_input(self ,board):
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0 and board[i][j] != self.saved_grid[i][j]:
                    return False
        return True


