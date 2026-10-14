"""Deterministic M0 guardrails; no Ollama runtime required."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from evaluation.probe import Analysis, Decision, sanitize


def make_result(questions):
    return Analysis.model_validate({
        "feature_label": "Booking", "questions": questions,
        "caution": "Developer should confirm these suggested gaps.",
    })


def make_question(key, text, excerpt="Customers can book slots"):
    return {
        "gap_key": key,
        "question": text,
        "why_it_matters": "Affects behavior and data consistency.",
        "source_excerpt": excerpt,
        "priority": 1,
    }


def test_resolved_topic_cannot_reappear_exact_key():
    a = make_result([make_question("booking.double_booking", "Can two users confirm one time slot?")])
    decision = Decision(gap_key="booking.double_booking", question="Can two users confirm one time slot?", status="answered", detail="No, first confirmation wins")
    checked = sanitize(a, "Customers can book slots", [decision])
    assert checked["questions"] == []
    assert checked["removed"]["resolved_keys"] == ["booking.double_booking"]


def test_unrelated_key_not_suppressed():
    a = make_result([make_question("booking.cancellation", "Can users cancel a confirmed time slot?")])
    decision = Decision(gap_key="booking.double_booking", question="Can two users confirm one slot?", status="answered", detail="No")
    assert len(sanitize(a, "Customers can book slots", [decision])["questions"]) == 1


def test_fabricated_excerpt_omitted_and_counted():
    a = make_result([make_question("booking.double_booking", "Can two users confirm one slot?", "Client said: never allow duplicates")])
    checked = sanitize(a, "Customers can book slots", [])
    assert checked["questions"][0]["source_excerpt"] is None
    assert checked["removed"]["fabricated_excerpts"]


def test_duplicate_gap_key_removed():
    a = make_result([
        make_question("booking.double_booking", "Can two users confirm one slot?"),
        make_question("booking.double_booking", "What if two clients choose the same slot?"),
    ])
    checked = sanitize(a, "Customers can book slots", [])
    assert len(checked["questions"]) == 1


def test_invalid_shape_rejected():
    with pytest.raises(ValidationError):
        make_result([make_question("not-a-valid-key", "Does this malformed gap key pass validation?")])
    with pytest.raises(ValidationError):
        make_result([make_question("booking.gap", "Question one?")] * 4)


def test_empty_answer_rejected():
    with pytest.raises(ValidationError):
        Decision(gap_key="booking.double_booking", question="What happens when slots overlap?", status="answered", detail="")


from types import SimpleNamespace
from evaluation.probe import run_model


class FakeOllamaClient:
    def __init__(self, response):
        self.response = response
        self.last_kwargs = None

    def chat(self, **kwargs):
        self.last_kwargs = kwargs
        return self.response


def test_truncated_and_repetitive_json_returns_safe_diagnostics():
    raw = '{"feature_label":"Booking","questions":[' + "01" * 260
    response = SimpleNamespace(
        message=SimpleNamespace(content=raw),
        done_reason="length",
        eval_count=512,
        prompt_eval_count=128,
    )
    client = FakeOllamaClient(response)
    result = run_model(
        client=client, model="test", notes="synthetic booking notes",
        decisions=[], mode="baseline", num_ctx=2048, num_predict=512,
    )
    assert result["validated"] is False
    assert result["diagnostics"]["possible_output_truncation"] is True
    assert result["diagnostics"]["repetitive_tail_suspected"] is True
    assert result["diagnostics"]["eval_count"] == 512
    assert raw not in str(result)
    assert client.last_kwargs["options"]["num_predict"] == 512


def test_valid_json_reports_metadata_and_preserves_result():
    import json
    valid = {
        "feature_label": "Booking",
        "questions": [{
            "gap_key": "booking.double_booking",
            "question": "Can both customers reserve the same time slot?",
            "why_it_matters": "Could allow duplicate confirmed bookings.",
            "source_excerpt": None,
            "priority": 1,
        }],
        "caution": "Developer must confirm the decision.",
    }
    response = SimpleNamespace(
        message=SimpleNamespace(content=json.dumps(valid)),
        done_reason="stop", eval_count=98, prompt_eval_count=100,
    )
    result = run_model(
        client=FakeOllamaClient(response), model="test",
        notes="Bookings are available online", decisions=[], mode="unasked",
        num_ctx=2048, num_predict=512,
    )
    assert result["validated"] is True
    assert len(result["result"]["questions"]) == 1
    assert result["diagnostics"]["possible_output_truncation"] is False
    assert result["diagnostics"]["ends_with_json_brace"] is True


def test_json_mode_drops_schema_constraint_but_keeps_validation():
    import json
    response = SimpleNamespace(
        message=SimpleNamespace(content=json.dumps({
            "feature_label": "Booking",
            "questions": [],
            "caution": "Developer must review the suggested gaps.",
        })),
        done_reason="stop", eval_count=40, prompt_eval_count=100,
    )
    client = FakeOllamaClient(response)
    result = run_model(
        client=client, model="test", notes="Synthetic booking requirements",
        decisions=[], mode="baseline", num_ctx=2048, num_predict=512,
        format_mode="json",
    )
    assert client.last_kwargs["format"] == "json"
    assert "feature_label" in client.last_kwargs["messages"][0]["content"]
    assert result["validated"] is True
    assert result["diagnostics"]["format_mode"] == "json"


def test_json_mode_invalid_response_keeps_only_safe_metadata():
    response = SimpleNamespace(
        message=SimpleNamespace(content='{"feature_label":"01' + "01" * 250),
        done_reason="length", eval_count=512, prompt_eval_count=100,
    )
    client = FakeOllamaClient(response)
    result = run_model(
        client=client, model="test", notes="Synthetic booking requirements",
        decisions=[], mode="baseline", num_ctx=2048, num_predict=512,
        format_mode="json",
    )
    assert result["validated"] is False
    assert result["diagnostics"]["possible_output_truncation"] is True
    assert "raw_preview_start" not in result["diagnostics"]
    assert client.last_kwargs["format"] == "json"


def test_explicit_raw_preview_for_fictional_fixtures_only():
    response = SimpleNamespace(
        message=SimpleNamespace(content='{"feature_label":"01' + "01" * 250),
        done_reason="length", eval_count=512, prompt_eval_count=100,
    )
    result = run_model(
        client=FakeOllamaClient(response), model="test",
        notes="Fictional booking requirements", decisions=[], mode="baseline",
        num_ctx=2048, num_predict=512, debug_raw_preview=True,
    )
    assert result["validated"] is False
    assert result["diagnostics"]["raw_preview_start"].startswith('{"feature_label"')
    assert len(result["diagnostics"]["raw_preview_end"]) <= 160
