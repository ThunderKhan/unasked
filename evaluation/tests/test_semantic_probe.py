"""Semantic probe tests: no Ollama server or GPU needed."""
from types import SimpleNamespace

import pytest

from evaluation.semantic_probe import build_messages, run_case


CASE = {
    "id": "booking",
    "notes": "Visitors reserve times; cancellation is not allowed.",
    "gold_missing_topics": [{"gap_key": "booking.double_booking", "description": "Slot conflicts"}],
    "explicitly_answered_topics": ["booking.cancellation_policy"],
    "followup_decision": {
        "question": "Can two customers confirm the same time slot?",
        "detail": "No. Only the first customer can confirm.",
    },
}


def test_generic_and_risk_prompts_are_distinct():
    generic = build_messages(CASE, "generic", False)
    risk = build_messages(CASE, "risk", False)
    assert generic[0]["content"] != risk[0]["content"]
    assert generic[1] == risk[1]
    assert "JSON" not in generic[0]["content"]
    assert "JSON" not in risk[0]["content"]


def test_answer_is_added_only_when_requested():
    first = build_messages(CASE, "risk", False)[1]["content"]
    answered = build_messages(CASE, "risk", True)[1]["content"]
    assert "Only the first customer" not in first
    assert "Only the first customer" in answered
    assert "cancellation is not allowed" in answered


def test_invalid_mode_rejected():
    with pytest.raises(ValueError):
        build_messages(CASE, "unsupported", False)


def test_inference_does_not_pass_format_parameter():
    class FakeClient:
        def chat(self, **kwargs):
            assert "format" not in kwargs
            assert kwargs["options"]["num_predict"] == 256
            return SimpleNamespace(
                message=SimpleNamespace(content="1. What if two people choose a slot?"),
                done_reason="stop", eval_count=24,
            )
    result = run_case(client=FakeClient(), model="test", case=CASE,
                      mode="risk", after_answer=False, num_ctx=2048,
                      num_predict=256)
    assert "two people" in result["response"]
    assert result["case_id"] == "booking"
