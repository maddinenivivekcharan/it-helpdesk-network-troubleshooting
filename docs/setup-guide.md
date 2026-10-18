# Setup guide

1. Install a normal Python 3.10+ distribution; confirm `python --version`.
   If Windows opens the Store instead, choose the installed interpreter or fix
   the Python app execution alias/PATH. `py -3` may be available on other machines.
2. Open PowerShell in the checkout root. Scripts locate src/ automatically.
3. Run `python scripts/run_lab.py --help` and
   `python scripts/run_network_diagnostics.py --help`.
4. Run `python -m unittest discover -s tests -v`.
5. Create a fictional ticket with `--store local-data/demo.json` before `create`.
   Do not point --store at either fixture in data/; live data and samples differ.

No runtime pip dependencies and no administrator privileges are needed.
requirements.txt and requirements-dev.txt deliberately contain comments only.
Optional packaging uses setuptools and may require downloading build tooling;
it is unnecessary for running from source. Use editable install as shown in the
README; wheels do not include the repository-level knowledge-base data. Supply
`kb --file` explicitly if using a wheel.

## Runtime used for local validation

This workspace initially had no usable Python or Git executable. An official
Python 3.13.7 embeddable runtime was downloaded, with approval, to the sibling
`../python-runtime/` directory, outside the project. In this workspace use:

```powershell
$python = 'C:\VivekCharan\Projects\python-runtime\python.exe'
& $python scripts/run_lab.py --help
& $python -m unittest discover -s tests -v
```

The embeddable runtime is only a local validation aid, has no pip/venv tooling,
and is not committed as a project dependency. A normal Python distribution is
recommended for development. Network commands can be absent or restricted on
some hosts; the program prints the actual error rather than changing settings.

## Recovering storage safely

If JSON is invalid, the program refuses to replace it. Copy the damaged store
to a private backup before investigating; do not paste it into public issues.
A .lock file can mean an active writer. Confirm all lab processes have stopped
before treating it as stale. A .tmp file can contain a pending write after an
interruption. Compare it to the preserved store and keep a private backup of
both before manually recovering. Do not blindly remove either recovery file.
There is no automated reset operation.

## Git publication

No repository or remote was present at inspection and Git is unavailable here.
Install Git, then review all generated files before initializing/publishing.
If the GitHub repository already contains history, first clone it into a separate
folder, inspect its README and changes, and merge these files deliberately;
do not initialize an unrelated history over that checkout. See verification.md
for exact proposed commands. Push only after explicit review/confirmation.
