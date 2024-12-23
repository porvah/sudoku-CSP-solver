import copy
import random
import time
import customtkinter as ctk
from logic.difficulty import Difficulty
from logic.generator import SudokuGenerator
from logic.solver import Solver
from logic.grid_verifier import GridVerifier

class Gui(ctk.CTk):
    def setup(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.player_creating = False
        self.player_solving = False
        self.generator = SudokuGenerator()
        self.original_board = None  # To store the initial state for verification
        
    def __init__(self):
        self.setup()
        super().__init__()

        # Window configuration
        self.title("Sudoku Game")
        self.geometry("1020x760")
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Grid configuration
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=2)

        # Solving Mode Radio Buttons
        self.solve_mode_label = ctk.CTkLabel(self.main_frame, text="Solving Mode", font=("Arial", 16))
        self.solve_mode_label.grid(row=0, column=0, pady=(20, 10), padx=(10, 10), sticky="w")

        self.solve_mode_var = ctk.StringVar(value="none")
        self.solve_mode_var.trace_add("write", self.on_solve_mode_change)

        self.solve_mode_frame = ctk.CTkFrame(self.main_frame)
        self.solve_mode_frame.grid(row=1, column=0, pady=10, padx=(10, 10), sticky="w")

        solve_modes = [
            ("AI Solving", "ai"),
            ("Player Solving", "player"),
            ("None", "none")
        ]

        for text, value in solve_modes:
            radio = ctk.CTkRadioButton(
                self.solve_mode_frame,
                text=text,
                variable=self.solve_mode_var,
                value=value
            )
            radio.pack(side="left", padx=10)

        # Creation Mode Dropdown
        self.create_mode_label = ctk.CTkLabel(self.main_frame, text="Creation Mode", font=("Arial", 16))
        self.create_mode_label.grid(row=2, column=0, pady=(20, 10), padx=(10, 10), sticky="w")

        self.create_mode_var = ctk.StringVar(value="none")
        self.create_mode_var.trace_add("write", self.on_create_mode_change)

        self.create_mode_dropdown = ctk.CTkOptionMenu(
            self.main_frame,
            values=["AI Creating", "Player Creating"],
            variable=self.create_mode_var
        )
        self.create_mode_dropdown.grid(row=3, column=0, pady=10, padx=(10, 10), sticky="w")

        # AI Solve Button (for player creation mode)
        self.ai_solve_button = ctk.CTkButton(
            self.main_frame,
            text="AI Solve",
            command=self.ai_solve_puzzle,
            state="disabled"
        )
        self.ai_solve_button.grid(row=3, column=0, pady=10, padx=(200, 10), sticky="w")

        # Difficulty Dropdown
        self.difficulty_label = ctk.CTkLabel(self.main_frame, text="Difficulty Level", font=("Arial", 16))
        self.difficulty_label.grid(row=2, column=0, pady=(20, 10), padx=(200, 10), sticky="w")

        self.difficulty_var = ctk.StringVar(value="Medium")
        self.difficulty_dropdown = ctk.CTkOptionMenu(
            self.main_frame,
            values=["Easy", "Medium", "Hard"],
            variable=self.difficulty_var
        )
        self.difficulty_dropdown.grid(row=3, column=0, pady=10, padx=(200, 10), sticky="w")

        # AI Solve Button
        self.ai_solve_button = ctk.CTkButton(
            self.main_frame,
            text="AI Solve",
            command=self.ai_solve_puzzle,
            state="disabled"
        )
        self.ai_solve_button.grid(row=3, column=0, pady=10, padx=(400, 10), sticky="w")


        # Add Clear Button
        self.clear_button = ctk.CTkButton(
            self.main_frame,
            text="Clear",
            command=self.clear_board
        )
        self.clear_button.grid(row=5, column=0, pady=10, padx=(10, 10), sticky="w")


        # Sudoku Grid
        self.grid_frame = ctk.CTkFrame(self.main_frame)
        self.grid_frame.grid(row=4, column=0, pady=20, padx=10, sticky="w")

        self.grid_cells = []
        for row in range(9):
            row_cells = []
            for col in range(9):
                color = "white" if (row//3 + col//3) % 2 == 0 else "light grey"
                cell = ctk.CTkEntry(
                    self.grid_frame,
                    width=50,
                    height=50,
                    font=("Arial", 20),
                    justify="center",
                    fg_color=color
                )
                cell.grid(row=row, column=col, padx=1, pady=1)
                cell.bind('<Return>', lambda e, r=row, c=col: self.on_cell_enter(r, c))
                cell.bind('<FocusOut>', lambda e, r=row, c=col: self.on_cell_focus_out(r, c))
                row_cells.append(cell)
            self.grid_cells.append(row_cells)

        # Status and Notes Area
        self.text_area = ctk.CTkTextbox(self.main_frame, width=500, height=680, font=("Arial", 14))
        self.text_area.grid(row=1, column=1, rowspan=4, padx=(20, 10), pady=10, sticky="nsew")
        self.text_area.configure(state="disabled")
        
        
        self._update_grid()
        self._update_status("Welcome to Sudoku! Select a mode to begin.")

    def on_solve_mode_change(self, *args):
        mode = self.solve_mode_var.get()
        if mode == "ai":
            self.player_solving = False
            if self.original_board:
                start = time.time()
                solver = Solver(self.original_board)
                if solver.solve():
                    self.board = solver.grid
                    self._update_grid()
                    self._update_status("AI has solved the puzzle!")
                else:
                    self._update_status("This puzzle cannot be solved!")
                duration = time.time() - start
                self._update_status(f"Time taken: {duration:.2f} seconds")
        elif mode == "player":
            self.player_solving = True
            self._update_status("Player solving mode activated. Enter numbers and press Enter to validate.")
        else:
            self.player_solving = False
            self._update_status("Select a mode to begin.")

    def get_difficulty_level(self):
        difficulty_map = {
            "Easy": Difficulty.EASY,
            "Medium": Difficulty.MED,
            "Hard": Difficulty.HARD
        }
        return difficulty_map[self.difficulty_var.get()]

    def on_create_mode_change(self, *args):
        mode = self.create_mode_var.get()
        if mode == "AI Creating":
            self.player_creating = False
            difficulty = self.get_difficulty_level()
            start = time.time()
            self.board = self.generator.generate_puzzle(difficulty)
            self.original_board = copy.deepcopy(self.board)
            self._update_grid()
            self._update_status(f"AI has created a new {self.difficulty_var.get()} puzzle. Select solving mode to continue.")
            duration = time.time() - start
            self._update_status(f"Time taken: {duration:.2f} seconds")
            self.ai_solve_button.configure(state="disabled")
        elif mode == "Player Creating":
            self.player_creating = True
            self.board = [[0 for _ in range(9)] for _ in range(9)]
            self._update_grid()
            self._update_status("Create your puzzle. Enter numbers and press Enter to validate. Click 'AI Solve' when done.")
            self.ai_solve_button.configure(state="normal")

    def on_cell_enter(self, row, col):
        try:
            value = int(self.grid_cells[row][col].get())
            if 1 <= value <= 9:
                if self.player_solving:
                    # Verify move in player solving mode
                    temp_board = copy.deepcopy(self.board)
                    temp_board[row][col] = value
                    if self.generator.is_valid_input(temp_board):
                        self.board[row][col] = value
                        self._update_status("Valid move!")
                    else:
                        self.grid_cells[row][col].delete(0, "end")
                        if self.board[row][col] != 0:
                            self.grid_cells[row][col].insert(0, str(self.board[row][col]))
                        self._update_status("Invalid move! Try again.")
                elif self.player_creating:
                    # Update both the visual grid and the internal board
                    self.board[row][col] = value
                    self._update_status(f"Added {value} at position ({row+1}, {col+1})")
            else:
                raise ValueError
        except ValueError:
            self.grid_cells[row][col].delete(0, "end")
            if self.board[row][col] != 0:
                self.grid_cells[row][col].insert(0, str(self.board[row][col]))
            self._update_status("Please enter a number between 1 and 9.")

    def ai_solve_puzzle(self):
        if self.player_creating:
            # Create a numerical board from the current grid state
            numerical_board = [[0 for _ in range(9)] for _ in range(9)]
            for row in range(9):
                for col in range(9):
                    cell_value = self.grid_cells[row][col].get()
                    if cell_value:
                        try:
                            numerical_board[row][col] = int(cell_value)
                        except ValueError:
                            numerical_board[row][col] = 0
            
            # Update the internal board state
            self.board = numerical_board
            
            # Print for debugging
            print("Current board state:")
            for row in self.board:
                print(row)
            gridVerifier = GridVerifier(copy.deepcopy(self.board))
            if gridVerifier.verify_grid():
                solver = Solver(self.board)
                if solver.solve():
                    self.board = solver.grid
                    self._update_grid()
                    self._update_status("Puzzle solved successfully!")
                else:
                    self._update_status("This puzzle cannot be solved!")
            else:
                self._update_status("Invalid puzzle! please enter a puzzle with a unique solution")

    def on_cell_focus_out(self, row, col):
        if not self.grid_cells[row][col].get() and self.board[row][col] != 0:
            self.grid_cells[row][col].insert(0, str(self.board[row][col]))


    def _update_grid(self):
        for row in range(9):
            for col in range(9):
                self.grid_cells[row][col].delete(0, "end")
                if self.board[row][col] != 0:
                    self.grid_cells[row][col].insert(0, str(self.board[row][col]))

    def _update_status(self, message):
        self.text_area.configure(state="normal")
        self.text_area.insert("end", f"\n{message}")
        self.text_area.see("end")
        self.text_area.configure(state="disabled")
    def clear_board(self):
        # Reset the internal board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = None
        self.player_creating = False
        self.player_solving = False

        # Reset the grid cells
        self._update_grid()

        # Reset dropdowns and radio buttons
        self.solve_mode_var.set("none")
        self.create_mode_var.set("none")
        self.difficulty_var.set("Medium")

        # Clear the status text area
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", "end")
        self.text_area.configure(state="disabled")

        # Disable AI Solve button
        self.ai_solve_button.configure(state="disabled")

        # Update status
        self._update_status("Board cleared! Select a mode to start fresh.")
