# 以下を「app.py」に書き込み
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
import os
from audio_recorder_streamlit import audio_recorder
from tempfile import NamedTemporaryFile

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
os.environ["OPENAI_API_KEY"] = st.secrets.OpenAIAPI.openai_api_key

chat = ChatOpenAI(model="gpt-3.5-turbo")

# プロンプトのテンプレート
system_template = (
    "あなたは、{source_lang} を {target_lang}に翻訳する優秀な翻訳アシスタントです。翻訳結果以外は出力しないでください。"
)
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)

if "response" not in st.session_state:
    st.session_state["response"]= ""

# LLMとやりとりする関数
def communicate():
    text = st.session_state["user_input"]
    response = chat(
        chat_prompt.format_prompt(
            source_lang=source_lang, target_lang=target_lang, text=text
        ).to_messages()
    )
    st.session_state["response"] = response.content

# ユーザーインターフェイスの構築
st.title("翻訳アプリ")
st.write("LangChainを使った翻訳アプリです。")

options = ["日本語", "英語", "スペイン語", "ドイツ語", "フランス語", "中国語"]
source_lang = st.selectbox(label="翻訳元", options=options)
target_lang = st.selectbox(label="翻訳先", options=options)
st.text_input("翻訳する文章を入力してください。", key="user_input")
st.button("翻訳", type="primary", on_click=communicate)

if st.session_state["user_input"] != "":
    st.write("翻訳結果:")
    st.write(st.session_state["response"])
