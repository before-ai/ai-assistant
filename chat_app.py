"""
AI質問翻訳チャット
やりたいことを言うだけで、AIが最適な答えを返してくれます。
"""

import streamlit as st
import anthropic

# --- ページ設定 ---
st.set_page_config(
    page_title="AIアシスタント",
    page_icon="💬",
    layout="centered"
)

# --- スタイル ---
st.markdown("""
<style>
    .stApp { background-color: #f5f5f5; }
    .main { max-width: 700px; margin: 0 auto; }
    [data-testid="stChatMessage"] { border-radius: 16px; margin-bottom: 8px; }
    .stTextInput input { border-radius: 24px; padding: 12px 20px; }
    h1 { text-align: center; color: #333; font-size: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("💬 AIアシスタント")
st.caption("やりたいことを話しかけてください。そのまま答えます。")

# --- セッション初期化 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "stage" not in st.session_state:
    st.session_state.stage = "start"  # start → questioning → answering

# --- システムプロンプト ---
SYSTEM_PROMPT = """あなたは「AI質問翻訳者」です。
AIに不慣れな人が目的を伝えると、最高の答えを引き出してあげるのがあなたの役割です。

## 動作ルール

### ステージ1：目的ヒアリング（最初のメッセージ）
ユーザーが最初に目的を言ったら、深掘りのための質問を**3つだけ**返す。
- 質問は短く、簡単な日本語で
- 番号付きリストで表示（1. 2. 3.）
- 最後に「この3つを教えてもらえると、もっと的確に答えられます！」と添える

### ステージ2：回答生成（質問への返答後）
ユーザーが3つの質問に答えたら：
1. 「では、最適な答えをお出しします！」と一言添える
2. そのまま具体的・実用的な回答を日本語で出す
3. 最後に「他にも気になることがあれば、何でも聞いてください。」と添える

### 共通ルール
- 専門用語は使わない
- 親しみやすい丁寧語（です・ます調）
- 回答は箇条書きや見出しを使って読みやすく
- 長すぎず、短すぎず（500文字前後を目安）
"""

# --- 過去メッセージ表示 ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# --- 入力欄 ---
user_input = st.chat_input("例：営業資料を早く作りたい、英語メールを書きたい...")

if user_input:
    # ユーザーメッセージ表示
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Claude API呼び出し
    client = anthropic.Anthropic()

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("考えています..."):
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages,
            )
            reply = response.content[0].text
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
