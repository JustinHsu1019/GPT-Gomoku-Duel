### Tkinter 介面 ###
import tkinter as tk

### Controllers ###
from controllers import check_winner, play_chess_for_ai

### UI 設定 ###
BOARD_SIZE = 19
FIRST_PLAYER_CHAR = "\u26AB"
SECOND_PLAYER_CHAR = "\u2B55"
round_num = 0
board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def on_cell_click(row, col):
    global board, round_num
    if board[row][col] == " ":
        if round_num % 2 == 0:
            player_char = FIRST_PLAYER_CHAR
            board[row][col] = player_char
            board_buttons[row][col].config(text=player_char, state=tk.DISABLED)
            round_num += 1

            winner = check_winner(board, BOARD_SIZE)
            if winner:
                status_label.config(text=f"Winner is {winner}!")
                disable_all_buttons()
                return

            status_label.config(text="Turn: GPT")
            board, ai_row, ai_col = play_chess_for_ai(board, BOARD_SIZE, SECOND_PLAYER_CHAR)
            board_buttons[ai_row][ai_col].config(text=SECOND_PLAYER_CHAR, state=tk.DISABLED)
            round_num += 1

            winner = check_winner(board, BOARD_SIZE)
            if winner:
                status_label.config(text=f"Winner is {winner}!")
                disable_all_buttons()
                return

            status_label.config(text="Turn: Player")

def disable_all_buttons():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            board_buttons[i][j].config(state=tk.DISABLED)

root = tk.Tk()
root.title("Gomoku GPT")

status_label = tk.Label(root, text="Turn: Player")
status_label.pack(pady=10)

board_frame = tk.Frame(root)
board_frame.pack(pady=10)

board_buttons = []
for i in range(BOARD_SIZE):
    row_buttons = []
    for j in range(BOARD_SIZE):
        btn = tk.Button(board_frame, text="", width=2, height=1, command=lambda i=i, j=j: on_cell_click(i, j))
        btn.grid(row=i, column=j, padx=1, pady=1)
        row_buttons.append(btn)
    board_buttons.append(row_buttons)

root.mainloop()
