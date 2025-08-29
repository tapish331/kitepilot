from __future__ import annotations

import contextlib
import os

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect
from testcontainers.postgres import PostgresContainer  # type: ignore[import-untyped]

ALEMBIC_INI = os.path.join(os.path.dirname(__file__), "..", "..", "alembic.ini")


@contextlib.contextmanager
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as pg:
        url = pg.get_connection_url()
        yield url


def run_alembic(url: str, cmd: str) -> None:
    cfg = Config(ALEMBIC_INI)
    cfg.set_main_option("sqlalchemy.url", url)
    if cmd == "up":
        command.upgrade(cfg, "head")
    elif cmd == "down":
        command.downgrade(cfg, "base")
    else:
        raise ValueError(cmd)


def test_upgrade_and_downgrade_cycle():
    os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"
    with postgres_url() as url:
        run_alembic(url, "up")
        engine = create_engine(url)
        insp = inspect(engine)
        tables = set(insp.get_table_names())
        assert {"instrument", "order", "fill", "position", "run", "auditevent"}.issubset(tables)

        run_alembic(url, "down")
        insp = inspect(engine)
        tables_after = set(insp.get_table_names())
        assert "instrument" not in tables_after
