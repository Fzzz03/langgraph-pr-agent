"""Agent 01 — Code Reader
Fetches the issue and pulls the most relevant file contents from the repo
so downstream agents have real code context to work with.
"""

from state import AgentState
from github_tools import get_issue, search_repo_files, get_file_content


def code_reader_agent(state: AgentState) -> AgentState:
    try:
        issue = get_issue(state["repo"], state["issue_number"])
        issue_text = f"{issue['title']}\n\n{issue['body']}"

        relevant_paths = search_repo_files(state["repo"], issue_text)
        chunks = []
        for path in relevant_paths:
            content = get_file_content(state["repo"], path)
            if content:
                chunks.append(f"### {path}\n```\n{content[:3000]}\n```")

        return {
            **state,
            "issue": issue_text,
            "code_context": "\n\n".join(chunks) or "No matching files found.",
        }
    except Exception as e:
        return {**state, "error": f"code_reader failed: {e}"}
