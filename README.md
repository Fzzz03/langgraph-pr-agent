# LangGraph PR Agent

I built this to see if a multi-agent setup could actually take a GitHub
issue and turn it into a real patch — not just chat about the code, but
read it, plan a fix, write it, write tests for it, and open a PR.

It's built with [LangGraph](https://github.com/langchain-ai/langgraph),
using a supervisor-style graph where each agent is a node and a planner
decides how the issue should be routed.

## How it works

```
Issue → Code Reader → Planner ──(simple)──→ Code Writer → Test Writer → PR Opener → PR
                           └──(complex)──→ Research Agent ──┘
```

- **Code Reader** pulls the issue + the most relevant files from the repo
- **Planner** writes a step-by-step plan and decides if the issue is
  `simple` or `complex`
- **Research Agent** only runs for complex issues — grabs more context
  before handing off
- **Code Writer** turns the plan into an actual diff
- **Test Writer** writes tests against that diff
- **PR Opener** either saves everything locally (dry-run) or actually
  pushes a branch and opens the PR

Everything flows through one shared state object (`AgentState`), so each
agent just reads what it needs and adds its own piece.

