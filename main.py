import customtkinter as tk
from PIL import ImageTk, Image
import os
import sys

tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")
tk.deactivate_automatic_dpi_awareness()


def resource_path(relative_path: str):
    """Function to find the Path of the given file in Relative Path.

    Args:
        relative_path (str): The Relative Path of the file.

    Returns:
        str: The Actual Path of the file.
    """

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MessageBox:
    def __init__(self, parent: tk.CTk, title, message):
        self.parent = parent
        self.title = title
        self.message = message
        self.dialog = None

        self.create_dialog()

    def create_dialog(self):
        self.dialog = tk.CTkToplevel(self.parent)
        self.dialog.title(self.title)

        x = self.parent.winfo_x() + 7
        y = self.parent.winfo_y() + 120
        self.dialog.geometry("300x120+{}+{}".format(x, y))
        self.dialog.grab_set()
        self.dialog.wm_attributes('-toolwindow', 1)

        frame = tk.CTkFrame(self.dialog, fg_color="grey14", corner_radius=10)

        label = tk.CTkLabel(frame, text=self.message, font=("Garamond", 14))
        label.pack(padx=20, pady=20)

        ok_button = tk.CTkButton(frame, text="OK", command=self.close_dialog)
        ok_button.pack(pady=10)

        frame.pack(fill="both", expand=True)
        self.parent.wait_window(self.dialog)

    def close_dialog(self):
        self.dialog.destroy()


class TicTacToeGUI:
    def __init__(self, root: tk.CTk):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        self.root.geometry("312x337")
        self.icon = ImageTk.PhotoImage(
            Image.open(resource_path("assets/icon.png"))
        )
        self.game_mode = None
        self.frames = []
        self.root.after(200, self.set_icon)

        backButton = tk.CTkButton(
            self.root,
            text="⬅️",
            command=self.back,
            height=20,
            width=50,
        )
        backButton.place(x=2, y=2.5)

        self.first_frame = tk.CTkFrame(
            self.root,
            height=312,
            width=337
        )
        self.second_frame = tk.CTkFrame(
            self.root,
            height=312,
            width=337
        )
        self.third_frame = tk.CTkFrame(
            self.root,
            height=312,
            width=337
        )
        self.first_frame.place(y=25)
        self.current = self.first_frame

        self.create = tk.CTkButton(
            self.first_frame,
            text="➕ New Game",
            command=self.new_game
        )

        self.join = tk.CTkButton(
            self.first_frame,
            text="✖️ Join Game",
            command=self.join_game
        )

        self.create.place(x=80, y=100)
        self.join.place(x=80, y=160)

    def set_icon(self):
        self.root.iconphoto(False, self.icon)

    def back(self):
        if self.frames:
            self.current.place_forget()
            prev = self.frames.pop()
            prev.place(y=25)
            self.current = prev

    def new_game(self):
        self.first_frame.place_forget()
        self.second_frame.place(y=25)
        self.current = self.second_frame
        self.frames.append(self.first_frame)

        self.locally = tk.CTkButton(
            self.second_frame,
            text="💻 Play Locally",
            command=self.vs_player
        )

        self.computer = tk.CTkButton(
            self.second_frame,
            text="🤖 Play vs Computer",
            command=self.vs_computer
        )

        self.room = tk.CTkButton(
            self.second_frame,
            text="📤 Create Room",
            command=self.multi
        )

        self.locally.place(x=80, y=80)
        self.computer.place(x=80, y=130)
        self.room.place(x=80, y=180)

    def vs_player(self):
        self.game_mode = "player"
        self.create_board()

    def vs_computer(self):
        self.game_mode = "computer"
        self.create_board()

    def multi(self):
        MessageBox(
            self.root,
            "Coming Soon!",
            "This feature is not yet ready."
        )

    def join_game(self):
        self.multi()

    def create_board(self):
        self.second_frame.place_forget()
        self.third_frame.place(y=25)
        self.current = self.third_frame
        self.frames.append(self.second_frame)

        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.buttons = [[tk.CTkButton for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.CTkButton(
                    self.third_frame, text="",
                    font=("Helvetica", 40),
                    height=100,
                    width=100,
                    # corner_radius=2,
                    command=lambda i=i, j=j: self.make_move(i, j),
                    fg_color=("#e4e5f1", "#2C2F33"),
                    hover_color=("#d2d3db", "#23272A"),
                )

                self.buttons[i][j].grid(
                    row=i, column=j, padx=2, pady=2, sticky="nsew"
                )

    def make_move(self, row: int, col: int):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            text_color = (("gray14", "#FFFFFF")
                          if self.current_player == "X" else ("red", "red"))
            self.buttons[row][col].configure(
                text=self.current_player, text_color=text_color
            )

            if self.is_winner():
                MessageBox(
                    self.root, "Winner!", f"Player {self.current_player} wins!"
                )
                self.reset_board()

            elif self.is_draw():
                MessageBox(self.root, "Draw!", "It's a draw!")
                self.reset_board()

            else:
                self.current_player = ("O"
                                       if self.current_player == "X" else "X")
                if self.game_mode == "computer" and self.current_player == "O":
                    self.computer_move()

    def reset_board(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text="")

    def is_winner(self, player=None):
        if not player:
            player = self.current_player
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def get_empty_cells(self):
        return [
            (i, j)
            for i in range(3)
            for j in range(3)
            if self.board[i][j] == ""
        ]

    def computer_move(self):
        move = self.get_best_move()
        self.make_move(move[0], move[1])
        pass

    def minimax(self, depth, is_maximizing):
        if self.is_winner('X'):
            return -1
        if self.is_winner('O'):
            return 1
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i, j in self.get_empty_cells():
                self.board[i][j] = 'O'
                score = self.minimax(depth + 1, False)
                self.board[i][j] = ""
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i, j in self.get_empty_cells():
                self.board[i][j] = 'X'
                score = self.minimax(depth + 1, True)
                self.board[i][j] = ""
                best_score = min(best_score, score)
            return best_score

    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        for i, j in self.get_empty_cells():
            self.board[i][j] = 'O'
            score = self.minimax(0, False)
            self.board[i][j] = ""
            if score > best_score:
                best_score = score
                best_move = (i, j)
        return best_move


if __name__ == "__main__":
    root = tk.CTk()
    app = TicTacToeGUI(root)
    root.mainloop()
