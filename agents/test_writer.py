"""Agent 04 — Test Writer
Generates tests that exercise the patch produced by the code writer.
"""

from state import AgentState
from llm import get_llm

PROMPT = """You are writing tests for the following code change.

ISSUE:
{issue}

PATCH:
{patch}

Write a focused test (or a small set of tests) that verifies this patch
fixes the issue. Match the testing framework already used in the code
context below if one is evident; otherwise default to pytest.

CODE CONTEXT:
{code_context}

Output only the test code.
"""


def test_writer_agent(state: AgentState) -> AgentState:
    if state.get("error"):
        return state
    try:
        llm = get_llm()
        tests = llm.invoke(
            PROMPT.format(
                issue=state["issue"],
                patch=state["patch"],
                code_context=state["code_context"],
            )
        ).content

        return {**state, "tests": tests}
    except Exception as e:
        return {**state, "error": f"test_writer failed: {e}"}
