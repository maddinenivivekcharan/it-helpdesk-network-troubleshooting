# Interview preparation

These are plausible practice questions for a FinacPlus IT Helpdesk Intern
interview, not verified employer questions. Answers describe this implementation
and appropriate support boundaries; they do not claim production experience.

1. **What did you build?** A Python CLI that combines safe network inspection,
   JSON ticket management, twelve local procedures and simulated incident
   documentation. It has no company-system integration.
2. **How would you investigate no internet access?** Clarify scope and onset;
   inspect physical/Wi-Fi link, address and gateway, then DNS and the original
   application. Use consent and stop before unauthorized changes.
3. **How do DNS and DHCP differ?** DNS resolves names to records. DHCP commonly
   leases address configuration. Successful DNS does not prove a service works.
4. **What does 169.254.x.x mean?** IPv4 link-local, often seen without a DHCP
   lease. Check whether DHCP was expected; IPv6 may still work.
5. **Does failed ping prove the internet is down?** No. ICMP can be blocked,
   DNS may be a separate issue, and application protocols can behave differently.
   Read replies/errors; some Windows failures return zero. This lab preserves
   raw output and does not treat command success as verified service health.
6. **How do you prevent command injection?** Validate a single hostname/IP,
   construct a fixed argument list, use shell=False, restrict ping to two
   requests and enforce process timeouts. Never run free-form shell text.
7. **How are tickets identified and stored?** A dataclass generates a UUID-based
   LAB ID and timezone-aware UTC creation timestamp. Validated records serialize
   to a local JSON list separate from the read-only sample fixtures.
8. **How do you prevent accidental data loss?** Reject invalid stores before
   writing, take an exclusive writer lock, write/fsync a new temporary file and
   atomically replace the store. Failures preserve the original; stale recovery
   files need manual review. This does not replace backups or disk-failure recovery.
9. **What are your status rules?** Open/In Progress represent active work.
   Resolved and Closed require nonempty resolution details. Closing requires
   Resolved first; reopening clears the old resolution. Notes remain available.
10. **How would you prioritize?** Use impact and urgency, not the user's title.
    A single blocked training device might be Medium; shared service failure
    could be High. An employer's actual priority/SLA matrix takes precedence.
11. **What do you do for account lockout?** Stop repeated attempts, record a
    sanitized error, follow approved identity verification and escalate to the
    authorized identity team. This lab never unlocks or resets an account.
12. **How do you handle phishing?** Do not click, open or reply; report through
    approved security channels. If credentials were entered or an attachment
    executed, escalate immediately and follow security containment instructions.
13. **How were diagnostics tested without a network?** Inject fake command
    runners and DNS resolvers; assert exact arguments, timeout behavior, exit
    handling and interpretation. Temporary directories isolate ticket tests.
    Mock success is not evidence that any external network is available.
14. **What is AD versus Entra ID, and have you administered them here?** AD DS
    is an on-premises domain directory; Entra ID is cloud identity/access. Both
    require separately authorized environments and roles. This lab documents
    concepts and escalation only; it has no directory administration integration.
15. **What would you improve?** Bundle KB resources for wheel installs, use
    SQLite for larger workloads, add audit events and improve localization-aware
    diagnostic analysis. Production use would also need an access/security design.

## Resume bullets justified by the implementation

- Built a standard-library Python helpdesk CLI with validated ticket creation,
  lifecycle updates, filtering, investigation notes and local JSON persistence.
- Implemented bounded network diagnostics with validated subprocess arguments,
  explicit error handling and offline tests using injected system interfaces.
- Created twelve searchable troubleshooting procedures and three clearly labeled
  simulated incident reports covering network and account-access scenarios.
- Added 35 automated unittest tests and a Windows/Linux GitHub Actions test
  workflow; the local Python 3.13.7 suite passed during implementation.

Do not claim employment at FinacPlus, real incident resolution, production AD or
Microsoft 365 administration, certifications, CI success or measured business
impact from this educational project. State the actual test count from the latest
verification record if you later add tests.
