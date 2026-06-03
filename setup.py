#!/usr/bin/env python3
"""
GH-najdi Bot -- Setup Wizard
Run this script once before starting the bot.
"""
import os

print("""
========================================
   GH-najdi Bot -- Setup Wizard
========================================
""")

# Step 1: Telegram
print("[1/3] Create a bot via @BotFather in Telegram and paste the token:")
tg = input("> ").strip()

# Step 2: LLM provider
print("""
[2/3] Choose LLM provider:
  1. OpenRouter (200+ models, recommended)
  2. OpenAI (ChatGPT)
  3. Anthropic (Claude)
  4. Other (enter URL manually)
""")
choice = input("> ").strip()

if choice == "1":
    base_url = "https://openrouter.ai/api/v1"
    print("Paste your OpenRouter API Key (openrouter.ai):")
    api_key = input("> ").strip()
    print("Model name (press Enter for default: qwen/qwen3.7-max):")
    model = input("> ").strip() or "qwen/qwen3.7-max"
elif choice == "2":
    base_url = "https://api.openai.com/v1"
    print("Paste your OpenAI API Key:")
    api_key = input("> ").strip()
    print("Model name (press Enter for default: gpt-4o):")
    model = input("> ").strip() or "gpt-4o"
elif choice == "3":
    base_url = "https://api.anthropic.com/v1"
    print("Paste your Anthropic API Key:")
    api_key = input("> ").strip()
    print("Model name (press Enter for default: claude-opus-4-6):")
    model = input("> ").strip() or "claude-opus-4-6"
else:
    print("Enter provider base URL:")
    base_url = input("> ").strip()
    print("Enter API Key:")
    api_key = input("> ").strip()
    print("Enter model name:")
    model = input("> ").strip()

# Step 3: GitHub token
print("""
[3/3] Paste your GitHub Personal Access Token
(get one at github.com/settings/tokens -- scope: public_repo):""")
gh = input("> ").strip()

# Write .env
env_content = f"""TELEGRAM_TOKEN={tg}
OPENROUTER_API_KEY={api_key}
GITHUB_TOKEN={gh}
LLM_BASE_URL={base_url}
LLM_MODEL={model}
"""
with open(".env", "w") as f:
    f.write(env_content)

print("""
Done! .env file created.

Next steps:
  pip install -r requirements.txt
  python bot.py
""")
