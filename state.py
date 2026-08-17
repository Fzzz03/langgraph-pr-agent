"""
AgentState — the single shared object that flows through every node
in the graph. Each agent reads what it needs and writes its result
back in, so the state grows as it moves through the pipeline.
"""

from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):
    # --- input ---
    repo: str              # "owner/name"
    issue_number: int
    issue: str             # issue title + body, fetched by code_reader

    # --- working memory ---
    code_context: str      # relevant file contents pulled from the repo
    complexity: str        # "simple" | "complex" — set by the planner
    plan: str              # step-by-step plan produced by the planner
    research_notes: str    # extra context gathered for complex issues

    # --- outputs ---
    patch: str             # unified diff / new file contents
    tests: str             # generated test code
    pr_url: Optional[str]  # URL of the opened PR (None in dry-run mode)

    # --- control ---
    error: Optional[str]   # set by any node that fails, short-circuits the graph
