# アプリ名・説明
APP_NAME = "生成AI英会話アプリ"
APP_DESCRIPTION = "こちらは生成AIによる音声英会話の練習アプリです。何度も繰り返し練習し、英語力をアップさせましょう。"

# 操作説明
OPERATION_GUIDE_TITLE = "**【操作説明】**"
OPERATION_GUIDE_TEXT = """
- モードと再生速度を選択し、「英会話開始」ボタンを押して英会話を始めましょう。
- モードは「日常英会話」「シャドーイング」「ディクテーション」から選べます。
- 発話後、5秒間沈黙することで音声入力が完了します。
- 「一時中断」ボタンを押すことで、英会話を一時中断できます。
- サイドバーから設定を変更した場合は、「開始」ボタンを押してください。
- 同じモードを続ける場合は、画面下部に表示される「〇〇を続ける」ボタンを押してください。
"""
# 設定ラベル
SETTING_TITLE = "### 設定"
SPEED_SELECT_LABEL = "再生速度"
MODE_SELECT_LABEL = "モード"
ENGLV_SELECT_LABEL = "英語レベル"

# モード名
MODE_1 = "日常英会話"
MODE_2 = "シャドーイング"
MODE_3 = "ディクテーション"

# ボタンラベル
START_BUTTON_LABEL = "開始"
PAUSE_BUTTON_LABEL = "一時中断"
SHADOWING_CONTINUE_BUTTON_LABEL = "シャドーイングを続ける"
DICTATION_CONTINUE_BUTTON_LABEL = "ディクテーションを続ける"
BASIC_CONTINUE_BUTTON_LABEL = "日常英会話を続ける"

# チャット・入力関連
DICTATION_INFO = "AIが読み上げた音声を、画面下部のチャット欄からそのまま入力・送信してください。"
DICTATION_CHAT_INPUT_LABEL = "※「ディクテーション」選択時以外は送信不可"

# スピナー・インフォ
AUDIO_TRANSCRIBE_SPINNER = "音声入力をテキストに変換中..."
ANSWER_AUDIO_SPINNER = "回答の音声読み上げ準備中..."
PROBLEM_GEN_SPINNER = "問題文生成中..."
EVALUATION_GEN_SPINNER = "評価結果の生成中..."
RECORDING_INFO = "録音中...（5秒間無音で自動終了）"
PAUSE_INFO = "一時中断しました。再開する場合は「開始」ボタンを押してください。"

# アイコンパス
USER_ICON_PATH = "images/user_icon.jpg"
AI_ICON_PATH = "images/ai_icon.jpg"

# 英語レベル選択肢
ENGLISH_LEVEL_OPTION = ["初級者", "中級者", "上級者"]


# 音声ファイル保存先
AUDIO_INPUT_DIR = "audio_input"
AUDIO_OUTPUT_DIR = "audio_output"

# 再生速度選択肢
PLAY_SPEED_OPTION = [2.0, 1.5, 1.2, 1.0, 0.8, 0.6]

# 英語レベル選択肢
ENGLISH_LEVEL_OPTION = ["初級者", "中級者", "上級者"]

# 英語講師として自由な会話をさせ、文法間違いをさりげなく訂正させるプロンプト
SYSTEM_TEMPLATE_BASIC_CONVERSATION_FOR_BEGINNER = """
You are an English conversation teacher. The user is a beginner in English.
Please converse slowly using simple words and short sentences.
If there are any grammatical mistakes, please correct them gently and clearly.
At the end of the conversation, please add explanations or advice in simple Japanese.
"""
SYSTEM_TEMPLATE_BASIC_CONVERSATION_FOR_INTERMEDIATE = """
You are an English conversation teacher. The user is an intermediate English learner.
Converse using everyday expressions, incorporating slightly more complex grammar and vocabulary.
If there are grammar mistakes, correct them naturally within the flow of conversation, adding simple explanations in English when necessary.
"""
SYSTEM_TEMPLATE_BASIC_CONVERSATION_FOR_ADVANCED = """
You are an English conversation teacher. The user is an advanced English speaker.
Converse freely, incorporating natural English expressions and topics including business and social matters.
If there are grammar or vocabulary mistakes, correct them casually without disrupting the flow of conversation, and provide detailed explanations or nuances in English.
At the end of the conversation, offer advice in English on more advanced expressions or areas for improvement.
"""


# 初級向けの5語以内の英文生成を指示するプロンプト
SYSTEM_TEMPLATE_FOR_BEGINNER = """
Generate exactly 1 English sentence that reflects natural English used in daily conversations, workplace, and social settings.

Requirements:
- The sentence must contain **no more than 5 words**.
- Use **only simple and common words** that beginner English learners can easily understand.
- Ensure it is grammatically correct and natural.
- Keep the tone casual, polite, or friendly depending on the situation.

Output format:
- Only the English sentence (max 5 words).
- Do not include explanations, translations, or extra text.
"""

# 中級向けの10語以内の英文生成を指示するプロンプト
SYSTEM_TEMPLATE_FOR_INTERMEDIATE = """
Generate exactly 1 English sentence that reflects natural English used in daily conversations, workplace, and social settings.

Requirements:
- The sentence must contain **no more than 10 words**.
- Use **intermediate-level vocabulary (CEFR B1)** that English learners can understand.
- Ensure the sentence is grammatically correct, natural, and contextually meaningful.
- Style may be casual, polite, or friendly depending on the situation.

Output format:
- Only the English sentence (maximum 10 words).
- Do not include explanations, translations, or extra text.
"""

# 上級向けの20語以内の英文生成を指示するプロンプト
SYSTEM_TEMPLATE_FOR_ADVANCED = """
Generate exactly 1 English sentence that reflects natural English used in daily conversations, workplace, and social settings.

Requirements:
- The sentence must contain **no more than 20 words**.
- Use **advanced-level vocabulary (CEFR B2–C1)** suitable for professional, academic, or nuanced contexts.
- Ensure the sentence is grammatically correct, natural, and contextually meaningful.
- Style may include polite business language, subtle emotions, or culturally nuanced expressions.

Output format:
- Only the English sentence (maximum 20 words).
- Do not include explanations, translations, or extra text.
"""

# 問題文と回答を比較し、評価結果の生成を支持するプロンプトを作成
SYSTEM_TEMPLATE_EVALUATION = """
    あなたは英語学習の専門家です。
    以下の「LLMによる問題文」と「ユーザーによる回答文」を比較し、分析してください：

    【LLMによる問題文】
    問題文：{llm_text}

    【ユーザーによる回答文】
    回答文：{user_text}

    【分析項目】
    1. 単語の正確性（誤った単語、抜け落ちた単語、追加された単語）
    2. 文法的な正確性
    3. 文の完成度

    フィードバックは以下のフォーマットで日本語で提供してください：

    【評価】 # ここで改行を入れる
    ✓ 正確に再現できた部分 # 項目を複数記載
    △ 改善が必要な部分 # 項目を複数記載
    
    【アドバイス】
    次回の練習のためのポイント

    ユーザーの努力を認め、前向きな姿勢で次の練習に取り組めるような励ましのコメントを含めてください。
"""