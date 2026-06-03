# GH-найди -- Telegram-bot dlja poiska open-source instrumentov

AI-agent kotoryj pomogaet najti open-source proekt na GitHub i HuggingFace cherez dialog na estestvennom jazyke.

## Chto umeet

- Ishchet repozitorii na GitHub po opisaniju zadachi
- Filtruet po jazyku, zvjozdam, aktivnosti
- Ishchet AI-modeli i datasety na HuggingFace
- Vedjot dialog: zadajoet utochnjajushchie voprosy
- Zapominaet kontekst razgovora (SQLite, sobljudaetsja mezhdu perezapuskami)

## Stek

- Python 3.10+
- aiogram 3 -- Telegram Bot API
- LangGraph -- ReAct-agent s pamjatju
- OpenRouter -- LLM provajder (model: qwen/qwen3.7-max)
- GitHub API + HuggingFace API
- SQLite -- persistentnaja pamjat dialogov

## Ustanovka

### 1. Klonirovat repozitorij

```bash
git clone https://github.com/amapemom-rgb/gh-search-bot.git
cd gh-search-bot
```

### 2. Virtualnoye okruzhenie

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Zavisimosti

```bash
pip install -r requirements.txt
```

### 4. Nastroit .env

```bash
cp .env.example .env
```

Nuzhnyje tokeny:
- `TELEGRAM_TOKEN` -- poluchit u @BotFather
- `OPENROUTER_API_KEY` -- poluchit na openrouter.ai
- `GITHUB_TOKEN` -- poluchit na github.com/settings/tokens (scope: public_repo)

### 5. Zapustit

```bash
python bot.py
```

## Komandy bota

| Komanda | Opisanie |
|---------|----------|
| `/start` | Nachat dialog |
| `/reset` | Sbrosit kontekst |

## Arhitektura

```
bot.py     -- Telegram-interfejs (aiogram)
agent.py   -- LangGraph ReAct-agent + instrumenty poiska
SOUL.md    -- Lichnost i pravila povedenija agenta
SKILL.md   -- Instrukcii po poisku
memory.db  -- SQLite baza pamjati (sozdajotsja avtomaticheski)
```

## Licenzija

MIT
