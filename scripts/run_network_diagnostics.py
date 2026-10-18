"""Run diagnostics from a checkout without installation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from helpdesk_lab.cli import main

if __name__ == '__main__':
    raise SystemExit(main(['diagnose', *sys.argv[1:]]))
