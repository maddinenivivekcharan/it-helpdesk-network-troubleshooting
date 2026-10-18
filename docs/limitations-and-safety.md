# Limitations and safety

This is educational software for simulated tickets and safe local inspection.
No real employer incidents, certifications or production experience are claimed.
Do not scan external networks or connect to company systems for this demo.

No password reset, account unlock, configuration edits, lease renewal, cache
flush, firewall change, security disabling or remote support runs automatically.
Manual Windows state changes are described separately with disruption warnings.

DNS is resolved via the OS in a child Python process with a four-second limit.
This captures system resolver behavior, not DNS packet details or authoritative
record validation. Ping sends two requests with an eight-second process limit;
ICMP filtering and platform-dependent exit codes prevent a universal reachability
conclusion. Returned `ok` for command checks reflects exit status, not a guarantee
that the target or application works. Output is not parsed using English reply
phrases, which would fail on localized Windows installations.

Strict destinations accept ASCII DNS names and literal IPv4/IPv6. Unicode names,
IPv6 scope/zone IDs, URLs and command arguments are intentionally unsupported.
No port checks, traceroutes, scans, exploitation or external-service polling are
implemented. The package supports command selection for Windows/Linux/macOS;
only the host used in verification has actual local smoke-check evidence.
Missing tools, permission errors and timeouts are reported without escalation.

IP inspection may show sensitive device metadata on screen. No diagnostic output
is automatically stored; users must not paste it into tickets. Free-text fields
cannot reliably prevent accidental secret entry: only fictional content is
allowed. Stores are plaintext; there is no authentication, encryption, immutable
audit history, assignment system, SLA tracking or production incident integration.

Writes use a local exclusive lock and atomic replacement after validation.
This prevents overlapping cooperating writers and partial JSON replacement in
ordinary failures; it is not distributed locking or a disk-failure guarantee.
A crash can leave .lock/.tmp files, deliberately blocking writes until inspected.
Failed writes preserve the original store and may preserve a recovery temporary
file. Keep private backups; there is no automated repair/reset or file deletion.

Tests prove local behavior under mocks. They do not prove that an external
network, live tenant, Linux host, macOS device or CI environment works. Editable
packaging is optional; wheels need an explicit KB file path because external
JSON resources remain in the source checkout.
