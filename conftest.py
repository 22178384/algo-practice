"""Pytest root conftest.

Its only job is to make the repo root importable so `from sort.merge_sort import
merge_sort` works. pytest inserts the directory of the topmost conftest.py into
sys.path, and since this file sits at the repo root, that's the root.

This matters more than it looks: without the root on sys.path, `import string`
resolves to the stdlib `string` module and `string/kmp.py` is unreachable.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
