import tkinter as tk
from tkinter import messagebox
import importlib

class GameParlourUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Game Parlour")
        self.root.geometry("420x420")
        self.root.configure(bg="#b3e5fc")

        tk.Label(root, text="Welcome to Game Parlour",
                 font=("Helvetica", 18, "bold"), bg="#b3e5fc").pack(pady=20)

        games = [
            ("Tic Tac Toe", "games.tic_tac_toe.game_ui"),
            ("Sudoku", "games.sudoku.game_ui"),
            ("2048", "games.game2048.game_ui"),
            ("Minesweeper", "games.minesweeper.game_ui"),
        ]

        for name, module_path in games:
            btn = tk.Button(root, text=name, width=20, height=2,
                            bg="#0288d1", fg="white", font=("Helvetica", 12, "bold"),
                            command=lambda m=module_path: self.launch_game(m))
            btn.pack(pady=8)

        tk.Button(root, text="Exit", width=15, height=2, bg="#ff5252", fg="white",
                  font=("Helvetica", 12, "bold"), command=root.quit).pack(pady=12)

    def launch_game(self, module_path):
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, "launch_ui"):
                module.launch_ui(self.root)
            else:
                messagebox.showinfo("Coming Soon", "This game is under development!")
        except ModuleNotFoundError:
            messagebox.showerror("Error", f"Cannot find {module_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameParlourUI(root)
    root.mainloop()
