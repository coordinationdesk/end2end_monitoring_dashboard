import json
import os

from maas_model.generator.jsongen import generate as generate_json

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

TPL1 = os.path.join(DATA_DIR, "sample1-simple_template.json")

TPL2 = os.path.join(DATA_DIR, "sample2-meta_template.json")

TPL3 = os.path.join(DATA_DIR, "bad-partition-field_template.json")

RAW_TPL = os.path.join(DATA_DIR, "raw-data-sample3_template.json")


def test_generate_json():

    generated_code = generate_json(TPL1, TPL2, RAW_TPL)

    d = json.loads(generated_code)

    assert "models" in d

    assert len(d["models"]) == 3

    assert d["models"][0] == {
        "index": "sample1-simple",
        "name": "Sample1Simple",
        "fields": [
            {"name": "kw_field", "type": "Keyword"},
            {"name": "int_field", "type": "Integer"},
            {"name": "date_field", "type": "Date"},
            {"name": "ingestionTime", "type": "Date"},
        ],
    }

    assert d["models"][1] == {
        "index": "sample2-meta",
        "name": "CustomNameDocument",
        "fields": [
            {"name": "kw_field", "type": "Keyword"},
            {"name": "int_field", "type": "Integer"},
            {"name": "mydate_field", "type": "Date"},
        ],
        "partition_field": "mydate_field",
        "partition_format": "%Y-%m",
    }

    assert d["models"][2] == {
        "index": "raw-data-sample3",
        "name": "Sample3",
        "fields": [
            {"name": "kw_field", "type": "Keyword"},
            {"name": "int_field", "type": "Integer"},
            {"name": "date_field", "type": "Date"},
        ],
    }
