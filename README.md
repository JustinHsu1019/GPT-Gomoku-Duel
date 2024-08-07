# LLM-Gomoku-Duel - Intelligent Gomoku Duel Program
## Introduction: 
This is a Gomoku game, with the unique feature of allowing players to duel against the LLM model. Players can compete against the LLM model and experience a Gomoku game powered by deep learning.

## Areas for Improvement:
1. Prepare for fine-tuning, starting with data preparation, using the original GPT-4o model.
- Dataset: [https://gomocup.org/results](https://gomocup.org/results/)
2. Introduce the LLama-3 model, performing continual pretraining with Gomoku knowledge, followed by fine-tuning and RLHF to enhance the gaming experience.
3. Enhance the LLM's ability to play Gomoku using Retrieval-Augmented Generation (RAG). Ensure that various board configurations are recorded accurately for precise retrieval.
4. Implement custom game settings that allow players to choose the chessboard size, game difficulty, and other preferences.
5. Enable save and load functionality, allowing players to save their game progress at any time and load it later.

## Key Features:
1. Player vs. LLM Model Duel: Players and the LLM model take turns in the Gomoku duel.
2. Chessboard Display: Clearly displays the current state of the chessboard.
3. Winner Determination: Once a player achieves five in a row, the program automatically declares that player as the winner.

## How to Use:
1. Install Required Packages: Run `pip install -r requirements.txt` to install all necessary Python packages.
2. Configuration: Ensure you have set the API key in CSconfig_chess.ini.
3. Start the Game: Execute main.py to begin the game.
4. Gameplay: Players and the LLM model take turns making moves until one side achieves five in a row.
5. Game End: The game automatically ends when a player achieves five in a row.

## Technical Details:
1. Interaction with LLM Model: Uses AzureChatOpenAI to interact with the LLM model, obtaining the model's recommended next move.
2. Winner Determination: Uses simple loops to check for five in a row horizontally, vertically, and diagonally.
3. Chessboard Drawing: Uses Tkinter for chessboard drawing and updates.

## Prompt:
```python
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

請指示下一步的行和列:"""
```

## Program Tour:

[![Program Tour](https://img.youtube.com/vi/CNjWbQX38EE/0.jpg)](https://www.youtube.com/embed/CNjWbQX38EE)

## License
This repository is licensed under the [MIT License](https://github.com/JustinHsu1019/GPT-Gomoku-Duel/blob/main/LICENSE).

