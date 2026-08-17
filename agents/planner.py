"""Agent 02 — Planner
Reads the issue + code context and produces a step-by-step plan.
Also classifies complexity ("simple" | "complex") which the graph's
conditional edge uses to decide whether to route through the research
agent first or go straight to the code writer.
"""

from state import AgentState
from llm import get_llm

PROMPT = """You are a senior software engineer planning a fix for a GitHub issue.

ISSUE:
{issue}

RELEVANT CODE:
{code_context}

Produce:
1. A short step-by-step plan to resolve the issue.
2. A final line, exactly formatted as: COMPLEXITY: simple  OR  COMPLEXITY: complex

Use "complex" only if the fix touches multiple files/modules, needs
architectural changes, or requires information not present in the code
shown above. Otherwise use "simple".
"""


def planner_agent(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        llm = get_llm()
        response = llm.invoke(
            PROMPT.format(issue=state["issue"], code_context=state["code_context"])
        ).content

        complexity = "simple"
        if "COMPLEXITY: complex" in response:
            complexity = "complex"

        plan = response.split("COMPLEXITY:")[0].strip()

        return {**state, "plan": plan, "complexity": complexity}
    except Exception as e:
        return {**state, "error": f"planner failed: {e}"}


def route_by_complexity(state: AgentState) -> str:
    """Used by workflow.add_conditional_edges — returns the branch key."""
    if state.get("error"):
        return "error"
    return state.get("complexity", "simple")
