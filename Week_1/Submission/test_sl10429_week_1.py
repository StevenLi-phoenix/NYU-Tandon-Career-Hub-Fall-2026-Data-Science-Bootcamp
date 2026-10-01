"""Checks for the Week 1 take-home notebook: runs clean and every exercise has the expected output."""
import json
import re
from pathlib import Path

import pytest

NB_PATH = Path(__file__).with_name("sl10429_week_1.ipynb")


@pytest.fixture(scope="module")
def cells() -> list[dict]:
    return json.loads(NB_PATH.read_text(encoding="utf-8"))["cells"]


def text_output(cell: dict) -> str:
    return "".join("".join(o.get("text", "")) for o in cell.get("outputs", []))


def answer_after(cells: list[dict], number: int) -> dict:
    for i, cell in enumerate(cells):
        if cell["cell_type"] == "markdown" and "".join(cell["source"]).startswith(f"## Exercise {number}: "):
            nxt = cells[i + 1]
            assert nxt["cell_type"] == "code", f"Exercise {number} heading is not followed by code"
            return nxt
    raise AssertionError(f"Exercise {number} heading missing")


def test_header_cell(cells):
    first = "".join(cells[0]["source"])
    assert cells[0]["cell_type"] == "markdown"
    assert "**NetID:** sl10429" in first and "**Section:** 2" in first


def test_runs_without_errors(cells):
    code = [c for c in cells if c["cell_type"] == "code"]
    assert all(c["execution_count"] is not None for c in code), "notebook not fully executed"
    assert not [o for c in code for o in c["outputs"] if o["output_type"] == "error"]


@pytest.mark.parametrize("number, pattern", [
    (1, r"6\.25 <class 'float'>"),
    (2, r"20 <class 'int'>"),
    (3, r"'' False"),
    (4, r"False <class 'bool'>"),
    (5, r"Unique skills: 22"),
    (6, r"Distinct words: 52"),
    (7, r"\{'1': 5\.0, '2': 4\.86\}"),
])
def test_exercise_output(cells, number, pattern):
    assert re.search(pattern, text_output(answer_after(cells, number)))
