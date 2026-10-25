#!/usr/bin/env python3
"""Dev-mode wrapper so `python scripts/install.py ...` keeps working from a checkout
without installing the package. Prefer `pip install .` and the `ai-engineering install`
console command outside this repo."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ai_engineering.installer import main

if __name__ == '__main__':
    main()
