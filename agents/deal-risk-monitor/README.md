# Deal Risk & Champion Health Agent

**Problem:** Renewal and expansion risk is usually caught late — a CSM notices a deal
is in trouble a week before the renewal date, not two months before, because nobody is
systematically reviewing activity gaps, champion turnover, or sentiment across every
account in their book. This is a retention/expansion GTM problem, distinct from
top-of-funnel lead qualification.

**What this agent does:** Takes deal metadata (ARR, stage, days since last activity,
named champion) plus recent notes (calls, emails, support tickets — anything already
sitting in a CRM or Gong-style tool) and returns:

- A risk level (Low/Medium/High/Critical) and numeric risk score
- A renewal probability estimate
- Champion health (Strong/Weak/Unknown/Missing) — explicitly flags "Missing" when a
  champion has left or gone silent, which is often the single biggest renewal risk
- The specific risk factors and any positive signals found in the notes
- One concrete action the CSM/AM should take this week

**Target user:** CSM, Account Manager, or a RevOps/CS Ops team building a renewal
risk dashboard.

**Why it matters for GTM:** Most "AI + GTM" demos focus entirely on acquisition
(lead scoring, outbound). Retention and expansion are where enterprise SaaS actually
makes or loses its NRR — and champion turnover is one of the most common, least
systematically-tracked renewal risks. Pairing this agent with the lead qualifier
demonstrates coverage of the full GTM motion, not just the flashy top-of-funnel part.

**What's mocked vs. real:**
- Mocked: CRM/call-transcript data (`sample_deals.py`) — in production this would pull
  from Salesforce/HubSpot fields plus Gong/email summaries.
- Real: the risk analysis, which calls Claude via structured outputs
  (`client.messages.parse`) to guarantee a validated JSON response.

**Metrics you'd track in production:** Lead time between a "Critical" flag and the
actual renewal decision (are we catching risk early enough to act?), save rate on
flagged deals vs. unflagged deals, CSM override/agreement rate with the risk level.

## Running it

```bash
pip install -r ../../requirements.txt
export ANTHROPIC_API_KEY=your-key-here
streamlit run app.py
```

Pick a sample deal from the sidebar, or paste your own deal notes.
