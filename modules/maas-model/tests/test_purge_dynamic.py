import os

from maas_model.generator.pygen import generate as generate_python


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

TPL1 = os.path.join(DATA_DIR, "sample1-simple_template.json")

TPL2 = os.path.join(DATA_DIR, "sample1-complex_template.json")

TPL_LIST = os.path.join(DATA_DIR, "object-list_template.json")


def test_purge():
    generated_code = generate_python(TPL1)

    # execute the generated Python code
    exec(generated_code, globals())

    Sample1Simple = globals()["Sample1Simple"]

    doc = Sample1Simple()

    doc.kw_field = "test string"

    doc.int_field = 42

    # add a dynamic field
    doc.dynamic_field = "dynamic value"

    assert doc.to_dict() == {
        "kw_field": "test string",
        "int_field": 42,
        "dynamic_field": "dynamic value",
    }

    doc.purge_dynamic_fields()

    # check dynamic field has disappeared
    assert doc.to_dict() == {
        "kw_field": "test string",
        "int_field": 42,
    }


def test_purge_inner_doc():
    generated_code = generate_python(TPL2)

    # execute the generated Python code
    exec(generated_code, globals())

    Sample1Complex = globals()["Sample1Complex"]

    doc = Sample1Complex()
    doc.kw_field = "test string"

    # add a root dynamic field
    doc.dynamic_field = "dynamic value"

    doc.metadata.updateTime = "1977-01-23T20:15:23.000Z"
    # add a first level dynamic field
    doc.metadata.dynamic_field = "first level dynamic value"

    doc.properties.product_class = "SomeClass"
    doc.properties.metadata.updateTime = "2023-02-14T12:01:23.000Z"
    # add a second level dynamic field
    doc.properties.metadata.dynamic_field = "second level dynamic value"

    doc.full_clean()

    # dynamic fields appear
    assert doc.to_dict() == {
        "kw_field": "test string",
        "dynamic_field": "dynamic value",
        "metadata": {
            "updateTime": "1977-01-23T20:15:23.000Z",
            "dynamic_field": "first level dynamic value",
        },
        "properties": {
            "product_class": "SomeClass",
            "metadata": {
                "updateTime": "2023-02-14T12:01:23.000Z",
                "dynamic_field": "second level dynamic value",
            },
        },
    }

    # purge time !
    doc.purge_dynamic_fields()

    # dynamic fields disappear
    assert doc.to_dict() == {
        "kw_field": "test string",
        "metadata": {
            "updateTime": "1977-01-23T20:15:23.000Z",
        },
        "properties": {
            "product_class": "SomeClass",
            "metadata": {
                "updateTime": "2023-02-14T12:01:23.000Z",
            },
        },
    }


def test_purge_object_list_doc():
    generated_code = generate_python(TPL_LIST)

    # execute the generated Python code
    exec(generated_code, globals())

    ObjectList = globals()["ObjectList"]

    doc = ObjectList()
    doc.missing_periods = [
        {
            "product_type": "IW_RAW__0S",
            "sensing_start_date": "2022-07-04T16:27:09.000Z",
            "sensing_end_date": "2022-07-04T16:28:20.000Z",
            "duration": 71000000,
            "dynamic": "field",
        }
    ]

    doc.dynamic = "field"

    doc.full_clean()

    # dynamic fields appear
    assert doc.to_dict() == {
        "missing_periods": [
            {
                "product_type": "IW_RAW__0S",
                "sensing_start_date": "2022-07-04T16:27:09.000Z",
                "sensing_end_date": "2022-07-04T16:28:20.000Z",
                "duration": 71000000,
                "dynamic": "field",
            }
        ],
        "dynamic": "field",
    }

    # purge time !
    doc.purge_dynamic_fields()

    # dynamic fields disappear
    assert doc.to_dict() == {
        "missing_periods": [
            {
                "product_type": "IW_RAW__0S",
                "sensing_start_date": "2022-07-04T16:27:09.000Z",
                "sensing_end_date": "2022-07-04T16:28:20.000Z",
                "duration": 71000000,
            }
        ]
    }
