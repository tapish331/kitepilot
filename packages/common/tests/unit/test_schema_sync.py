from __future__ import annotations
import json
from kitepilot_common import schema_json


def test_schema_matches_published_file():
    with open("config/config.schema.json", "r", encoding="utf-8") as f:
        published = json.load(f)
    assert published == schema_json()
