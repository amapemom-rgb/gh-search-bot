#!/usr/bin/env python3
# (c) 2026 amapemom-rgb — https://github.com/amapemom-rgb/gh-search-bot
# Licensed under MIT License
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
providers = {
    "1": {
        "name": "OpenRouter (200+ models, recommended)",
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": "qwen/qwen3.7-max",
        "key_hint": "openrouter.ai -> Keys",
    },
    "2": {
        "name": "OpenAI (ChatGPT)",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o",
        "key_hint": "platform.openai.com/api-keys",
    },
    "3": {
        "name": "Anthropic (Claude)",
        "base_url": "https://api.anthropic.com/v1",
        "default_model": "claude-opus-4-6",
        "key_hint": "console.anthropic.com/settings/keys",
    },
    "4": {
        "name": "Google (Gemini)",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "default_model": "gemini-2.0-flash",
        "key_hint": "aistudio.google.com/app/apikey",
    },
    "5": {
        "name": "xAI (Grok)",
        "base_url": "https://api.x.ai/v1",
        "default_model": "grok-3",
        "key_hint": "console.x.ai",
    },
    "6": {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
        "key_hint": "platform.deepseek.com/api_keys",
    },
    "7": {
        "name": "Alibaba (Qwen)",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-max",
        "key_hint": "dashscope.aliyun.com",
    },
    "8": {
        "name": "Other (enter URL manually)",
        "base_url": None,
        "default_model": None,
        "key_hint": None,
    },
}

print("\n[2/3] Choose LLM provider:")
for k, v in providers.items():
    print(f"  {k}. {v['name']}")

choice = input("\n> ").strip()
p = providers.get(choice, providers["8"])

if p["base_url"] is None:
    print("Enter provider base URL:")
    base_url = input("> ").strip()
    print("Enter model name:")
    model = input("> ").strip()
else:
    base_url = p["base_url"]
    print(f"\nGet your API key at: {p['key_hint']}")
    print("Paste API Key:")
    model_input = None

api_key = input("> ").strip()

if p["base_url"] is not None:
    print(f"Model name (press Enter for default: {p['default_model']}):")
    model_input = input("> ").strip()
    model = model_input or p["default_model"]

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

print(f"""
Done! .env file created.
Provider: {p['name']}
Model: {model}

Next steps:
  pip install -r requirements.txt
  python bot.py
""")
