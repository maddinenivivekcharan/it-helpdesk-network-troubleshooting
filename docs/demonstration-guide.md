# Beginner demonstration guide

Use PowerShell in the repository root. With a normal Python install set
`$python = 'python'`. In this workspace, the tested portable interpreter is:

```powershell
$python = 'C:\VivekCharan\Projects\python-runtime\python.exe'
& $python scripts/run_lab.py --help
& $python scripts/run_network_diagnostics.py --help
```

1. Explain the project: fictional support workflow, read-only diagnostics,
   standard-library implementation, no company-system or tenant access.
2. Display safe guidance with
   `& $python scripts/run_network_diagnostics.py guidance`.
   Explain DHCP, gateway, DNS and Wi-Fi checks.
3. Optionally demonstrate **local only** diagnostics:
   `& $python scripts/run_network_diagnostics.py dns localhost` and
   `& $python scripts/run_network_diagnostics.py ping 127.0.0.1`.
   Explain why these results do not prove internet access. A blocked ping is
   a valid error demonstration, not a reason to disable security controls.
4. Create an isolated fictional ticket and capture its generated ID:

```powershell
$ticket = (& $python scripts/run_lab.py --store local-data/demo.json create 'SIMULATED: No internet' 'Training cable appears disconnected' --priority Medium) | ConvertFrom-Json
$id = $ticket.id
& $python scripts/run_lab.py --store local-data/demo.json view $id
& $python scripts/run_lab.py --store local-data/demo.json list --status Open
```

5. Add an evidence-based **simulated** note, start investigation, then demonstrate
   a validation failure. The failure should exit 2 and preserve the store:

```powershell
& $python scripts/run_lab.py --store local-data/demo.json update $id --note 'SIMULATED: observed missing link; cable inspection proposed' --status 'In Progress'
& $python scripts/run_lab.py --store local-data/demo.json update $id --status Resolved
```

6. Record a fictional resolution and close after simulated user confirmation:

```powershell
& $python scripts/run_lab.py --store local-data/demo.json update $id --status Resolved --resolution 'SIMULATED: cable connected with consent; original app retested successfully'
& $python scripts/run_lab.py --store local-data/demo.json update $id --status Closed
& $python scripts/run_lab.py --store local-data/demo.json list --status Closed
```

7. Search procedures: `& $python scripts/run_lab.py kb 'DNS resolution'` and
   `& $python scripts/run_lab.py kb 'account lockout'`. Explain escalation and
   why the lab never changes accounts. Open the matching simulated reports.
8. Run `& $python -m unittest discover -s tests -v`. Explain temporary storage,
   fake command runners and why offline tests are repeatable.
9. Discuss limitations and a next improvement. Distinguish this project from
   real employment, authorized enterprise administration and live CI evidence.

Every repeat creates a new ticket; no reset silently erases prior demo data.
Do not record hostname/IP output or private terminal content in screenshots.
