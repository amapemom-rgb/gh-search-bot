# (c) 2026 amapemom-rgb — https://github.com/amapemom-rgb/gh-search-bot
# Licensed under MIT License

import os, httpx, json, aiosqlite, logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger("gh-agent")
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

BASE_DIR = Path(__file__).parent

llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL", "qwen/qwen3.7-max"),
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
    temperature=0.5,
    max_tokens=4000,
)

@tool
def search_github(query: str, language: str = "", min_stars: int = 0) -> str:
    "Search GitHub repositories."
    logger.info(f"[TOOL] search_github: {query} lang={language} stars>={min_stars}")
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    q = query
    if language: q += f" language:{language}"
    if min_stars > 0: q += f" stars:>={min_stars}"
    params = {"q": q, "sort": "stars", "order": "desc", "per_page": 20}
    with httpx.Client(timeout=10) as client:
        data = client.get("https://api.github.com/search/repositories", headers=headers, params=params).json()
    if "items" not in data:
        return f"Error: {data.get('message', 'unknown')}"
    results = [{"name": r["full_name"], "stars": r["stargazers_count"], "description": r.get("description",""), "url": r["html_url"], "language": r.get("language",""), "license": r.get("license",{}).get("spdx_id","none") if r.get("license") else "none", "updated": r["updated_at"][:10], "archived": r.get("archived",False)} for r in data["items"][:15]]
    return json.dumps(results, ensure_ascii=False)

@tool
def get_repo_details(repo_full_name: str) -> str:
    "Get detailed info about a repository."
    logger.info(f"[TOOL] get_repo_details: {repo_full_name}")
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    with httpx.Client(timeout=10) as client:
        repo = client.get(f"https://api.github.com/repos/{repo_full_name}", headers=headers).json()
        commits = client.get(f"https://api.github.com/repos/{repo_full_name}/commits", headers=headers, params={"per_page": 1}).json()
    last = commits[0]["commit"]["committer"]["date"][:10] if commits and isinstance(commits, list) else "unknown"
    return json.dumps({"name": repo.get("full_name"), "stars": repo.get("stargazers_count"), "forks": repo.get("forks_count"), "description": repo.get("description"), "topics": repo.get("topics",[]), "license": repo.get("license",{}).get("spdx_id") if repo.get("license") else "none", "last_commit": last, "open_issues": repo.get("open_issues_count"), "archived": repo.get("archived",False), "url": repo.get("html_url")}, ensure_ascii=False)

@tool
def search_huggingface(query: str, task: str = "") -> str:
    "Search AI models and datasets on HuggingFace."
    logger.info(f"[TOOL] search_huggingface: {query} task={task}")
    params = {"search": query, "limit": 10, "sort": "downloads", "direction": -1}
    if task:
        params["pipeline_tag"] = task
    with httpx.Client(timeout=10) as client:
        r = client.get("https://huggingface.co/api/models", params=params)
        models = r.json()
    if not models:
        return "Nothing found on HuggingFace."
    results = [{"id": m.get("id"), "downloads": m.get("downloads", 0), "likes": m.get("likes", 0), "task": m.get("pipeline_tag", ""), "url": f"https://huggingface.co/{m.get('id')}"}  for m in models[:8]]
    return json.dumps(results, ensure_ascii=False)


@tool
def search_npm(query: str) -> str:
    "Search npm packages (Node.js/JavaScript libraries)."
    logger.info(f"[TOOL] search_npm: {query}")
    with httpx.Client(timeout=10) as client:
        r = client.get("https://registry.npmjs.org/-/v1/search", params={"text": query, "size": 8})
        data = r.json()
    if "objects" not in data:
        return "Nothing found on npm."
    results = [{"name": p["package"]["name"], "description": p["package"].get("description",""), "version": p["package"]["version"], "url": f"https://www.npmjs.com/package/{p['package']['name']}", "weekly_downloads": p.get("downloads",{}).get("weekly",0)} for p in data["objects"][:8]]
    return json.dumps(results, ensure_ascii=False)

@tool
def search_pypi(query: str) -> str:
    "Search Python packages on PyPI."
    logger.info(f"[TOOL] search_pypi: {query}")
    with httpx.Client(timeout=10) as client:
        r = client.get("https://pypi.org/search/", params={"q": query}, headers={"Accept": "application/json"})
        data = r.json()
    if not data.get("results"):
        return "Nothing found on PyPI."
    results = [{"name": p["name"], "description": p.get("description",""), "version": p.get("version",""), "url": f"https://pypi.org/project/{p['name']}"} for p in data["results"][:8]]
    return json.dumps(results, ensure_ascii=False)

@tool
def search_awesome(query: str) -> str:
    "Search awesome-lists on GitHub (curated lists of tools and libraries)."
    logger.info(f"[TOOL] search_awesome: {query}")
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    params = {"q": f"awesome {query} in:name,description", "sort": "stars", "order": "desc", "per_page": 8}
    with httpx.Client(timeout=10) as client:
        data = client.get("https://api.github.com/search/repositories", headers=headers, params=params).json()
    if "items" not in data:
        return f"Error: {data.get('message', 'unknown')}"
    results = [{"name": r["full_name"], "stars": r["stargazers_count"], "description": r.get("description",""), "url": r["html_url"]} for r in data["items"][:8]]
    return json.dumps(results, ensure_ascii=False)

SOUL = open(BASE_DIR / "SOUL.md").read()
SKILL = open(BASE_DIR / "SKILL.md").read()
SYSTEM_PROMPT = SOUL + "\n\n" + SKILL + "\n\nTy pomogaesh najti open-source proekty na GitHub."

_agent = None

async def get_agent():
    global _agent
    if _agent is None:
        conn = await aiosqlite.connect(str(BASE_DIR / "memory.db"))
        memory = AsyncSqliteSaver(conn)
        _agent = create_react_agent(llm, [search_github, get_repo_details, search_huggingface, search_npm, search_pypi, search_awesome], prompt=SYSTEM_PROMPT, checkpointer=memory)
    return _agent

async def run_agent(user_message: str, thread_id: str) -> str:
    agent = await get_agent()
    config = {"configurable": {"thread_id": thread_id}}
    state = await agent.aget_state(config)
    if state and state.values.get("messages"):
        msgs = state.values["messages"]
        if len(msgs) > 20:
            await agent.aupdate_state(config, {"messages": msgs[-20:]})
    result = await agent.ainvoke({"messages": [HumanMessage(content=user_message)]}, config=config)
    return result["messages"][-1].content
