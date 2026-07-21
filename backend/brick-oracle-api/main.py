"""WSGI entrypoint for the Brick Oracle Flask API."""

from typing import Any

from src import create_app
from src.catalog.repository import table_row_counts

app = create_app()


@app.route("/")
def index() -> dict[str, Any]:
    return {
        "message": "Brick Oracle API Route: '/' ",
        "counts": table_row_counts(),
        "status": 200,
    }
