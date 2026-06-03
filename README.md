# GH-найди — Telegram bot for finding open-source tools

AI agent that helps find the right open-source project on GitHub and HuggingFace through a natural language conversation.

## What it does

- Searches GitHub repositories by task description (not exact name)
- Filters by language, stars, activity
- Searches AI models and datasets on HuggingFace
- Asks clarifying questions to narrow the search
- Remembers conversation context (SQLite, persists across restarts)

## Stack

- Python 3.10+
- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API
- [LangGraph](https://langchain-ai.github.io/langgraph/) — ReAct agent with memory
- [OpenRouter](https://openrouter.ai/) / OpenAI / Anthropic — LLM provider (configurable)
- GitHub API + HuggingFace API — data sources
- SQLite — persistent conversation memory

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/amapemom-rgb/gh-search-bot.git
cd gh-search-bot
```

### 2. Create virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run setup wizard

```bash
python setup.py
```

The wizard will ask for:
- Telegram bot token (get one from [@BotFather](https://t.me/BotFather))
- LLM provider choice: OpenRouter, OpenAI, Anthropic, or custom
- API key for chosen provider
- GitHub Personal Access Token ([github.com/settings/tokens](https://github.com/settings/tokens), scope: `public_repo`)

It will create a `.env` file automatically.

### 5. Run the bot

```bash
python bot.py
```

## Bot commands

| Command | Description |
|---------|-------------|
| `/start` | Start conversation |
| `/reset` | Clear context and start over |

## Architecture

```
bot.py      — Telegram interface (aiogram)
agent.py    — LangGraph ReAct agent + search tools
setup.py    — First-time configuration wizard
SOUL.md     — Agent personality and behavior rules
SKILL.md    — Search instructions and response format
memory.db   — SQLite memory (created automatically)
```

## License

MIT
