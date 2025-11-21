import tkinter as tk
from tkinter import messagebox
import random
import time

class MinesweeperUI:
    def __init__(self, parent, rows=9, cols=9, mines=10):
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.win = tk.Toplevel(parent)
        self.win.title("Minesweeper")
        self.win.geometry("420x520")
        self.win.configure(bg="#f0f4c3")
        self.start_time = None
        self.timer_id = None

        top = tk.Frame(self.win, bg="#f0f4c3")
        top.pack(pady=6)
        self.status_label = tk.Label(top, text=f"Mines: {self.mines}", font=("Helvetica", 12, "bold"), bg="#f0f4c3")
        self.status_label.pack(side="left", padx=8)
        self.time_label = tk.Label(top, text="Time: 0s", font=("Helvetica", 12, "bold"), bg="#f0f4c3")
        self.time_label.pack(side="right", padx=8)

        mid = tk.Frame(self.win, bg="#f0f4c3")
        mid.pack()
        control = tk.Frame(self.win, bg="#f0f4c3")
        control.pack(pady=8)

        tk.Button(control, text="New (Easy)", command=self.new_easy, bg="#4caf50", fg="white").grid(row=0, column=0, padx=4)
        tk.Button(control, text="Medium", command=self.new_medium, bg="#0288d1", fg="white").grid(row=0, column=1, padx=4)
        tk.Button(control, text="Hard", command=self.new_hard, bg="#ff9800", fg="white").grid(row=0, column=2, padx=4)
        tk.Button(control, text="Reset", command=self.reset_game, bg="#9e9e9e", fg="white").grid(row=0, column=3, padx=4)
        tk.Button(control, text="Close", command=self.win.destroy, bg="#ff5252", fg="white").grid(row=0, column=4, padx=4)

        self.board_frame = tk.Frame(self.win, bg="#f0f4c3")
        self.board_frame.pack(pady=8)
        self.setup_board()
        self.place_widgets()
        self.new_game()

    def setup_board(self):
        self.cells = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.cell_buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False]*self.cols for _ in range(self.rows)]
        self.flagged = [[False]*self.cols for _ in range(self.rows)]
        self.mine_map = [[0]*self.cols for _ in range(self.rows)]
        self.first_click = True
        self.remaining = self.rows * self.cols - self.mines

    def place_widgets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                b = tk.Button(self.board_frame, text="", width=3, height=1, font=("Helvetica", 12, "bold"),
                              relief="raised", bg="#e0e0e0")
                b.grid(row=r, column=c, padx=2, pady=2)
                b.bind("<Button-1>", lambda e, rr=r, cc=c: self.on_left(rr,cc))
                b.bind("<Button-3>", lambda e, rr=r, cc=c: self.on_right(rr,cc))
                self.cell_buttons[r][c] = b

    def new_easy(self):
        self.rows, self.cols, self.mines = 9,9,10
        self.recreate_board()

    def new_medium(self):
        self.rows, self.cols, self.mines = 16,16,40
        self.recreate_board()

    def new_hard(self):
        self.rows, self.cols, self.mines = 16,30,99
        self.recreate_board()

    def recreate_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.setup_board()
        self.place_widgets()
        self.new_game()

    def new_game(self):
        self.start_time = None
        if self.timer_id:
            self.win.after_cancel(self.timer_id)
            self.timer_id = None
        self.time_label.config(text="Time: 0s")
        self.status_label.config(text=f"Mines: {self.mines}")
        self.first_click = True
        self.revealed = [[False]*self.cols for _ in range(self.rows)]
        self.flagged = [[False]*self.cols for _ in range(self.rows)]
        self.mine_map = [[0]*self.cols for _ in range(self.rows)]
        self.remaining = self.rows * self.cols - self.mines
        for r in range(self.rows):
            for c in range(self.cols):
                b = self.cell_buttons[r][c]
                b.config(text="", state="normal", relief="raised", bg="#e0e0e0")
        # mines placed on first click (so first click never hits a mine)

    def reset_game(self):
        self.new_game()

    def start_timer(self):
        if self.start_time is None:
            self.start_time = time.time()
            self.update_timer()

    def update_timer(self):
        if self.start_time is None:
            return
        elapsed = int(time.time() - self.start_time)
        self.time_label.config(text=f"Time: {elapsed}s")
        self.timer_id = self.win.after(1000, self.update_timer)

    def plant_mines(self, safe_r, safe_c):
        positions = [(r,c) for r in range(self.rows) for c in range(self.cols) if not (r==safe_r and c==safe_c)]
        random.shuffle(positions)
        for i in range(self.mines):
            r,c = positions[i]
            self.mine_map[r][c] = -1
        # compute neighbor counts
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mine_map[r][c] == -1:
                    continue
                cnt = 0
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nr, nc = r+dr, c+dc
                        if 0<=nr<self.rows and 0<=nc<self.cols and self.mine_map[nr][nc]==-1:
                            cnt += 1
                self.mine_map[r][c] = cnt

    def reveal_cell(self, r, c):
        if self.revealed[r][c] or self.flagged[r][c]:
            return
        b = self.cell_buttons[r][c]
        self.revealed[r][c] = True
        b.config(relief="sunken", state="disabled", bg="#f5f5f5")
        if self.mine_map[r][c] == -1:
            b.config(text="*", bg="#ff8a80")
            self.game_over(False)
            return
        elif self.mine_map[r][c] == 0:
            b.config(text="")
            # flood fill neighbours
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    nr, nc = r+dr, c+dc
                    if 0<=nr<self.rows and 0<=nc<self.cols and not self.revealed[nr][nc]:
                        self.reveal_cell(nr,nc)
        else:
            b.config(text=str(self.mine_map[r][c]), fg=self.get_color(self.mine_map[r][c]))
        self.remaining -= 1
        if self.remaining == 0:
            self.game_over(True)

    def get_color(self, n):
        colors = {1:"blue",2:"green",3:"red",4:"darkblue",5:"brown",6:"turquoise",7:"black",8:"gray"}
        return colors.get(n, "black")

    def on_left(self, r, c):
        if self.first_click:
            self.plant_mines(r,c)
            self.first_click = False
            self.start_timer()
        if self.flagged[r][c]:
            return
        self.reveal_cell(r,c)

    def on_right(self, r, c):
        # toggle flag
        if self.revealed[r][c]:
            return
        self.flagged[r][c] = not self.flagged[r][c]
        b = self.cell_buttons[r][c]
        if self.flagged[r][c]:
            b.config(text="F", fg="red")
        else:
            b.config(text="")

    def reveal_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mine_map[r][c] == -1:
                    b = self.cell_buttons[r][c]
                    b.config(text="*", bg="#ffcdd2")

    def game_over(self, won):
        if self.timer_id:
            self.win.after_cancel(self.timer_id)
            self.timer_id = None
        if won:
            messagebox.showinfo("You Win", "Congratulations — you cleared all mines!")
        else:
            self.reveal_all_mines()
            messagebox.showerror("Game Over", "Boom! You hit a mine.")
        # disable all buttons
        for r in range(self.rows):
            for c in range(self.cols):
                self.cell_buttons[r][c].config(state="disabled")

def launch_ui(parent):
    # default easy 9x9-10 mines; user can switch difficulty inside game
    MinesweeperUI(parent, rows=9, cols=9, mines=10)
