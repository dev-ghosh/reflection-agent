import os

import streamlit as st
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# API key setup MUST happen before importing agent/chains below, because
# chains.py builds the ChatGroq client as soon as it's imported. If the key
# isn't in the environment yet at that point, it fails with GroqError
# regardless of when load_dotenv is called later in the file.
# Works both locally (.env.ref) and on Streamlit Community Cloud (st.secrets).
# ---------------------------------------------------------------------------
load_dotenv(".env.ref", override=True)
try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

from langchain_core.messages import HumanMessage

from agent import build_graph

st.set_page_config(
    page_title="TweetForge AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #0f1117 0%, #14161f 100%);
        }
        .hero-title {
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, #1DA1F2, #7C3AED);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0rem;
        }
        .hero-sub {
            color: #9CA3AF;
            font-size: 1.05rem;
            margin-top: 0.2rem;
            margin-bottom: 1.5rem;
        }
        .final-card {
            background: #1a1d29;
            border: 1px solid #2d3142;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin-top: 0.5rem;
        }
        div.stButton > button {
            background: linear-gradient(90deg, #1DA1F2, #7C3AED);
            color: white;
            font-weight: 700;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1rem;
        }
        div.stButton > button:hover {
            opacity: 0.9;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("<div class='hero-title'>⚡ TweetForge AI</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-sub'>Feed it a rough tweet. It argues with itself until it's viral-ready.</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    rounds = st.slider("Reflection rounds", min_value=1, max_value=5, value=3)
    st.caption("More rounds = more critique cycles before the final draft.")

    st.markdown("---")
    st.markdown("### 🧠 How it works")
    st.markdown(
        "1. **Generate** — drafts a tweet\n"
        "2. **Reflect** — a critic persona reviews it for hooks, length, and virality\n"
        "3. Repeat until the rounds run out, then keep the last draft"
    )

    st.markdown("---")
    st.caption("Built with LangGraph + Groq (Llama 3.1 8B Instant)")

# ---------------------------------------------------------------------------
# Main input
# ---------------------------------------------------------------------------
tweet_draft = st.text_area(
    "Your draft tweet",
    height=150,
    placeholder="e.g. Just shipped a new feature for our app, check it out!",
)

run = st.button("🚀 Make it Viral", use_container_width=True)

if run:
    if not tweet_draft.strip():
        st.warning("Drop a draft in the box first — even a rough one works.")
    else:
        graph = build_graph(max_messages=rounds * 2 + 2)
        inputs = {
            "messages": [
                HumanMessage(content=f"Make this tweet better:\n{tweet_draft}")
            ]
        }

        final_tweet = tweet_draft
        iteration = 0

        with st.status("🔮 Reflecting on your tweet...", expanded=True) as status:
            for step in graph.stream(inputs):
                for node_name, node_output in step.items():
                    msg = node_output["messages"][-1]
                    if node_name == "generate":
                        iteration += 1
                        st.markdown(f"**✍️ Draft {iteration}**")
                        st.info(msg.content)
                        final_tweet = msg.content
                    else:
                        st.markdown(f"**🔍 Critique {iteration}**")
                        st.warning(msg.content)
            status.update(label="✅ Done reflecting!", state="complete")

        st.markdown("## 🎯 Final Tweet")
        st.markdown(f"<div class='final-card'>{final_tweet}</div>", unsafe_allow_html=True)
        st.code(final_tweet, language=None)
        st.caption(f"{len(final_tweet)}/280 characters")