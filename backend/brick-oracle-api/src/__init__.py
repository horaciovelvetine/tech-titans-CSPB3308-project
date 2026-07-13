"""Brick Oracle Flask API package.

Exposes the :func:`create_app` factory used by ``main.py`` and the test suite.
Startup wiring lives here: database initialization and the immutable catalog
seed both happen inside :func:`create_app` so that any entrypoint that
constructs the app (WSGI, dev server, tests) gets a fully-populated DB.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

from flask import Flask

from .config import Config
from .extensions import db


def create_app(config_overrides: Mapping[str, Any] | None = None) -> Flask:
    package_root = Path(__file__).resolve().parent
    backend_root = package_root.parents[1]
    default_instance_path = backend_root / "instance"

    app = Flask(
        __name__,
        instance_relative_config=True,
        instance_path=str(default_instance_path),
    )
    app.config.from_object(Config())
    if config_overrides:
        app.config.update(dict(config_overrides))

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    if app.config.get("SQLALCHEMY_DATABASE_URI") is None:
        db_path = Path(app.instance_path) / "brick_oracle.sqlite3"
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    db.init_app(app)

    # from .models import catalog as _catalog_models  # noqa: F401 - register models

    with app.app_context():
        db.create_all()

        if not app.config.get("SKIP_CATALOG_SEED"):
            from .catalog.seed import ensure_catalog_loaded

            ensure_catalog_loaded(app)

    return app


__all__ = ["create_app", "db"]
