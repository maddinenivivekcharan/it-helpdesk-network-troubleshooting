# Contributing

Use Python 3.10+ and keep runtime dependencies in the standard library.
Run `python -m unittest discover -s tests -v` from this repository root.
Add tests for behavior changes, with injected resolvers/command runners.
Never put real host inventories, personal information, credentials, raw logs,
or production incidents in fixtures. Mark every sample as simulated.
Keep all diagnostic subprocesses bounded, with argument lists and shell=False.
Do not add account changes, scans, firewall edits or automatic remediation.
Describe the problem, change, safety impact and actual validation in pull requests.
