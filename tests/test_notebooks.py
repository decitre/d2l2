"""Every notebook in content/ runs in CPython without errors, warnings or other stderr output.

    uv run --group test pytest tests/test_notebooks.py

A fast check before the browser smoke test; it does not show that a notebook runs in JupyterLite.
"""

from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

NOTEBOOKS = sorted((Path(__file__).parent.parent / "content").rglob("*.ipynb"))


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.stem)
def test_notebook_runs(path):
    nb = nbformat.read(path, as_version=4)
    NotebookClient(nb, timeout=120, kernel_name="python3").execute()
    stderr = [o["text"] for c in nb.cells if c.cell_type == "code" for o in c.outputs if o.get("name") == "stderr"]
    assert not stderr
