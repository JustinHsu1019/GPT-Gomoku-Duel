### For LLM ###
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import HumanMessage

### Logger ###
import logging.config
logging.config.fileConfig('logging_config_chess.ini')
logger = logging.getLogger('CsLogger')

### Config ###
import configparser
config = configparser.ConfigParser()
config.read('CSconfig_chess.ini')

### 呼叫 GPT 模型 (本次使用模型為 GPT-3.5-16k) ###
def do_openai(messages):
    """ Azure OpenAI Key """
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
    """ OpenAI Key
    openAI = ChatOpenAI(
        model_name=deployment_name_for_openai,
        openai_api_key=openai_api_key_for_openai,
        temperature=0.3,
        max_tokens=100
    )
    """
    try:
        res = openAI(messages)
        return res.content
    except Exception as e:
        print(f"哭哭，出現錯誤，錯誤內容: {e}")
        logger.error("哭哭，詢問GPT出現錯誤", exc_info=True)
        return do_openai(messages)

### 檢查是否有玩家連成五子 ###
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

### 整理當前棋局狀況 ###
"""
範例輸出:
 行5, 列3: ⚫
 行4, 列4: ⭕
 行4, 列5: ⭕
"""
def print_board(board, BOARD_SIZE):
    output = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != " ":
                output.append(f"行{i}, 列{j}: {board[i][j]}")
    return "\n".join(output)

### 在棋盤上下一子 ###
# Prompt 仍在調整中，若GPT-3.5仍無法實現指令遵從，則進行 FineTune or 更換成 LLama-2 進行 增量預訓練+FineTune
def play_chess_for_ai(board, board_size, mark):
    while True:
        board_str = print_board(board, board_size)
        prompt = f"""五子棋:
遊戲規則：
兩名玩家輪流在棋盤的空白位置上放置自己的棋子。
第一個玩家使用黑子，第二個玩家使用白子（或相反，根據約定）。
目標是在棋盤上形成一條由五個連續的同色棋子所組成的直線，這條線可以是水平、垂直或斜線。
第一個成功連接五個棋子的玩家獲勝。
策略：
五子棋需要玩家進行策略性思考，以預測對方的下一步，同時防止對方連接五子並嘗試自己連接。進階玩家會有各種開局策略和模式，以及識別危險位置並及時封堵的能力。

你是一位五子棋大師，請根據[當前棋局]及[你的角色]，下出最優的一步解
*如果你看到對方已經有三個以上的子連成一線，請立刻阻止他繼續連成四子或五子*
--> 範例：假設對手是O, 棋盤: 行5, 列3: O, 行5, 列4: O, 行5, 列5: O，這時候你就要下在 行5, 列6 或是 行5, 列2 來阻止他
*以連成5個{mark}為一直線為追求*
--> 範例：假設你是O, 行5, 列2: O, 行5, 列3: O, 行5, 列4: O，行5, 列5: O，這時候你就要下在 行5, 列6 或是 行5, 列1 來連成五子以獲得勝利
*只需要給我一步即可，無論任何情況，就是給我一個答案*
--> 範例：行4, 列3
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

            if (row >= 0 and row < board_size and col >= 0 and col < board_size and board[row][col] == " "):
                break
        except:
            logger.error("哭哭，切分GPT回覆發生了錯誤", exc_info=True)
            continue

    board[row][col] = mark
    return board, row, col
