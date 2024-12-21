class SudokuVerifier:
    def __init__(self, grid):
        self.grid = grid
        self.solutions = 0

    def is_valid(self, row, col, value):
        # Check row
        if value in self.grid[row]:
            return False
        # Check column
        if value in [self.grid[r][col] for r in range(9)]:
            return False
        # Check subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.grid[r][c] == value:
                    return False
        return True

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def solve(self):
        empty = self.find_empty()
        if not empty:
            self.solutions += 1
            return self.solutions == 1  # Stop if more than one solution
        row, col = empty
        for value in range(1, 10):
            if self.is_valid(row, col, value):
                self.grid[row][col] = value
                if not self.solve():
                    return False  # More than one solution
                self.grid[row][col] = 0
        return self.solutions < 2  # Unique if solutions < 2