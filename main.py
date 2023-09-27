### Controllers ###
from controllers import check_winner, play_chess, print_board

### Logger ###
import logging.config
logging.config.fileConfig('logging_config_chess.ini')
logger = logging.getLogger('CsLogger')

### Setting ###
BOARD_SIZE = 19
FIRST_PLAYER_CHAR = "X"
SECOND_PLAYER_CHAR = "O"
first_player_last_row = 0
first_player_last_col = 0
second_player_last_row = 0
second_player_last_col = 0
round_num = 0
board = []
for i in range(BOARD_SIZE):
    board.append([])
    for j in range(BOARD_SIZE):
        board[i].append(" ")

### Main ###
def main():
    global board, round_num, first_player_last_row, first_player_last_col, second_player_last_row, second_player_last_col
    logger.info("開始遊戲")
    print(print_board(board, BOARD_SIZE))
    while True:
        logger.info("又一輪")

        if round_num % 2 == 0:
            player_char = FIRST_PLAYER_CHAR
            last_row = first_player_last_row
            last_col = first_player_last_col
        else:
            player_char = SECOND_PLAYER_CHAR
            last_row = second_player_last_row
            last_col = second_player_last_col

        board, last_row, last_col = play_chess(board, BOARD_SIZE, player_char, round_num)

        if player_char == FIRST_PLAYER_CHAR:
            first_player_last_row = last_row
            first_player_last_col = last_col
        else:
            second_player_last_row = last_row
            second_player_last_col = last_col

        round_num += 1

        print(print_board(board, BOARD_SIZE))
        
        if check_winner(board, BOARD_SIZE) != None:
            break
        
    logger.info("遊戲結束")
    print(f"Player {check_winner(board, BOARD_SIZE)} is the winner!")

if __name__ == '__main__':
    main()
