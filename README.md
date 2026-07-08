# ⚡ TweetForge AI

A tweet-writing agent that critiques its own drafts until they're actually good.

You give it a rough tweet idea, and instead of spitting out one generic response, it runs a **generate → reflect → regenerate** loop: one AI persona writes a draft, another persona (a strict viral-growth critic) tears it apart, and the writer revises based on that feedback — repeating for several rounds before handing you the final, polished tweet.

**🔗 Live demo:** [https://tweetforge.streamlit.app](https://tweetforge.streamlit.app)
> ⚠️ The app is hosted on a free tier and may go to sleep when idle. On first visit it can take **10–30 seconds to wake up**, during which you might see a blank/black screen — just wait a moment and it'll load.

---

## 🧠 How it works

This is a **reflection agent** built with LangGraph, a common agentic pattern where an LLM improves its own output through self-critique instead of one-shot generation.

```
        ┌─────────────┐
   ┌───▶│  Generate    │───▶ writes / revises the tweet
   │    └─────────────┘
   │           │
   │           ▼
   │    ┌─────────────┐
   └────│  Reflect     │◀── critiques it (hook, length, virality, tone)
        └─────────────┘
```

- **Generate node** — an LLM persona focused purely on writing the best possible tweet, given either the original prompt or the latest critique
- **Reflect node** — a second LLM persona acting as a viral-growth critic, grading the draft and giving specific, actionable feedback
- The two nodes pass messages back and forth for a configurable number of rounds (adjustable via a slider in the UI), then the last generated draft is returned as the final tweet

This loop is implemented as a stateful graph using **LangGraph**, with each node's messages tracked and appended via LangChain's message state.

---

## 🛠️ Tech Stack

- **[LangGraph](https://github.com/langchain-ai/langgraph)** — orchestrates the generate/reflect state graph
- **[LangChain](https://github.com/langchain-ai/langchain)** — prompt templates and message handling
- **[Groq](https://groq.com/)** (Llama 3.1 8B Instant) — fast LLM inference for both the generator and critic
- **[Streamlit](https://streamlit.io/)** — frontend UI, deployed on Streamlit Community Cloud

---

## 📂 Project Structure

```
ReflecionAgent/
├── app.py             # Streamlit frontend
├── agent.py           # Reusable LangGraph builder (generate/reflect graph)
├── chains.py          # Prompt templates + LLM chain definitions
├── main.py            # CLI script for testing the agent in the terminal
├── requirements.txt   # Python dependencies
└── .gitignore
```

---

## 🚀 Running It Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/dev-ghosh/reflection-agent.git
   cd reflection-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Groq API key**
   Create a `.env.ref` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Get a free key at [console.groq.com](https://console.groq.com/keys).

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

   Or test the agent directly from the terminal:
   ```bash
   python main.py
   ```

---

## ☁️ Deployment

Deployed on **Streamlit Community Cloud**. The `GROQ_API_KEY` is set via Streamlit's Secrets manager rather than a local `.env` file — `app.py` automatically checks `st.secrets` when running in the cloud, so no code changes are needed between local and deployed environments.

---

## 💡 Possible Improvements

- Let users pick between different critic "personas" (e.g. professional vs. meme-y tone)
- Support threads instead of single tweets
- Swap in different LLM providers/models for comparison
- Persist past sessions so users can revisit earlier drafts

---

Built as a project to explore agentic workflows with LangGraph — feedback and suggestions welcome!!