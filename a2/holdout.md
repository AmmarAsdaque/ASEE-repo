# Holdout check

## What it checks
That the 1-99 rule also applies when the request uses camelCase JSON keys
("squadNumber"), which the API accepts through its alias generator: -5 and 100
must be rejected with 422 and not saved, and 99 must be accepted. All my visible
tests send snake_case "squad_number", and none of them uses a negative number.

## Where it lived
~/holdouts/a2/test_holdout.py, outside the repository. Not mentioned in any
prompt; not present in runs/a2-implement.md. Run only after the visible tests and
both mutation runs were done.

## The check
```python
"""Holdout for A2: the range rule must also apply to camelCase JSON keys."""
from fastapi.testclient import TestClient

from main import app

PLAYER = {
    "firstName": "Holdout",
    "lastName": "Player",
    "position": "Goalkeeper",
}


def test_camelcase_squad_number_out_of_range_rejected_and_in_range_accepted():
    with TestClient(app) as client:
        try:
            for bad in (-5, 100):
                response = client.post("/players/", json={**PLAYER, "squadNumber": bad})
                assert response.status_code == 422
                assert client.get(f"/players/squadnumber/{bad}").status_code == 404
            ok = client.post("/players/", json={**PLAYER, "squadNumber": 99})
            assert ok.status_code == 201
        finally:
            for n in (-5, 100, 99):
                client.delete(f"/players/squadnumber/{n}")
```

## Result
PASSED on first run, 2026-11-01.
```text
============================= test session starts ==============================
platform linux -- Python 3.13.3, pytest-9.1.1, pluggy-1.6.0 -- /mnt/d/ASEE-Repo/ASEE-repo/.venv/bin/python
rootdir: /mnt/d/ASEE-Repo/ASEE-repo
configfile: pyproject.toml
plugins: anyio-4.14.2, cov-7.1.0
collecting ... collected 1 item

::test_camelcase_squad_number_out_of_range_rejected_and_in_range_accepted PASSED [100%]

============================== 1 passed in 2.88s ===============================
```

## What I did
Nothing needed fixing. The validator runs on the field itself, so it applies to
both the snake_case name and the camelCase alias.
