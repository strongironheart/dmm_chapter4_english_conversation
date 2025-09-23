import streamlit as st
import os
import time
from pathlib import Path
import wave
import pyaudio
from pydub import AudioSegment
from audiorecorder import audiorecorder
import numpy as np
from scipy.io.wavfile import write
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
import constants as ct

# 英語レベルとモードに応じてsystem_templateを更新
def update_system_template():
    if st.session_state.mode == ct.MODE_1:
        if st.session_state.englv == ct.ENGLISH_LEVEL_OPTION[0]:
            st.session_state.system_template = ct.SYSTEM_TEMPLATE_BASIC_CONVERSATION_FOR_BEGINNER
        elif st.session_state.englv == ct.ENGLISH_LEVEL_OPTION[1]:
            st.session_state.system_template = ct.SYSTEM_TEMPLATE_BASIC_CONVERSATION_FOR_INTERMEDIATE
        elif st.session_state.englv == ct.ENGLISH_LEVEL_OPTION[2]:
            st.session_state.system_template = ct.SYSTEM_TEMPLATE_BASIC_CONVERSATION_FOR_ADVANCED
    else:
        if st.session_state.englv == ct.ENGLISH_LEVEL_OPTION[0]:
            st.session_state.system_template = ct.SYSTEM_TEMPLATE_FOR_BEGINNER
        elif st.session_state.englv == ct.ENGLISH_LEVEL_OPTION[1]:
            st.session_state.system_template = ct.SYSTEM_TEMPLATE_FOR_INTERMEDIATE
        elif st.session_state.englv == ct.ENGLISH_LEVEL_OPTION[2]:
            st.session_state.system_template = ct.SYSTEM_TEMPLATE_FOR_ADVANCED

# モード実行ボタンの表示とフラグ更新
def show_mode_buttons():
    mode = st.session_state.mode

    if mode == ct.MODE_2:  # シャドーイング
        if st.session_state.shadowing_flg:
            st.session_state.shadowing_button_flg = st.button(
                ct.SHADOWING_CONTINUE_BUTTON_LABEL, key="btn_shadowing_continue"
            )

    elif mode == ct.MODE_3:  # ディクテーション
        if st.session_state.dictation_flg:
            st.session_state.dictation_button_flg = st.button(
                ct.DICTATION_CONTINUE_BUTTON_LABEL, key="btn_dictation_continue"
            )

    elif mode == ct.MODE_1:  # 日常英会話
        st.session_state.basic_button_flg = st.button(
            ct.BASIC_CONTINUE_BUTTON_LABEL, key="btn_basic_continue"
        )

# モード変更時の初期化処理
def handle_mode_change():
    if st.session_state.mode != st.session_state.pre_mode:
        st.session_state.start_flg = False
        if st.session_state.mode == ct.MODE_1:
            st.session_state.dictation_flg = False
            st.session_state.shadowing_flg = False
        st.session_state.shadowing_count = 0
        if st.session_state.mode == ct.MODE_2:
            st.session_state.dictation_flg = False
        st.session_state.dictation_count = 0
        if st.session_state.mode == ct.MODE_3:
            st.session_state.shadowing_flg = False
        st.session_state.chat_open_flg = False
    st.session_state.pre_mode = st.session_state.mode

# 初期表示
# col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
# 提出課題用

def show_start_button(col):
    """開始ボタンの表示とフラグ管理"""
    with col:
        if st.session_state.start_flg:
            with st.sidebar:
                st.button(ct.START_BUTTON_LABEL, use_container_width=True, type="primary")
        else:
            with st.sidebar:
                st.session_state.start_flg = st.button(ct.START_BUTTON_LABEL, use_container_width=True, type="primary")

def show_speed_selectbox(col):
    """再生速度の選択ボックス表示"""
    with col:
        with st.sidebar:
            st.session_state.speed = st.selectbox(
                label=ct.SPEED_SELECT_LABEL,
                options=ct.PLAY_SPEED_OPTION,
                index=3,
                label_visibility="collapsed",
            )

def show_mode_selectbox(col):
    """モード選択ボックス表示とモード変更処理"""
    with col:
        with st.sidebar:
            st.session_state.mode = st.selectbox(
                label=ct.MODE_SELECT_LABEL,
                options=[ct.MODE_1, ct.MODE_2, ct.MODE_3],
                label_visibility="collapsed",
            )

def show_englv_selectbox(col):
    """英語レベル選択ボックス表示とテンプレート更新"""
    with col:
        with st.sidebar:
            st.session_state.englv = st.selectbox(
                label=ct.ENGLV_SELECT_LABEL,
                options=ct.ENGLISH_LEVEL_OPTION,
                label_visibility="collapsed",
            )

def record_audio(audio_input_file_path):
    """
    音声入力を受け取って音声ファイルを作成
    5秒間無音が続いたら自動で録音終了
    """

    import pyaudio
    import numpy as np
    import wave
    import time
    import streamlit as st

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    SILENCE_THRESHOLD = 500  # 無音判定の閾値（調整可）
    SILENCE_DURATION = 5     # 無音が続く秒数

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    silence_start = None

    st.info(ct.RECORDING_INFO)

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.int16)
        if np.abs(audio_data).mean() < SILENCE_THRESHOLD:
            if silence_start is None:
                silence_start = time.time()
            elif time.time() - silence_start > SILENCE_DURATION:
                break
        else:
            silence_start = None

    stream.stop_stream()
    stream.close()
    p.terminate()

    # ディレクトリがなければ作成
    input_dir = os.path.dirname(audio_input_file_path)
    os.makedirs(input_dir, exist_ok=True)
    wf = wave.open(audio_input_file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(audio_input_file_path):
    """
    音声入力ファイルから文字起こしテキストを取得
    Args:
        audio_input_file_path: 音声入力ファイルのパス
    """

    with open(audio_input_file_path, 'rb') as audio_input_file:
        transcript = st.session_state.openai_obj.audio.transcriptions.create(
            model="whisper-1",
            file=audio_input_file,
            language="en"
        )
    
    # 音声入力ファイルを削除
    os.remove(audio_input_file_path)

    return transcript

def save_to_wav(llm_response_audio, audio_output_file_path):
    """
    一旦mp3形式で音声ファイル作成後、wav形式に変換
    Args:
        llm_response_audio: LLMからの回答の音声データ
        audio_output_file_path: 出力先のファイルパス
    """

    # ディレクトリがなければ作成
    output_dir = os.path.dirname(audio_output_file_path)
    os.makedirs(output_dir, exist_ok=True)
    temp_audio_output_filename = f"{ct.AUDIO_OUTPUT_DIR}/temp_audio_output_{int(time.time())}.mp3"
    temp_output_dir = os.path.dirname(temp_audio_output_filename)
    os.makedirs(temp_output_dir, exist_ok=True)
    with open(temp_audio_output_filename, "wb") as temp_audio_output_file:
        temp_audio_output_file.write(llm_response_audio)
    
    audio_mp3 = AudioSegment.from_file(temp_audio_output_filename, format="mp3")
    audio_mp3.export(audio_output_file_path, format="wav")

    # 音声出力用に一時的に作ったmp3ファイルを削除
    os.remove(temp_audio_output_filename)

def play_wav(audio_output_file_path, speed=1.0):
    """
    音声ファイルの読み上げ
    Args:
        audio_output_file_path: 音声ファイルのパス
        speed: 再生速度（1.0が通常速度、0.5で半分の速さ、2.0で倍速など）
    """

    # 音声ファイルの読み込み
    audio = AudioSegment.from_wav(audio_output_file_path)
    
    # 速度を変更
    if speed != 1.0:
        # frame_rateを変更することで速度を調整
        modified_audio = audio._spawn(
            audio.raw_data, 
            overrides={"frame_rate": int(audio.frame_rate * speed)}
        )
        # 元のframe_rateに戻すことで正常再生させる（ピッチを保持したまま速度だけ変更）
        modified_audio = modified_audio.set_frame_rate(audio.frame_rate)

        modified_audio.export(audio_output_file_path, format="wav")

    # PyAudioで再生
    with wave.open(audio_output_file_path, 'rb') as play_target_file:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(play_target_file.getsampwidth()),
            channels=play_target_file.getnchannels(),
            rate=play_target_file.getframerate(),
            output=True
        )

        data = play_target_file.readframes(1024)
        while data:
            stream.write(data)
            data = play_target_file.readframes(1024)

        stream.stop_stream()
        stream.close()
        p.terminate()
    
    # LLMからの回答の音声ファイルを削除
    os.remove(audio_output_file_path)

def create_chain(system_template):
    """
    LLMによる回答生成用のChain作成
    """

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_template),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    chain = ConversationChain(
        llm=st.session_state.llm,
        memory=st.session_state.memory,
        prompt=prompt
    )

    return chain

def create_problem_and_play_audio():
    """
    問題生成と音声ファイルの再生
    Args:
        chain: 問題文生成用のChain
        speed: 再生速度（1.0が通常速度、0.5で半分の速さ、2.0で倍速など）
        openai_obj: OpenAIのオブジェクト
    """

    # 問題文を生成するChainを実行し、問題文を取得
    problem = st.session_state.chain_create_problem.predict(input="")

    # LLMからの回答を音声データに変換
    llm_response_audio = st.session_state.openai_obj.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=problem
    )

    # 音声ファイルの作成
    audio_output_file_path = f"{ct.AUDIO_OUTPUT_DIR}/audio_output_{int(time.time())}.wav"
    save_to_wav(llm_response_audio.content, audio_output_file_path)

    # 音声ファイルの読み上げ
    play_wav(audio_output_file_path, st.session_state.speed)

    return problem, llm_response_audio

def create_evaluation():
    """
    ユーザー入力値の評価生成
    """

    llm_response_evaluation = st.session_state.chain_evaluation.predict(input="")

    return llm_response_evaluation

# 「一時中断」ボタン表示と押下時の処理
def show_pause_button_and_handle():
    """
    一時中断ボタンの表示と中断処理
    """
    import streamlit as st

    pause_col = st.columns([1])[0]
    with pause_col:
        st.session_state.pause_flg = st.button(ct.PAUSE_BUTTON_LABEL, use_container_width=True, type="secondary", key="pause_btn")

    if st.session_state.pause_flg:
        st.session_state.start_flg = False
        st.session_state.dictation_flg = False
        st.session_state.shadowing_flg = False
        st.session_state.shadowing_button_flg = False
        st.session_state.dictation_button_flg = False
        st.session_state.basic_button_flg = False
        st.session_state.chat_open_flg = False
        st.info(ct.PAUSE_INFO)
        st.stop()