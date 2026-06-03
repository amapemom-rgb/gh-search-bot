import os, httpx, json, sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

llm = ChatOpenAI(
    model="qwen/qwen3.7-max",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.5,
    max_tokens=4000,
)

@tool
def search_github(query: str, language: str = "", min_stars: int = 0) -> str:
    "Search GitHub repositories."
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
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    with httpx.Client(timeout=10) as client:
        repo = client.get(f"https://api.github.com/repos/{repo_full_name}", headers=headers).json()
        commits = client.get(f"https://api.github.com/repos/{repo_full_name}/commits", headers=headers, params={"per_page": 1}).json()
    last = commits[0]["commit"]["committer"]["date"][:10] if commits and isinstance(commits, list) else "unknown"
    return json.dumps({"name": repo.get("full_name"), "stars": repo.get("stargazers_count"), "forks": repo.get("forks_count"), "description": repo.get("description"), "topics": repo.get("topics",[]), "license": repo.get("license",{}).get("spdx_id") if repo.get("license") else "none", "last_commit": last, "open_issues": repo.get("open_issues_count"), "archived": repo.get("archived",False), "url": repo.get("html_url")}, ensure_ascii=False)

@tool
def search_huggingface(query: str, task: str = "") -> str:
    "Search AI models and datasets on HuggingFace."
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

SOUL = open("/opt/github-search/SOUL.md").read()
SKILL = open("/opt/github-search/SKILL.md").read()
SYSTEM_PROMPT = SOUL + "\n\n" + SKILL + "\n\nTy pomogaesh najti open-source proekty na GitHub."

conn = sqlite3.connect("/opt/github-search/memory.db", check_same_thread=False)
memory = SqliteSaver(conn)

agent = create_react_agent(llm, [search_github, get_repo_details, search_huggingface], prompt=SYSTEM_PROMPT, checkpointer=memory)

async def run_agent(user_message: str, thread_id: str) -> str:
    config = {"configurable": {"thread_id": thread_id}}
    state = await agent.aget_state(config)
    if state and state.values.get("messages"):
        msgs = state.values["messages"]
        if len(msgs) > 20:
            await agent.aupdate_state(config, {"messages": msgs[-20:]})
    result = await agent.ainvoke({"messages": [HumanMessage(content=user_message)]}, config=config)
    return result["messages"][-1].content
