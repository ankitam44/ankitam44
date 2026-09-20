"""Deal-risk / champion-health agent for expansion & renewal motions.

Given deal metadata plus recent activity notes (calls, emails, CRM fields), flags
stalled deals, weak champion engagement, and renewal risk with a recommended action.
"""

from typing import List, Literal

import anthropic
from pydantic import BaseModel, Field

MODEL = "claude-opus-5"

SYSTEM_PROMPT = """You are a Revenue Operations analyst supporting Customer Success and \
Account Management at an enterprise SaaS company. You review renewal and expansion deals \
and flag risk for a CSM/AM who needs to act this week, not next quarter.

Signals that indicate risk:
- Long gaps since last meaningful activity (calls, emails, product usage mentions)
- Champion has gone quiet, changed roles, or left the company
- No economic buyer / decision-maker engaged
- Negative sentiment in notes (frustration, competitor mentions, budget concerns)
- Usage or adoption concerns mentioned in notes
- Renewal or expansion date approaching without a clear next step

Be concrete and calibrated. Do not invent facts not present in the notes. If notes are \
sparse, treat that itself as a risk signal (lack of visibility) rather than assuming health."""


class DealRiskAssessment(BaseModel):
    risk_level: Literal["Low", "Medium", "High", "Critical"]
    risk_score: int = Field(ge=0, le=100, description="Higher = more at risk")
    renewal_probability_pct: int = Field(ge=0, le=100)
    champion_health: Literal["Strong", "Weak", "Unknown", "Missing"]
    key_risk_factors: List[str]
    positive_signals: List[str] = Field(description="Any signals working in our favor")
    recommended_action: str = Field(
        description="One concrete, specific action the CSM/AM should take this week"
    )


def assess_deal(
    deal_name: str,
    arr: str,
    stage: str,
    days_since_last_activity: str,
    champion_name_title: str,
    notes: str,
    client: anthropic.Anthropic | None = None,
) -> DealRiskAssessment:
    client = client or anthropic.Anthropic()

    user_content = (
        f"Deal: {deal_name}\n"
        f"ARR: {arr}\n"
        f"Stage: {stage}\n"
        f"Days since last activity: {days_since_last_activity}\n"
        f"Champion: {champion_name_title or '(none identified)'}\n\n"
        f"Recent notes (calls, emails, CRM activity):\n"
        f"{notes.strip() or '(no notes provided)'}"
    )

    response = client.messages.parse(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
        output_format=DealRiskAssessment,
    )

    return response.parsed_output
