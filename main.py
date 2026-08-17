"""
Run the multi-agent pipeline against a real GitHub issue.

Usage:
    python main.py owner/repo 42
    DRY_RUN=false python main.py owner/repo 42   # actually opens a PR
"""

import sys
import json

from langgraph_workflow import graph


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py owner/repo <issue_number>")
        sys.exit(1)

    repo = sys.argv[1]
    issue_number = int(sys.argv[2])

    initial_state = {
        "repo": repo,
        "issue_number": issue_number,
    }

    print(f"Running pipeline for {repo}#{issue_number} ...\n")
    final_state = graph.invoke(initial_state)

    if final_state.get("error"):
        print(f"❌ Pipeline stopped early: {final_state['error']}")
        sys.exit(1)

    print("✅ Pipeline complete.\n")
    print("=== PLAN ===")
    print(final_state.get("plan", ""))
    print("\n=== PATCH (also saved to output/patch.diff) ===")
    print(final_state.get("patch", "")[:1500])
    print("\n=== TESTS (also saved to output/tests.py) ===")
    print(final_state.get("tests", "")[:1000])

    if final_state.get("pr_url"):
        print(f"\n🔗 PR opened: {final_state['pr_url']}")
    else:
        print("\n(DRY_RUN mode — no PR opened, files written to ./output/)")


if __name__ == "__main__":
    main()
