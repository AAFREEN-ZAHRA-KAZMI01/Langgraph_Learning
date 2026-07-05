from unittest.mock import MagicMock, patch

import planner_critic_memory_agent as pcm


def test_approves_on_first_try():
    with patch.object(pcm, "llm") as mock_llm:
        mock_llm.side_effect = [
            MagicMock(content="1. Do the thing"),
            MagicMock(content="APPROVED\nLooks good."),
        ]
        result = pcm.run("a simple task")

    assert result["approved"] is True
    assert result["iterations"] == 1
    assert len(result["memory"]) == 1


def test_stops_after_max_iterations_if_never_approved():
    with patch.object(pcm, "llm") as mock_llm:
        # planner, critic, planner, critic, planner, critic -> always rejected
        mock_llm.side_effect = [MagicMock(content=f"plan/critique {i}") for i in range(2 * pcm.MAX_ITERATIONS)]
        mock_llm.side_effect = [
            v if i % 2 == 0 else MagicMock(content="REJECTED\ntry again")
            for i, v in enumerate(mock_llm.side_effect)
        ]
        result = pcm.run("a task that's never good enough")

    assert result["approved"] is False
    assert result["iterations"] == pcm.MAX_ITERATIONS
    assert len(result["memory"]) == pcm.MAX_ITERATIONS


def test_second_planner_call_includes_prior_feedback():
    with patch.object(pcm, "llm") as mock_llm:
        mock_llm.side_effect = [
            MagicMock(content="plan v1"),
            MagicMock(content="REJECTED\nneeds more detail"),
            MagicMock(content="plan v2"),
            MagicMock(content="APPROVED\ngood now"),
        ]
        pcm.run("a task")

    second_planner_prompt = mock_llm.call_args_list[2][0][0][0].content
    assert "needs more detail" in second_planner_prompt
