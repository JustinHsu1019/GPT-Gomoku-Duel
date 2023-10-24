# GPT-Gomoku-Duel - 智能五子棋對弈程式
## 介紹: 
這是一款五子棋遊戲，特色是讓GPT模型進行對弈。玩家可以與OpenAI模型進行對弈，體驗由深度學習驅動的五子棋遊戲。

## 主要功能:
1. 玩家對OpenAI模型對弈: 玩家和OpenAI模型輪流進行五子棋的對弈。
2. 棋盤顯示: 清晰地展示當前的棋盤狀態。
3. 贏家判定: 一旦有玩家連成五子，程式會自動判定該玩家為贏家。

## 如何使用:
1. 安裝所需套件: 執行 `pip install -r requirements.txt` 以安裝所有必要的Python套件。
2. 設定: 確保你已設定CSconfig_chess.ini中的API鑰匙。
3. 啟動遊戲: 執行main.py以開始遊戲。
4. 遊戲進行: 玩家和OpenAI模型輪流下棋，直到有一方連成五子。
5. 遊戲結束: 當有玩家連成五子時，遊戲會自動結束。

## 技術細節:
1. OpenAI模型互動: 利用AzureChatOpenAI與OpenAI模型進行交互，取得模型建議的下一步。
2. 贏家判定: 透過簡單的循環檢查橫、直、斜線連成五子的情況。
3. 棋盤繪製: 使用Tkinter進行棋盤的繪製和更新。

## 提示詞:
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

## 待完善之項目:
1. 多語言支持: 增加其他語言的支援，如英語、日語等。
2. 自訂遊戲設定: 讓玩家可以選擇棋盤大小、遊戲難度等。
3. 保存和加載: 允許玩家在任何時候保存遊戲進度並在稍後加載。
4. 模型升級: 未來我們計劃引入經過五子棋知識微調的LLama-2模型，以進一步提升遊戲體驗。

## 程式導覽:

[![程式導覽](https://img.youtube.com/vi/CNjWbQX38EE/0.jpg)](https://www.youtube.com/embed/CNjWbQX38EE)

## UI 介面:

![GomokuGPT](https://github.com/JustinHsu1019/GPT-Gomoku-Duel/assets/141555665/528eec7e-7ff9-4cb3-b040-58acf5eccb74)

