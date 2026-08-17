r"""
LangGraph StateGraph: Multi-Agent Flow
Issue -> Code Reader -> Planner --(simple)--> Code Writer -> Test Writer -> PR Opener -> PR
                              \--(complex)--> Research Agent --/
"""

from langgraph.graph import StateGraph, END

from state import AgentState
from agents.code_reader import code_reader_agent
from agents.planner import planner_agent, route_by_complexity
from agents.research_agent import research_agent
from agents.code_writer import code_writer_agent
from agents.test_writer import test_writer_agent
from agents.pr_opener import pr_opener_agent


def build_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node("code_reader", code_reader_agent)
    workflow.add_node("planner", planner_agent)
    workflow.add_node("research_agent", research_agent)
    workflow.add_node("code_writer", code_writer_agent)
    workflow.add_node("test_writer", test_writer_agent)
    workflow.add_node("pr_opener", pr_opener_agent)

    workflow.set_entry_point("code_reader")
    workflow.add_edge("code_reader", "planner")

    # conditional routing based on the planner's complexity call
    workflow.add_conditional_edges(
        "planner",
        route_by_complexity,
        {
            "simple": "code_writer",
            "complex": "research_agent",
            "error": END,
        },
    )

    workflow.add_edge("research_agent", "code_writer")
    workflow.add_edge("code_writer", "test_writer")
    workflow.add_edge("test_writer", "pr_opener")
    workflow.add_edge("pr_opener", END)

    return workflow.compile()


graph = build_workflow()
