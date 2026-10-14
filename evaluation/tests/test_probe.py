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
