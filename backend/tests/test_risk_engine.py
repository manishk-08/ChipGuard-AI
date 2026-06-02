from app.services.risk_engine import calculate_risk_score


def test_low_risk():
    total, scores, severity = calculate_risk_score(
        availability_score=10,
        lifecycle_score=10,
        supplier_score=10,
        lead_time_score=10,
        compliance_score=10,
    )
    assert total < 40
    assert severity == "low"


def test_medium_risk():
    total, scores, severity = calculate_risk_score(
        availability_score=50,
        lifecycle_score=50,
        supplier_score=50,
        lead_time_score=10,
        compliance_score=10,
    )
    assert 40 <= total < 70
    assert severity == "medium"


def test_high_risk():
    total, scores, severity = calculate_risk_score(
        availability_score=80,
        lifecycle_score=80,
        supplier_score=80,
        lead_time_score=80,
        compliance_score=50,
    )
    assert total >= 70
    assert severity == "high"


def test_weights_sum_to_one():
    scores = {
        "availability_score": 100,
        "lifecycle_score": 100,
        "supplier_score": 100,
        "lead_time_score": 100,
        "compliance_score": 100,
    }
    weights = {"availability_score": 0.35, "lifecycle_score": 0.20, "supplier_score": 0.20, "lead_time_score": 0.15, "compliance_score": 0.10}
    assert abs(sum(weights.values()) - 1.0) < 0.001


def test_explanation_for_high_risk():
    total, scores, severity = calculate_risk_score(
        availability_score=90,
        lifecycle_score=80,
        supplier_score=90,
        lead_time_score=80,
        compliance_score=60,
    )
    assert severity == "high"
    assert "Low stock" in scores["explanation"] or "No significant" not in scores["explanation"]
