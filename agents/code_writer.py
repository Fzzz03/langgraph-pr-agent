"""Agent 03 — Code Writer
Turns the plan (+ research notes, if any) into an actual patch.
"""

from state import AgentState
from llm import get_llm

PROMPT = """You are implementing a fix for this GitHub issue.

ISSUE:
{issue}

PLAN:
{plan}

RESEARCH NOTES (if any):
{research_notes}

CODE CONTEXT:
{code_context}

Write the code change as a unified diff (git diff format). Only output
the diff — no explanation, no markdown fences.
"""


def code_writer_agent(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        llm = get_llm()
        patch = llm.invoke(
            PROMPT.format(
                issue=state["issue"],
                plan=state["plan"],
                research_notes=state.get("research_notes", "None"),
                code_context=state["code_context"],
            )
        ).content

        return {**state, "patch": patch}
    except Exception as e:
        return {**state, "error": f"code_writer failed: {e}"}
