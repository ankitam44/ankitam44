import os

import streamlit as st

from agent import assess_deal
from sample_deals import SAMPLE_DEALS

st.set_page_config(page_title="Deal Risk Monitor Agent", page_icon="🚦", layout="centered")

st.title("🚦 Deal Risk & Champion Health Agent")
st.caption(
    "Enterprise SaaS GTM demo — flags stalled renewals/expansions and champion risk "
    "from CRM data + call/email notes. Built with the Claude API (structured outputs)."
)

if not os.environ.get("ANTHROPIC_API_KEY"):
    st.warning(
        "Set the `ANTHROPIC_API_KEY` environment variable before running — "
        "this app calls the Claude API directly and does not store or transmit your key.",
        icon="⚠️",
    )

with st.sidebar:
    st.subheader("Demo deals")
    st.write("In production this data comes from Salesforce/HubSpot + Gong/email. "
              "For this demo, pick a mock deal or paste your own.")
    chosen = st.selectbox("Load a sample deal", ["(none)"] + list(SAMPLE_DEALS.keys()))

defaults = {"arr": "", "stage": "", "days_since_last_activity": "", "champion_name_title": "", "notes": ""}
deal_name_default = ""
if chosen != "(none)":
    deal_name_default = chosen
    defaults = SAMPLE_DEALS[chosen]

deal_name = st.text_input("Deal name", value=deal_name_default)
col1, col2 = st.columns(2)
with col1:
    arr = st.text_input("ARR", value=defaults["arr"])
    days_since_last_activity = st.text_input(
        "Days since last activity", value=defaults["days_since_last_activity"]
    )
with col2:
    stage = st.text_input("Stage", value=defaults["stage"])
    champion_name_title = st.text_input("Champion (name, title)", value=defaults["champion_name_title"])

notes = st.text_area(
    "Recent notes (calls, emails, CRM activity, support tickets...)",
    value=defaults["notes"],
    height=220,
)

if st.button("Assess deal", type="primary", disabled=not deal_name):
    with st.spinner("Analyzing deal risk..."):
        try:
            result = assess_deal(deal_name, arr, stage, days_since_last_activity, champion_name_title, notes)
        except Exception as e:
            st.error(f"Request failed: {e}")
            st.stop()

    risk_color = {"Low": "green", "Medium": "orange", "High": "red", "Critical": "red"}[result.risk_level]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"### Risk: :{risk_color}[{result.risk_level}]")
    with col2:
        st.metric("Risk score", f"{result.risk_score}/100")
    with col3:
        st.metric("Renewal probability", f"{result.renewal_probability_pct}%")

    st.markdown(f"**Champion health:** {result.champion_health}")

    st.markdown("**Key risk factors**")
    for r in result.key_risk_factors:
        st.markdown(f"- {r}")

    if result.positive_signals:
        st.markdown("**Positive signals**")
        for p in result.positive_signals:
            st.markdown(f"- {p}")

    st.markdown("**Recommended action this week**")
    st.info(result.recommended_action)
