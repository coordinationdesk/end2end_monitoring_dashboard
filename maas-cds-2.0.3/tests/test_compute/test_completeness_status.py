from maas_cds.model.enumeration import CompletenessStatus

from maas_cds.model.datatake import (
    evaluate_completeness_status,
)


def test_evaluate_completeness_status_missing():
    "evaluate_completeness_status missing test"

    status = evaluate_completeness_status(0)

    assert status == CompletenessStatus.MISSING.value


def test_evaluate_completeness_status_partial():
    "evaluate_completeness_status partial test"

    status = evaluate_completeness_status(50)

    assert status == CompletenessStatus.PARTIAL.value


def test_evaluate_completeness_status_complete():
    "evaluate_completeness_status complete test"

    status = evaluate_completeness_status(100)

    assert status == CompletenessStatus.COMPLETE.value
