import random

### LLM ###
from langchain.chat_models import AzureChatOpenAI
from openai.error import RateLimitError
from langchain.schema import HumanMessage

### Logger ###
import logging.config
logging.config.fileConfig('logging_config_chess.ini')
logger = logging.getLogger('CsLogger')

### Config ###
import configparser
config = configparser.ConfigParser()
config.read('CSconfig_chess.ini')

### Call OpenAI LLM Model ###
# 後續可更換成 LLama2 模型並針對五子棋相關知識進行 FineTune
def do_openai(messages):
    AzureOpenAIconfig = config['Open AI Default']['open_ai_section_name']
    openAI = AzureChatOpenAI(
        openai_api_base=config[AzureOpenAIconfig]['OPENAI_API_BASE'],
        openai_api_version=config[AzureOpenAIconfig]['OPENAI_API_VERSION'],
        deployment_name=config[AzureOpenAIconfig]['COMPLETIONS_MODEL'],
        openai_api_key=config[AzureOpenAIconfig]['OPENAI_AZURE_API_KEY'],
        openai_api_type=config[AzureOpenAIconfig]['OPENAI_API_TYPE'],
        temperature=0.3,
        max_tokens=4096
    )
    try:
        res = openAI(messages)
        return res.content
    except RateLimitError:
        print("get rate limit, run again")
        return do_openai(messages)
    except Exception as e:
        print(f"get error: {e}")
        logger.error("詢問GPT發生了一個例外情況", exc_info=True)
        return "系統發生錯誤，請通知系統管理員!"

### Check Winner ###
def check_winner(board, BOARD_SIZE):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - 4):
            if (board[row][col] != " " and
                board[row][col] == board[row][col + 1] and
                board[row][col] == board[row][col + 2] and
                board[row][col] == board[row][col + 3] and
                    board[row][col] == board[row][col + 4]):
                return board[row][col]
    for row in range(BOARD_SIZE - 4):
        for col in range(BOARD_SIZE):
            if (board[row][col] != " " and
                board[row][col] == board[row + 1][col] and
                board[row][col] == board[row + 2][col] and
                board[row][col] == board[row + 3][col] and
                    board[row][col] == board[row + 4][col]):
                return board[row][col]
    for row in range(BOARD_SIZE - 4):
        for col in range(BOARD_SIZE - 4):
            if (board[row][col] != " " and
                board[row][col] == board[row + 1][col + 1] and
                board[row][col] == board[row + 2][col + 2] and
                board[row][col] == board[row + 3][col + 3] and
                    board[row][col] == board[row + 4][col + 4]):
                return board[row][col]
    for row in range(BOARD_SIZE - 4):
        for col in range(4, BOARD_SIZE):
            if (board[row][col] != " " and
                board[row][col] == board[row + 1][col - 1] and
                board[row][col] == board[row + 2][col - 2] and
                board[row][col] == board[row + 3][col - 3] and
                    board[row][col] == board[row + 4][col - 4]):
                return board[row][col]
    return None

### 在棋盤上下一子 ###
def play_chess(board, board_size, mark, round_num):
    # 第一步
    if round_num == 0:
        board[board_size // 2][board_size // 2] = mark
        return board, board_size // 2, board_size // 2
    # 第二步
    elif round_num == 1:
        while True:
            row = random.randint(board_size // 2 - 1, board_size // 2 + 1)
            col = random.randint(board_size // 2 - 1, board_size // 2 + 1)
            if (row >= 0 and row < board_size and col >= 0 and col < board_size and board[row][col] == " "):
                break
    # 從第三步開始，之後的每一步都讓 GPT-3.5 來下
    else:
        while True:
            board_str = print_board(board, board_size)
            prompt = f"""你是一位五子棋大師，請根據當前棋局及你的角色，下出最優的一步解 (以連成5個{mark}為一直線為追求)(只需要給我一步即可，無論任何情況，就是給我一個答案)
*請嚴格且萬分的注意: 請下在空的位置上，在你選擇位置時請再三檢查，不可以下在有子的位置(無論該位置是O或X)*
[當前棋局]:
{board_str}
[你的角色]:
{mark}

輸出格式 *請嚴格按照輸出格式輸出，只能輸出這些，不要輸出其他文字*:
  行a, 列b

請指示下一步的行和列:
"""
            res = do_openai([HumanMessage(content=prompt)])
            try:
                cut_li = res.split(",")
                row = cut_li[0].replace(" ", "").replace("行", "")
                col = cut_li[-1].replace(" ", "").replace("列", "")
                row = int(row)
                col = int(col)
            except Exception as e:
                logger.error("切分GPT回復發生了一個例外情況", exc_info=True)
                row = -1
                col = -1
            
            if (row >= 0 and row < board_size and col >= 0 and col < board_size and board[row][col] == " "):
                break
    
    board[row][col] = mark
    return board, row, col

### 輸出當前棋盤 ###
def print_board(board, BOARD_SIZE):
    outp = "-" * (2 * BOARD_SIZE + 1) + "\n"
    for row in range(BOARD_SIZE):
        outp += "|"
        for col in range(BOARD_SIZE):
            outp += board[row][col]
            outp += "|"
        outp += "\n"
    outp += "-" * (2 * BOARD_SIZE + 1) + "\n"

    return outp
