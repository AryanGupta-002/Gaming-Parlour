import tkinter as tk
from tkinter import messagebox
import random

SIZE = 4
TARGET = 2048

class Game2048UI:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("2048")
        self.win.geometry("420x480")
        self.win.configure(bg="#fff3e0")

        self.grid_frame = tk.Frame(self.win, bg="#bbdefb")
        self.grid_frame.pack(pady=10)

        self.cells = [[tk.Label(self.grid_frame, text="", width=6, height=3, font=("Helvetica", 18, "bold"),
                                 relief="ridge", bg="#eee") for _ in range(SIZE)] for _ in range(SIZE)]
        for r in range(SIZE):
            for c in range(SIZE):
                self.cells[r][c].grid(row=r, column=c, padx=5, pady=5)

        self.score = 0
        self.score_label = tk.Label(self.win, text=f"Score: {self.score}", font=("Helvetica", 14, "bold"), bg="#fff3e0")
        self.score_label.pack()

        tk.Button(self.win, text="New Game", command=self.new_game, bg="#ff9800", fg="white").pack(pady=6)
        tk.Button(self.win, text="Close", command=self.win.destroy, bg="#ff5252", fg="white").pack(pady=6)

        self.win.bind('<Key>', self.key_handler)
        self.new_game()

    def new_game(self):
        self.board = [[0]*SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random()
        self.add_random()
        self.update_ui()

    def add_random(self):
        empty = [(r,c) for r in range(SIZE) for c in range(SIZE) if self.board[r][c]==0]
        if not empty:
            return False
        r,c = random.choice(empty)
        self.board[r][c] = 4 if random.random() < 0.1 else 2
        return True

    def update_ui(self):
        for r in range(SIZE):
            for c in range(SIZE):
                v = self.board[r][c]
                self.cells[r][c]["text"] = str(v) if v != 0 else ""
        self.score_label["text"] = f"Score: {self.score}"

    def key_handler(self, event):
        key = event.keysym
        moved = False
        if key in ('Left','a','A'):
            moved = self.move_left()
        elif key in ('Right','d','D'):
            moved = self.move_right()
        elif key in ('Up','w','W'):
            moved = self.move_up()
        elif key in ('Down','s','S'):
            moved = self.move_down()
        if moved:
            self.add_random()
            self.update_ui()
            if any(TARGET in row for row in self.board):
                messagebox.showinfo('2048', 'You reached 2048! You win!')
                self.new_game()
            elif not self.can_move():
                messagebox.showinfo('2048', 'No moves left — Game over!')
                self.new_game()

    # movement helpers
    def compress(self, row):
        new = [v for v in row if v!=0]
        new += [0]*(SIZE-len(new))
        return new

    def merge(self, row):
        new = []
        i = 0
        while i < SIZE:
            if i+1 < SIZE and row[i] == row[i+1] and row[i] != 0:
                new.append(row[i]*2)
                self.score += row[i]*2
                i += 2
            else:
                new.append(row[i])
                i += 1
        new += [0]*(SIZE-len(new))
        return new

    def move_left(self):
        moved = False
        for r in range(SIZE):
            original = list(self.board[r])
            compressed = self.compress(original)
            merged = self.merge(compressed)
            final = self.compress(merged)
            self.board[r] = final
            if final != original:
                moved = True
        return moved

    def reverse(self, row):
        return row[::-1]

    def transpose(self, matrix):
        return [list(row) for row in zip(*matrix)]

    def move_right(self):
        self.board = [self.reverse(row) for row in self.board]
        moved = self.move_left()
        self.board = [self.reverse(row) for row in self.board]
        return moved

    def move_up(self):
        self.board = self.transpose(self.board)
        moved = self.move_left()
        self.board = self.transpose(self.board)
        return moved

    def move_down(self):
        self.board = self.transpose(self.board)
        moved = self.move_right()
        self.board = self.transpose(self.board)
        return moved

    def can_move(self):
        if any(0 in row for row in self.board):
            return True
        for r in range(SIZE):
            for c in range(SIZE-1):
                if self.board[r][c] == self.board[r][c+1]:
                    return True
        for c in range(SIZE):
            for r in range(SIZE-1):
                if self.board[r][c] == self.board[r+1][c]:
                    return True
        return False

def launch_ui(parent):
    Game2048UI(parent)
