#!/usr/bin/env python3
# (c) 2026 amapemom-rgb -- https://github.com/amapemom-rgb/gh-search-bot
# Licensed under MIT License
"""
GH-najdi Bot -- Setup Wizard
Run this script once before starting the bot.
"""
import os
import sys
import subprocess
import time

print("""
========================================
   GH-najdi Bot -- Setup Wizard
========================================
""")

# Step 1: Telegram
print("[1/4] Create a bot via @BotFather in Telegram and paste the token:")
tg = input("> ").strip()

# Step 2: LLM provider
providers = {
    "1": {
        "name": "OpenRouter (200+ models, recommended)",
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": "qwen/qwen3-30b-a3b:free",
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

print("\n[2/4] Choose LLM provider:")
for k, v in providers.items():
    print(f"  {k}. {v['name']}")

choice = input("\n> ").strip()
p = providers.get(choice, providers["8"])

if p["base_url"] is None:
    print("Enter provider base URL:")
    base_url = input("> ").strip()
    print("Enter model name:")
    model = input("> ").strip()
    print("Paste API Key:")
    api_key = input("> ").strip()
else:
    base_url = p["base_url"]
    print(f"\nGet your API key at: {p['key_hint']}")
    print("Paste API Key:")
    api_key = input("> ").strip()
    print(f"Model name (press Enter for default: {p['default_model']}):")
    model_input = input("> ").strip()
    model = model_input or p["default_model"]

# Step 3: GitHub token
print("""
[3/4] Paste your GitHub Personal Access Token
(get one at github.com/settings/tokens -- scope: public_repo):""")
gh = input("> ").strip()

# Write .env
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")
env_content = f"""TELEGRAM_TOKEN={tg}
OPENROUTER_API_KEY={api_key}
GITHUB_TOKEN={gh}
LLM_BASE_URL={base_url}
LLM_MODEL={model}
"""
with open(env_path, "w") as f:
    f.write(env_content)
print("\n.env saved.")

# Step 4: Install & run
print("\n[4/4] Installing dependencies and starting the bot...")

# Install deps
print("  Installing Python packages...")
result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "-r",
     os.path.join(script_dir, "requirements.txt"), "-q"],
    capture_output=True, text=True
)
if result.returncode != 0:
    print("  ERROR installing packages:")
    print(result.stderr)
    sys.exit(1)
print("  Packages installed.")

# Detect if systemd is available
has_systemd = subprocess.run(["which", "systemctl"], capture_output=True).returncode == 0

if has_systemd:
    service_name = "gh-search-bot"
    service_path = f"/etc/systemd/system/{service_name}.service"
    python_bin = sys.executable
    bot_path = os.path.join(script_dir, "bot.py")

    service_content = f"""[Unit]
Description=GH-najdi Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory={script_dir}
ExecStart={python_bin} {bot_path}
Restart=always
RestartSec=5
EnvironmentFile={env_path}

[Install]
WantedBy=multi-user.target
"""
    try:
        with open(service_path, "w") as f:
            f.write(service_content)
        subprocess.run(["systemctl", "daemon-reload"], check=True, capture_output=True)
        subprocess.run(["systemctl", "enable", service_name], check=True, capture_output=True)
        subprocess.run(["systemctl", "restart", service_name], check=True, capture_output=True)
        time.sleep(3)
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True, text=True
        )
        if result.stdout.strip() == "active":
            print(f"  Bot started as systemd service: {service_name}")
            print(f"  Check logs: journalctl -u {service_name} -f")
        else:
            print(f"  Service status: {result.stdout.strip()}")
            print(f"  Check logs: journalctl -u {service_name} -n 20")
    except Exception as e:
        print(f"  Could not create systemd service: {e}")
        print(f"  Start manually: python3 {bot_path}")
else:
    print("  systemd not available. Start manually:")
    print(f"  python3 {os.path.join(script_dir, 'bot.py')}")

print(f"""
========================================
   Setup complete!
   Provider: {p['name']}
   Model:    {model}
========================================
""")
