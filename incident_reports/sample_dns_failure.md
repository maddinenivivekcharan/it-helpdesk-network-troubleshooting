# SIMULATED TRAINING EXAMPLE: DNS resolution failure

Ticket: SIM-002. Fictional scenario; no commands in this report were actually run.
Impact: several training devices cannot open an approved internal lab service.
Priority: High due to shared service impact; no claim about a real SLA.

Simulated observations: physical links and expected local configuration appear
normal; the service hostname lookup times out on multiple devices. This does
not establish the exact root cause or prove all internet access is unavailable.
Simulated investigation: confirm the typed name and scope, compare OS resolution
and an approved nslookup check, inspect configured resolver locally, record only
redacted summaries. No alternative DNS server or firewall change is attempted.
Possible causes: resolver unavailability, route/policy problem or a service-side
DNS issue. These are hypotheses pending authorized network investigation.
Resolution: not yet established; no fabricated recovery is recorded.
Final status: In Progress. Escalation: DNS/network owner receives the simulated
scope, timing, sanitized error type and expected service name via a safe channel.
Learning: a referral is not a fix, and lookup failure is not proof of cable loss.
