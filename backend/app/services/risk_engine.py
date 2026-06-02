from typing import Optional


def calculate_risk_score(
    availability_score: Optional[float] = None,
    lifecycle_score: Optional[float] = None,
    supplier_score: Optional[float] = None,
    lead_time_score: Optional[float] = None,
    compliance_score: Optional[float] = None,
) -> tuple[float, dict[str, float], str]:
    scores = {
        "availability_score": availability_score or 0,
        "lifecycle_score": lifecycle_score or 0,
        "supplier_score": supplier_score or 0,
        "lead_time_score": lead_time_score or 0,
        "compliance_score": compliance_score or 0,
    }

    weights = {
        "availability_score": 0.35,
        "lifecycle_score": 0.20,
        "supplier_score": 0.20,
        "lead_time_score": 0.15,
        "compliance_score": 0.10,
    }

    total = sum(scores[k] * weights[k] for k in weights)

    if total >= 70:
        severity = "high"
    elif total >= 40:
        severity = "medium"
    else:
        severity = "low"

    explanations = []
    if (availability_score or 0) >= 60:
        explanations.append("Low stock or no stock across distributors")
    if (lifecycle_score or 0) >= 50:
        explanations.append("Part is obsolete, end-of-life, or not recommended for new designs")
    if (supplier_score or 0) >= 50:
        explanations.append("Single source or concentrated supplier risk")
    if (lead_time_score or 0) >= 50:
        explanations.append("Long or unpredictable lead times")
    if (compliance_score or 0) >= 50:
        explanations.append("Export compliance review recommended")

    explanation = "; ".join(explanations) if explanations else "No significant risks detected"

    scores["explanation"] = explanation
    return total, scores, severity
