"""Mock CRM deal data — stands in for a live Salesforce/HubSpot pull + call transcripts."""

SAMPLE_DEALS = {
    "Northwind Logistics — Renewal": {
        "arr": "$180,000",
        "stage": "Renewal — 45 days out",
        "days_since_last_activity": "62",
        "champion_name_title": "Priya Shah, VP Sales Operations",
        "notes": """\
- Last QBR was 3 months ago; two follow-up emails from our CSM went unanswered
- Priya was promoted to VP two months ago; unclear if she still owns this relationship
- Support ticket volume down 40% quarter-over-quarter (could mean fewer issues, or \
declining usage — unclear which)
- No response to renewal outreach sent 2 weeks ago
- Original champion's direct report (a daily active user) mentioned in a support \
ticket that they've "mostly gone back to spreadsheets for this\"""",
    },
    "Solace Health — Expansion": {
        "arr": "$95,000 current / $250,000 proposed expansion",
        "stage": "Expansion — proposal sent",
        "days_since_last_activity": "5",
        "champion_name_title": "Marcus Webb, Chief Digital Officer",
        "notes": """\
- Marcus personally requested the expansion after a successful pilot with 2 regional teams
- Call notes from last week: "budget is approved in principle, just need procurement sign-off"
- Procurement contact (Linda Ortiz) looped in and responsive within 24 hours each time
- Legal redlines on the MSA were minor and resolved in one round
- Marcus mentioned a competitor demo happened 6 months ago before he joined, no recent \
competitive mentions""",
    },
    "Bramblewood — Renewal": {
        "arr": "$12,000",
        "stage": "Renewal — 20 days out",
        "days_since_last_activity": "90",
        "champion_name_title": "(unknown — original contact left company 4 months ago)",
        "notes": """\
- Original champion (Head of Ops) left the company; no replacement contact identified
- Zero logins to the product in the last 60 days per usage data mentioned by CSM in Slack
- Auto-renewal invoice sent, no response
- Company website shows a "we're hiring" banner but no reply to 3 outreach attempts""",
    },
}
