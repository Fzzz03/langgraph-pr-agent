"""Research Agent — only runs for issues the planner marked 'complex'.
Pulls a wider slice of the repo (more files, deeper search) so the code
writer has enough context for a multi-file change. This is the node your
conditional edge routes to before looping back into code_writer.
"""

from state import AgentState
from github_tools import search_repo_files, get_file_content
from llm import get_llm

PROMPT = """The following issue was classified as complex and needs deeper
investigation before a fix can be planned in detail.

ISSUE:
{issue}

INITIAL PLAN:
{plan}

ADDITIONAL CODE CONTEXT:
{extra_context}

Write concise research notes: what other parts of the codebase are
affected, what risks or edge cases exist, and anything the code writer
needs to know that wasn't in the initial plan.
"""


def research_agent(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        # widen the search net beyond what code_reader originally grabbed
        wider_paths = search_repo_files(state["repo"], state["issue"], max_results=10)
        extra_chunks = []
        for path in wider_paths:
            content = get_file_content(state["repo"], path)
            if content and path not in state["code_context"]:
                extra_chunks.append(f"### {path}\n```\n{content[:2000]}\n```")
        extra_context = "\n\n".join(extra_chunks) or "No additional files found."

        llm = get_llm()
        notes = llm.invoke(
            PROMPT.format(
                issue=state["issue"], plan=state["plan"], extra_context=extra_context
            )
        ).content

        return {
            **state,
            "research_notes": notes,
            "code_context": state["code_context"] + "\n\n" + extra_context,
        }
    except Exception as e:
        return {**state, "error": f"research_agent failed: {e}"}
