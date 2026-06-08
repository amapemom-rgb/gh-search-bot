# GH-найди — Telegram bot for finding open-source tools

AI agent that helps find the right open-source project on GitHub and HuggingFace through a natural language conversation.


## What it does

- Searches GitHub repositories by task description (not exact name)
- Filters by language, stars, activity
- Searches AI models and datasets on HuggingFace
- Searches npm packages (Node.js/JavaScript)
- Searches Python packages on PyPI
- Searches awesome-lists for curated tool collections
- **Reads files from repositories** — README, configs, examples (e.g., `glider.conf`, `docker-compose.yml`)
- Asks clarifying questions to narrow the search
- Remembers conversation context (SQLite, persists across restarts)

## Deploy options

### Option A — One click (Railway)

2. Sign in with GitHub
3. Fill in your tokens in the form (Telegram, LLM API key, GitHub)
4. Click Deploy — bot starts in the cloud, no local setup needed

Free tier: $5/month credit (enough for a light bot).

### Option B — Run locally

#### 1. Clone the repository

```bash
git clone https://github.com/amapemom-rgb/gh-search-bot.git
cd gh-search-bot
```

#### 2. Create virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run setup wizard

```bash
python setup.py
```

The wizard will ask for:
- Telegram bot token (get one from [@BotFather](https://t.me/BotFather))
- LLM provider: OpenRouter, OpenAI, Anthropic, Gemini, Grok, DeepSeek, Qwen, or custom
- API key for chosen provider
- GitHub Personal Access Token ([github.com/settings/tokens](https://github.com/settings/tokens), scope: `public_repo`)

#### 5. Run the bot

```bash
python bot.py
```

> Note: when running locally the bot works only while your computer is on and the terminal is open.

## Stack

- Python 3.10+
- [aiogram 3](https://docs.aiogram.dev/) — Telegram Bot API
- [LangGraph](https://langchain-ai.github.io/langgraph/) — ReAct agent with memory
- OpenRouter / OpenAI / Anthropic / Gemini / Grok / DeepSeek / Qwen — LLM provider (configurable)
- GitHub API + HuggingFace API + npm + PyPI — data sources
- SQLite — persistent conversation memory

## Agent tools

| Tool | Description |
|------|-------------|
| `search_github` | Search repositories by query, language, stars |
| `get_repo_details` | Get stars, license, last commit for a specific repo |
| `get_repo_file_content` | Read a file from a repo (README, config, examples) |
| `search_huggingface` | Search AI models and datasets |
| `search_npm` | Search Node.js packages on npm |
| `search_pypi` | Search Python packages on PyPI |
| `search_awesome` | Search awesome-lists on GitHub |

## Bot commands

| Command | Description |
|---------|-------------|
| `/start` | Start conversation |
| `/reset` | Clear context and start over |

## Architecture

```
bot.py        — Telegram interface (aiogram)
agent.py      — LangGraph ReAct agent + search tools
setup.py      — First-time configuration wizard
railway.json  — Railway deployment config
SOUL.md       — Agent personality and behavior rules
SKILL.md      — Search instructions and response format
memory.db     — SQLite memory (created automatically)
```

## License

MIT
