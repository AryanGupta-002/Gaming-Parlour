import tkinter as tk
from tkinter import messagebox
import copy
import random
PUZZLES = [
    [
        [5,3,0, 0,7,0, 0,0,0],
        [6,0,0, 1,9,5, 0,0,0],
        [0,9,8, 0,0,0, 0,6,0],

        [8,0,0, 0,6,0, 0,0,3],
        [4,0,0, 8,0,3, 0,0,1],
        [7,0,0, 0,2,0, 0,0,6],

        [0,6,0, 0,0,0, 2,8,0],
        [0,0,0, 4,1,9, 0,0,5],
        [0,0,0, 0,8,0, 0,7,9],
    ],

    [
        [0,0,4, 0,0,0, 8,0,5],
        [0,3,0, 0,0,0, 0,0,0],
        [0,0,0, 7,0,0, 0,0,0],

        [0,0,0, 0,6,0, 0,0,0],
        [0,0,0, 9,0,1, 0,0,0],
        [0,0,0, 0,2,0, 0,0,0],

        [0,0,0, 0,0,4, 0,0,0],
        [0,0,0, 0,0,0, 0,3,0],
        [9,0,3, 0,0,0, 2,0,0],
    ],

    [
        [8,0,0, 0,0,0, 0,0,0],
        [0,0,3, 6,0,0, 0,0,0],
        [0,7,0, 0,9,0, 2,0,0],

        [0,5,0, 0,0,7, 0,0,0],
        [0,0,0, 0,4,5, 7,0,0],
        [0,0,0, 1,0,0, 0,3,0],

        [0,0,1, 0,0,0, 0,6,8],
        [0,0,8, 5,0,0, 0,1,0],
        [0,9,0, 0,0,0, 4,0,0],
    ]
]


class SudokuUI:
    def __init__(self, parent):

        # pick a NEW puzzle every time window opens
        self.start_board = random.choice(PUZZLES)
        self.current = copy.deepcopy(self.start_board)

        self.win = tk.Toplevel(parent)
        self.win.title("Sudoku")
        self.win.geometry("520x560")
        self.win.configure(bg="#e8f5e9")

        tk.Label(self.win, text="Sudoku", font=("Helvetica", 16, "bold"), bg="#e8f5e9").pack(pady=8)

        self.grid_frame = tk.Frame(self.win, bg="#e8f5e9")
        self.grid_frame.pack()

        self.cells = [[None] * 9 for _ in range(9)]
        self.draw_grid()

        btn_frame = tk.Frame(self.win, bg="#e8f5e9")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Check", command=self.check, bg="#4caf50", fg="white").grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Solve", command=self.solve_and_fill, bg="#0288d1", fg="white").grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Reset", command=self.reset, bg="#ff9800", fg="white").grid(row=0, column=2, padx=6)
        tk.Button(btn_frame, text="Close", command=self.win.destroy, bg="#ff5252", fg="white").grid(row=0, column=3, padx=6)

    # ---------------------------
    # Draw grid with puzzle
    # ---------------------------
    def draw_grid(self):
        for r in range(9):
            for c in range(9):
                val = self.start_board[r][c]
                e = tk.Entry(self.grid_frame, width=2, font=("Helvetica", 18), justify="center")

                if val != 0:
                    e.insert(0, str(val))
                    e.config(state="disabled", disabledforeground="black")

                e.grid(row=r, column=c, padx=4, pady=4)
                self.cells[r][c] = e

    # ----------------------------
    # Read board
    # ----------------------------
    def read_board(self):
        board = [[0] * 9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                value = self.cells[r][c].get().strip()
                board[r][c] = int(value) if value.isdigit() and 1 <= int(value) <= 9 else 0
        return board

    # -----------------------------
    # Check for duplicates
    # -----------------------------
    def check(self):
        board = self.read_board()

        # rows
        for i in range(9):
            vals = [x for x in board[i] if x != 0]
            if len(vals) != len(set(vals)):
                messagebox.showerror("Error", f"Duplicate in row {i + 1}")
                return

        # columns
        for j in range(9):
            col = [board[i][j] for i in range(9) if board[i][j] != 0]
            if len(col) != len(set(col)):
                messagebox.showerror("Error", f"Duplicate in column {j + 1}")
                return

        # 3×3 boxes
        for br in range(3):
            for bc in range(3):
                box = []
                for r in range(br * 3, br * 3 + 3):
                    for c in range(bc * 3, bc * 3 + 3):
                        if board[r][c] != 0:
                            box.append(board[r][c])
                if len(box) != len(set(box)):
                    messagebox.showerror("Error", "Duplicate in a 3×3 box")
                    return

        messagebox.showinfo("OK", "Board looks valid!")

    # -----------------------------
    # Sudoku Solver
    # -----------------------------
    def is_safe(self, board, r, c, val):
        if any(board[r][j] == val for j in range(9)): return False
        if any(board[i][c] == val for i in range(9)): return False

        br, bc = 3*(r//3), 3*(c//3)
        for i in range(br, br+3):
            for j in range(bc, bc+3):
                if board[i][j] == val:
                    return False
        return True

    def solve_board(self, board):
        empty = [(r, c) for r in range(9) for c in range(9) if board[r][c] == 0]

        if not empty:
            return True

        r, c = empty[0]
        for val in range(1, 10):
            if self.is_safe(board, r, c, val):
                board[r][c] = val
                if self.solve_board(board):
                    return True
                board[r][c] = 0

        return False

    def solve_and_fill(self):
        board = self.read_board()
        working = copy.deepcopy(board)

        if self.solve_board(working):
            for r in range(9):
                for c in range(9):
                    self.cells[r][c].config(state="normal")
                    self.cells[r][c].delete(0, "end")
                    self.cells[r][c].insert(0, str(working[r][c]))
        else:
            messagebox.showerror("Error", "No solution found!")

    # -----------------------------
    # RESET → LOAD NEW RANDOM PUZZLE
    # -----------------------------
    def reset(self):
        self.start_board = random.choice(PUZZLES)
        self.current = copy.deepcopy(self.start_board)

        for r in range(9):
            for c in range(9):
                self.cells[r][c].config(state="normal")
                self.cells[r][c].delete(0, "end")

                if self.start_board[r][c] != 0:
                    self.cells[r][c].insert(0, str(self.start_board[r][c]))
                    self.cells[r][c].config(state="disabled", disabledforeground="black")


def launch_ui(parent):
    SudokuUI(parent)
