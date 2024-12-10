import random
import customtkinter as ctk

class Gui(ctk.CTk):
    def setup(self):
        self.board = [['0' for _ in range(9)] for _ in range(9)]
        
    def __init__(self):
        self.setup()
        super().__init__()

        # Window configuration
        self.title("Sudoku Game")
        self.geometry("1020x760")
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # 2 Columns and 5 Rows are used
        # Create a grid for layout with two columns (left for Sudoku, right for the text area)
        self.main_frame.grid_columnconfigure(0, weight=3)
        self.main_frame.grid_columnconfigure(1, weight=2)

        # Solving Mode Radio Buttons
        self.solve_mode_label = ctk.CTkLabel(self.main_frame, text="Solving Mode", font=("Arial", 16))
        self.solve_mode_label.grid(row=0, column=0, pady=(20, 10), padx=(10, 10), sticky="w")

        self.solve_mode_var = ctk.StringVar(value="none")
        self.solve_mode_var.trace_add("write", self.on_solve_mode_change)  # Track changes

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
        self.create_mode_var.trace_add("write", self.on_create_mode_change)  # Track changes

        self.create_mode_dropdown = ctk.CTkOptionMenu(
            self.main_frame,
            values=["AI Creating", "Player Creating"],
            variable=self.create_mode_var
        )
        self.create_mode_dropdown.grid(row=3, column=0, pady=10, padx=(10, 10), sticky="w")

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
                
                cell.delete(0, "end") # Clear whatever is in the cell
                if str(self.board[row][col]) != '0':
                    cell.insert(0, self.board[row][col])
                cell.grid(row=row, column=col, padx=1, pady=1)

                row_cells.append(cell)
            self.grid_cells.append(row_cells)

        # notes label
        self.notes_label = ctk.CTkLabel(self.main_frame, text="NOTES CAN BE ADDED HERE", font=("Arial", 12))
        self.notes_label.grid(row=0, column=1, padx=(20, 10), pady=(10, 20), sticky="w")

        
        self.text_area = ctk.CTkTextbox(self.main_frame, width=500, height=680, font=("Arial", 14))
        self.text_area.grid(row=1, column=1, rowspan=4, padx=(20, 10), pady=10, sticky="nsew")

        # Make the text area uneditable
        self.text_area.insert("0.0", "Here we go again " * 200)  # Example text
        self.text_area.configure(state="disabled")  # Make the text area uneditable

    def on_solve_mode_change(self, *args):
        if self.solve_mode_var.get() == "AI Solving":
            pass
        elif self.solve_mode_var.get() == "Player Solving":
            self.player_creating = False
            self.player_solving = True
            pass
        else:
            pass

    def on_create_mode_change(self, *args):
        if self.create_mode_var.get() == "AI Creating":
            self.player_creating = False
            # ##############################
            # REPLACE ME 
            self.board = [random.choices(range(0, 10), k=9) for _ in range(9)]
            # ##############################
            self._update_grid()
        elif self.create_mode_var.get() == "Player Creating":
            self.board = [['0' for _ in range(9)] for _ in range(9)]
            self._update_grid()
            self.player_creating = True
    
            
            
    def _update_grid(self):
        for row in range(9):
            for col in range(9):
                self.grid_cells[row][col].delete(0, "end")
                if str(self.board[row][col]) != '0':
                    self.grid_cells[row][col].insert(0, str(self.board[row][col]))  
        
        
