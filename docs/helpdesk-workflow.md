# Helpdesk workflow

1. Intake: record a fictional symptom and impact, onset and scope. Do not collect
   names, usernames, credentials, tokens or raw logs in this training tool.
2. Categorize: Network, Hardware, Software, Account Access, Microsoft 365 or
   Security. Choose the team best suited to investigate, rather than guessing
   the root cause from the category.
3. Prioritize using impact and urgency. Low: minor inconvenience with workaround;
   Medium: one simulated user blocked; High: a group/service significantly
   affected; Critical: broad severe outage or urgent security impact. These are
   training examples, not any employer's SLA policy.
4. Investigate: Open -> In Progress, ask clarifying questions, use safe checks,
   add notes separating observations from hypotheses and next steps.
5. Resolve: supply a meaningful resolution and verify the original symptom.
   `--status Resolved --resolution "..."` is one atomic update. Documentation
   alone does not cause a real network or account change.
6. Close: after simulated user validation, move Resolved -> Closed. A direct
   Open -> Closed move is rejected. Reopening to Open/In Progress clears the
   previous resolution; earlier notes remain. No append-only status audit exists.
7. Escalate when privileges, shared infrastructure, security, data risk or skill
   boundaries require it. Keep an escalated unresolved ticket In Progress and
   record the owner and reason in notes; do not mark resolved just for referral.

A useful note: time/context, redacted observation, hypothesis, action taken with
consent, result, next owner. Example: 'SIMULATED: Wi-Fi associated, DNS lookup
fails for the approved test name; shared symptom reported; escalated to DNS owner.'
Avoid 'fixed network' without a verifiable retest and a specific action.

There are no automated assignments, notifications, deletion or reset functions.
Fixture tickets are readable via --store for exploration but should never be
used as the write target. Create a separate demo store for demonstrations.
