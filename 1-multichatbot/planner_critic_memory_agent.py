"""Planner -> Critic loop with memory, built as a small LangGraph graph.

The planner proposes a plan for the given task; the critic reviews it.
If the critic isn't satisfied, its feedback is carried in memory and the
planner tries again (up to MAX_ITERATIONS times).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "1-tool-integration"))

from langgraph.graph import StateGraph, END  # noqa: E402
from langchain.schema import HumanMessage  # noqa: E402
from email_utils import get_llm  # noqa: E402

MAX_ITERATIONS = 3

llm = get_llm()


def planner_node(state):
    task = state["task"]
    memory = state.get("memory", [])

    feedback_block = ""
    if memory:
        last_critique = memory[-1]["critique"]
        feedback_block = (
            f"\n\nYour previous plan was rejected with this feedback:\n{last_critique}\n"
            "Revise the plan accordingly."
        )

    prompt = (
        "You are a planning agent. Break this task into a short numbered list of "
        f"concrete steps:\n\nTask: {task}{feedback_block}"
    )
    plan = llm([HumanMessage(content=prompt)]).content

    return {**state, "plan": plan, "iterations": state.get("iterations", 0) + 1}


def critic_node(state):
    plan = state["plan"]
    task = state["task"]

    prompt = f"""You are a critic agent reviewing a plan.
Task: {task}
Plan:
{plan}

Is this plan complete, concrete, and safe to execute? Answer with "APPROVED" on the
first line if so. Otherwise answer with "REJECTED" on the first line followed by
specific feedback on what to fix."""
    critique = llm([HumanMessage(content=prompt)]).content
    approved = critique.strip().upper().startswith("APPROVED")

    memory = state.get("memory", []) + [{"plan": plan, "critique": critique}]
    return {**state, "critique": critique, "approved": approved, "memory": memory}


def route_after_critic(state):
    if state["approved"] or state["iterations"] >= MAX_ITERATIONS:
        return END
    return "planner"


builder = StateGraph(dict)
builder.add_node("planner", planner_node)
builder.add_node("critic", critic_node)
builder.set_entry_point("planner")
builder.add_edge("planner", "critic")
builder.add_conditional_edges("critic", route_after_critic, {"planner": "planner", END: END})
graph = builder.compile()


def run(task):
    return graph.invoke({"task": task, "memory": [], "iterations": 0})


if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) or input("🧑 Task for the planner/critic agent: ")
    result = run(task)
    print(f"\n✅ Finished after {result['iterations']} iteration(s), approved={result['approved']}:\n")
    print(result["plan"])
