"""Structural test: route handlers must not touch the database layer.

Routes handle HTTP only and call services/player_service.py. Only the service
layer may import the table model (schemas/) or build and run SQL queries.
"""

import ast
from pathlib import Path

ROUTES = Path(__file__).parent.parent / "routes"
FORBIDDEN_MODULES = ("schemas", "sqlite3", "aiosqlite", "sqlalchemy")
ALLOWED_MODULES = ("sqlalchemy.ext.asyncio",)  # AsyncSession type for Depends()
FORBIDDEN_CALLS = {"execute", "scalars", "commit", "rollback", "flush", "refresh"}


def problems_in(path):
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in ast.walk(tree):
        modules = []
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules = [node.module]
        for module in modules:
            if module.startswith(FORBIDDEN_MODULES) and not module.startswith(
                ALLOWED_MODULES
            ):
                yield f"{path.name}:{node.lineno} imports {module}"
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in FORBIDDEN_CALLS
        ):
            yield f"{path.name}:{node.lineno} calls .{node.func.attr}()"


def test_routes_do_not_touch_the_database_layer():
    problems = [p for path in sorted(ROUTES.glob("*.py")) for p in problems_in(path)]
    assert not problems, (
        "ARCHITECTURE RULE: routes/ must not import the table model or SQL tools, "
        "and must not run queries.\n"
        + "\n".join(problems)
        + "\nHOW TO FIX: move the query into an async function in "
        "services/player_service.py (add one if it does not exist yet, e.g. "
        "retrieve_<what>_async(async_session)) and call it from the route. "
        "Do not delete or edit this test. See AGENTS.md, section 'Boundaries'."
    )
