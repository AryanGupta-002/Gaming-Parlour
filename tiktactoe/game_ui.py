import tkinter as tk
from tkinter import messagebox

def launch_ui(parent):
    win = tk.Toplevel(parent)
    win.title("Tic Tac Toe")
    win.geometry("320x360")
    win.configure(bg="#e1f5fe")

    header = tk.Label(win, text="Tic Tac Toe", font=("Helvetica", 16, "bold"), bg="#e1f5fe")
    header.pack(pady=8)

    frame = tk.Frame(win, bg="#e1f5fe")
    frame.pack()

    buttons = []
    turn = ["X"]

    def check_winner():
        b = [btn["text"] for btn in buttons]
        win_patterns = [(0,1,2),(3,4,5),(6,7,8),
                        (0,3,6),(1,4,7),(2,5,8),
                        (0,4,8),(2,4,6)]
        for x,y,z in win_patterns:
            if b[x] == b[y] == b[z] != "":
                return b[x]
        return None

    def on_click(i):
        if buttons[i]["text"] == "":
            buttons[i]["text"] = turn[0]
            winner = check_winner()
            if winner:
                messagebox.showinfo("Winner", f"Player {winner} wins!")
                reset_board()
                return
            if all(cell["text"] != "" for cell in buttons):
                messagebox.showinfo("Draw", "It's a draw!")
                reset_board()
                return
            turn[0] = "O" if turn[0] == "X" else "X"

    for i in range(9):
        btn = tk.Button(frame, text="", width=6, height=3, font=("Helvetica", 16, "bold"),
                        bg="#4fc3f7", command=lambda i=i: on_click(i))
        btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        buttons.append(btn)

    def reset_board():
        for b in buttons:
            b["text"] = ""
        turn[0] = "X"

    tk.Button(win, text="Reset", command=reset_board, bg="#0288d1", fg="white").pack(pady=10)
    tk.Button(win, text="Close", command=win.destroy, bg="#ff5252", fg="white").pack()
