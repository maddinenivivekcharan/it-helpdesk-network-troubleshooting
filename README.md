# IT Helpdesk & Network Troubleshooting Lab

A runnable Python CLI for practicing first-line IT support: safe diagnostics,
local JSON tickets, a searchable knowledge base and simulated incident reports.
Built for an undergraduate preparing to demonstrate IT Helpdesk Intern skills.

Repository: [maddinenivivekcharan/it-helpdesk-network-troubleshooting](https://github.com/maddinenivivekcharan/it-helpdesk-network-troubleshooting)
This link identifies the intended repository; local files have not been pushed.

## Problem and objectives

Beginners need a repeatable way to connect network symptoms, evidence, support
communication and escalation. This lab provides that practice without requiring
company systems or administrator access. Objectives are to distinguish network
layers, document investigations, manage ticket lifecycles and recognize when
an authorized specialist must take over.

## Features

- Hostname, bounded system DNS lookup, two-request ping and local IP inspection.
- Separate actual diagnostic output, interpretation and suggested next action.
- Six ticket categories, four priorities and four statuses; UUID-based IDs and
  UTC creation timestamps; notes, resolution validation and combined filters.
- JSON persistence with exclusive writer lock and atomic replacement. Invalid
  stores are rejected and preserved. No reset/delete/import command exists.
- Twelve searchable support procedures and three explicitly simulated incidents.
- Offline unittest coverage and a Windows/Linux GitHub Actions matrix.
- Standard-library runtime; no telemetry, web server, third-party service or
  automated account/network changes.

## Architecture and repository layout

CLI -> ticket service -> validated dataclass -> JSON store.
CLI -> knowledge-base search -> curated JSON procedures.
CLI -> diagnostics -> injected command runner or bounded DNS subprocess.

```text
.
|-- README.md, LICENSE, CONTRIBUTING.md, .gitignore
|-- pyproject.toml, requirements.txt, requirements-dev.txt
|-- src/helpdesk_lab/
|   |-- __init__.py, cli.py, models.py
|   |-- ticket_manager.py, network_diagnostics.py, knowledge_base.py
|-- scripts/run_lab.py, scripts/run_network_diagnostics.py
|-- data/sample_tickets.json, data/knowledge_base.json
|-- docs/
|   |-- project-overview.md, setup-guide.md, networking-fundamentals.md
|   |-- windows-troubleshooting.md, helpdesk-workflow.md, security-checklist.md
|   |-- interview-preparation.md, limitations-and-safety.md
|   |-- demonstration-guide.md, verification.md
|-- incident_reports/
|   |-- README.md, sample_no_internet.md
|   |-- sample_dns_failure.md, sample_account_lockout.md
|-- tests/
|   |-- test_models.py, test_ticket_manager.py, test_knowledge_base.py
|   |-- test_network_diagnostics.py, test_cli.py
|-- .github/workflows/python-tests.yml
```

Technology: Python 3.10+, argparse, dataclasses, pathlib, json, socket,
subprocess, uuid and unittest. JSON is suitable for this small training store;
it is not a replacement for an enterprise ITSM system.

## Windows PowerShell setup

Install Python 3.10+ from the official Python distribution and make `python`
available on PATH. Open PowerShell in the checkout root:

```powershell
cd C:\VivekCharan\Projects\it-helpdesk-network-troubleshooting
python --version
python scripts/run_lab.py --help
python scripts/run_network_diagnostics.py --help
```

No package installation is required for the script entry points or tests.
Optional development installation with a normal Python installation:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\helpdesk-lab.exe --help
```

Use editable installation for the console command: the knowledge-base default
points into this checkout. A standalone wheel does not bundle the external data;
use `kb --file PATH` in that case. See [setup guide](docs/setup-guide.md).

## Run the lab

Run from the repository root. `--store` is a global option and goes before the
subcommand. Default live store is `~/.helpdesk_lab/tickets.json` (outside Git).
Use a separate ignored demo store to keep examples separate from live work:

```powershell
python scripts/run_lab.py --store local-data/demo.json create "SIMULATED: No internet" "Training device has no link" --category Network --priority Medium
python scripts/run_lab.py --store local-data/demo.json list
python scripts/run_lab.py --store local-data/demo.json list --status Open --category Network
```

Copy the generated ID from the create/list output and set it below:

```powershell
$id = 'LAB-paste-the-generated-id-here'
python scripts/run_lab.py --store local-data/demo.json view $id
python scripts/run_lab.py --store local-data/demo.json update $id --note "SIMULATED: link inspected" --status "In Progress"
python scripts/run_lab.py --store local-data/demo.json update $id --status Resolved --resolution "SIMULATED: cable connected with consent; application retested"
python scripts/run_lab.py --store local-data/demo.json update $id --status Closed
python scripts/run_lab.py kb "DNS resolution"
python scripts/run_lab.py kb "account lockout"
```

Representative output fragment (illustrative, generated IDs/times vary):

```json
{"title": "SIMULATED: No internet", "priority": "Medium", "status": "Open"}
```

The actual CLI prints complete JSON records, including ID, creation time,
category, description, notes and resolution. Viewing and listing do not write.
Adding resolution alone does not mark a ticket resolved. Closing requires a
previous Resolved state; reopening clears the previous resolution.

## Diagnostics and interpretation

```powershell
python scripts/run_network_diagnostics.py guidance
python scripts/run_network_diagnostics.py hostname
python scripts/run_network_diagnostics.py dns localhost
python scripts/run_network_diagnostics.py ping 127.0.0.1
python scripts/run_network_diagnostics.py ip
```

Only target your own device or an explicitly authorized hostname/IP. Hostnames
are strict ASCII DNS names; URLs, spaces, command switches and IPv6 zone IDs are
rejected. No scans are implemented. `ip` output can contain identifiers: inspect
locally and never copy raw output into tickets or source control.

DNS success means the system resolver returned an address; it does not prove
internet or application access. A ping result retains the command exit code
and raw reply text. ICMP can be filtered; some Windows errors return exit zero,
so `ok` indicates command exit success, not independently verified reachability.
Always read the actual output and test the original application.

DNS subprocess timeout: 4 seconds. Ping/configuration process timeout: 8 seconds.
Exit codes: 0 successful command execution, 1 unsuccessful/unsupported diagnostic,
2 invalid input or storage error. These codes do not certify service availability.

Troubleshooting examples:

- No link: check a lab cable and network status before investigating DNS.
- Valid local address but name lookup fails: compare expected DNS results and
  escalate repeated/shared failures to the resolver owner.
- Locked account: stop repeated attempts, follow identity verification policy
  and escalate; this program cannot unlock or reset an account.

## Tests and validation

```powershell
python -m unittest discover -s tests -v
```

Tests use temporary directories, fake resolvers and injected command runners;
they do not require a network, admin rights or a DNS server. See
[actual verification record](docs/verification.md) for executed commands and
results. The workflow is configured for Python 3.10/3.13 on Windows/Linux;
configured CI is not a claim that a GitHub run has occurred.

## Safety and limitations

Use fictional training descriptions only: no passwords, tokens, names, account
identifiers or sensitive logs. Free-text fields are not a reliable secret
scanner. Files are plaintext, not encrypted, authenticated or access-controlled
by the application. Local filesystem permissions are the user's responsibility.
No automatic resets, unlocks, firewall changes, lease renewals, cache flushing,
security disabling or remote support sessions are performed.

Windows 10/11 commands are supported in code; only the actual local environment
listed in verification was exercised. Linux needs `ip`/`ping`; macOS needs
`ifconfig`/`ping`. Missing tools and denied access become diagnostic errors.
Concurrent writers are serialized with a lock; stale recovery files require
manual investigation. Atomic replacement reduces partial-write risk but is not
a backup or a guarantee against disk failure. See
[limitations](docs/limitations-and-safety.md) and
[Windows procedures](docs/windows-troubleshooting.md).

## Learning outcomes and future work

Practice separating facts from hypotheses, DHCP/DNS/gateway reasoning, ticket
prioritization, clear notes, validation, error handling and unit-test isolation.
Enterprise Active Directory, Entra ID and Microsoft 365 actions remain conceptual
without a separately authorized environment. This lab does not demonstrate
employment, certifications or production administration experience.

Possible future improvements: packaged knowledge-base resources, SQLite storage,
an audit-event history, localization-aware ping analysis and accessible UI.

Start with the [demonstration guide](docs/demonstration-guide.md), then review
[15 interview questions and justified resume bullets](docs/interview-preparation.md).
