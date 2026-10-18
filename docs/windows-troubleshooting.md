# Windows troubleshooting procedures

Use a personal lab device or a separately authorized endpoint. Start with the
reported symptom, save work, ask about impact and inspect before making changes.
Windows 10/11 labels can differ; use Start search to locate the named console.
Ordinary lab commands run without administrator rights; policy may restrict them.

## Read-only inspection

- Task Manager: Ctrl+Shift+Esc, inspect Processes and Performance. Observe CPU,
  memory and disk for a period rather than treating one spike as a fault.
  Do not end unknown system or security processes. Ending tasks can lose work.
- Device Manager: inspect a device's status and error code. Warning indicators
  need investigation, not an automatic driver replacement. Driver installation,
  disabling devices and rollback change state and may need admin approval.
- Settings -> Network & Internet: inspect adapter status, Wi-Fi signal and the
  expected network. Do not share SSIDs, MACs, addresses or host inventories.
- `ipconfig /all`: read adapter, DHCP, gateway and DNS configuration locally.
  This is inspection; its raw output may identify devices and must be redacted.
- `ping -n 2 127.0.0.1`: tests local ICMP response only. For an approved host,
  inspect both replies and errors; blocked ICMP does not prove a service is down.
- `tracert -d -h 8 -w 1000 127.0.0.1`: bounded manual route illustration to
  loopback; for another target obtain authorization first. Missing hop replies
  can be filtering. This program does not automate tracert.
- `nslookup localhost`: inspect a DNS-server answer. The system resolver can
  also use hosts/cache, so nslookup can differ from application resolution.
- Services (`services.msc`): inspect service state and description. Stopped may
  be expected. Do not start/stop/reconfigure services without approved ownership.
- Event Viewer (`eventvwr.msc`): inspect relevant Application/System events near
  the symptom time. Record sanitized event IDs and summaries, never whole logs.
  Security logs and some views may require approved administrative access.

## Manual state changes: never executed by this application

| Command/action | Effect | Prerequisite |
| --- | --- | --- |
| `ipconfig /release` | Releases DHCP IPv4 lease; can disconnect this endpoint and remote support | Explicit authorization and a recovery path; do not use casually on remote sessions |
| `ipconfig /renew` | Requests a DHCP lease; connectivity can be interrupted or renewal can fail | Authorized DHCP troubleshooting and local recovery plan |
| `ipconfig /flushdns` | Clears the DNS client resolver cache, including cached negative entries | Evidence of a relevant cache issue and permission; may need elevated prompt |
| Driver updates, service restart | Changes running system behavior; can disrupt work | Approved change process and owner, often admin rights |

The lease commands concern DHCP-configured adapters; they are not a fix for every
network failure. Permissions depend on OS and organizational policy. If access is
denied, stop and escalate rather than automatically elevating. Cache flushing
cannot repair a missing authoritative DNS record or a disconnected cable.

Command semantics references:
[Microsoft ipconfig](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig),
[Microsoft nslookup](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/nslookup),
[Microsoft TRACERT explanation](https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/trace-route-troubleshoot-tcp-ip-problems).
These sources support command interpretation; this lab intentionally automates
only inspection and bounded DNS/ping checks.

## Enterprise and other-platform awareness

- macOS: use System Settings -> Network, Activity Monitor and Console for basic
  inspection. The Python CLI supports hostname/DNS and ifconfig/ping command
  construction; macOS behavior has not been locally exercised here. Never assume
  Windows command flags or directory policies apply unchanged.
- Active Directory Domain Services: on-premises directory, domain membership,
  authentication and Group Policy. Account recovery and directory administration
  require a separately authorized domain, identity verification and privileges.
- Microsoft Entra ID: cloud identity and access, tenant policies and conditional
  access. It is distinct from AD DS; no tenant or identity APIs are integrated.
- Microsoft 365: licensed cloud applications including Outlook, Teams and
  OneDrive. Compare client symptoms and approved service-health information;
  administrator portal access requires authorization and suitable roles.
- VPNs: encrypted connectivity may provide internal routes and name resolution.
  Inspect status and errors; never install profiles or bypass access policy.
- Remote support: obtain consent, verify the support channel, explain actions
  and end sessions cleanly. Never ask for credentials or unattended access.
  No remote-control capability is implemented in this project.
- Endpoint protection: inspect approved security status; report alerts promptly.
  Never disable antivirus, exclusions or firewall rules as a troubleshooting fix.
- Patching: observe update status; schedule approved updates and restarts after
  saving work. Track compliance through the authorized endpoint management owner.
- ITSM: enterprise tools support assignment, SLAs, audit history, asset links and
  change/problem management. This CLI models only a small ticket lifecycle;
  it has no real service desk integration, SLA engine or enterprise audit trail.

All enterprise procedures above are conceptual training unless an organization
provides a specifically authorized environment. No real accounts were managed.
