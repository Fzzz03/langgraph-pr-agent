"""
Thin wrapper around the GitHub REST API. No PyGithub dependency —
just requests, so it's easy to read and easy to swap out.
"""

import os
import base64
import requests

API = "https://api.github.com"


def _headers():
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_issue(repo: str, issue_number: int) -> dict:
    r = requests.get(f"{API}/repos/{repo}/issues/{issue_number}", headers=_headers())
    r.raise_for_status()
    data = r.json()
    return {"title": data["title"], "body": data.get("body") or ""}


def search_repo_files(repo: str, query: str, max_results: int = 5) -> list[str]:
    """Very lightweight relevance search: pull the repo's default file tree
    and keyword-match paths against the issue text. Good enough for a demo;
    swap in embeddings/AST search for something more serious."""
    default_branch = requests.get(f"{API}/repos/{repo}", headers=_headers()).json().get(
        "default_branch", "main"
    )
    tree = requests.get(
        f"{API}/repos/{repo}/git/trees/{default_branch}?recursive=1", headers=_headers()
    ).json()
    paths = [item["path"] for item in tree.get("tree", []) if item["type"] == "blob"]

    keywords = [w.lower() for w in query.split() if len(w) > 3]
    scored = sorted(
        paths,
        key=lambda p: sum(kw in p.lower() for kw in keywords),
        reverse=True,
    )
    return scored[:max_results]


def get_file_content(repo: str, path: str) -> str:
    r = requests.get(f"{API}/repos/{repo}/contents/{path}", headers=_headers())
    if r.status_code != 200:
        return ""
    data = r.json()
    if data.get("encoding") == "base64":
        return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    return data.get("content", "")


def open_pull_request(repo: str, branch: str, title: str, body: str, base: str = "main") -> str:
    """Opens a real PR. Requires GITHUB_TOKEN with repo write access and an
    existing `branch` with commits already pushed. Returns the PR URL."""
    r = requests.post(
        f"{API}/repos/{repo}/pulls",
        headers=_headers(),
        json={"title": title, "head": branch, "base": base, "body": body},
    )
    r.raise_for_status()
    return r.json()["html_url"]
