import os
import datetime

import pytest


from maas_model.generator.pygen import generate as generate_python

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

COMPLEXTE_RAW_TPL = os.path.join(DATA_DIR, "complexe-partition-field_template.json")

NO_PARTIONNING_RAW_TPL = os.path.join(DATA_DIR, "no-partition-just-index_template.json")

SIMPLE_PARTIONNING_RAW_TPL = os.path.join(DATA_DIR, "simple-index_template.json")


def test_generate_python_no_partition():
    generated_code = generate_python(NO_PARTIONNING_RAW_TPL)

    # execute the generated Python code
    exec(generated_code, globals())

    NoPartition = globals()["NoPartitionJustIndex"]

    assert NoPartition.Index.name == "no-partition-just-index"

    assert len(NoPartition._PARTITION_FIELD) == 0

    assert NoPartition._PARTITION_FIELD_FORMAT == "%Y"

    inst = NoPartition(
        kw_field="some_keyword",
        int_field=42,
        date_field=datetime.datetime(2020, 6, 21),
    )

    assert inst.partition_index_name == "no-partition-just-index"

    assert inst.has_partition_field_value is True

    # Patch to try limit case behaviour
    NoPartition._PARTITION_FIELD = None
    NoPartition._PARTITION_FIELD_FORMAT = None

    inst2 = NoPartition(
        kw_field="some_keyword",
        int_field=42,
        date_field=datetime.datetime(2020, 6, 21),
    )

    assert inst2._PARTITION_FIELD is None
    assert inst2._PARTITION_FIELD_FORMAT is None

    assert inst2.partition_field_value is None
    assert inst2.partition_index_name == "no-partition-just-index"

    inst2._PARTITION_FIELD = 1
    with pytest.raises(TypeError):
        inst2.partition_field_value

    with pytest.raises(TypeError):
        inst2.has_partition_field_value


def test_generate_python_simple_partition():
    generated_code = generate_python(SIMPLE_PARTIONNING_RAW_TPL)

    # execute the generated Python code
    exec(generated_code, globals())

    SimpleIndex = globals()["SimpleIndex"]

    inst = SimpleIndex(
        kw_field="some_keyword",
        int_field=42,
        date_field=datetime.datetime(2020, 6, 21),
    )
    assert inst.has_partition_field_value is True

    assert inst.partition_index_name == "simple-index-06"


def test_generate_python_complexe_partition():
    generated_code = generate_python(COMPLEXTE_RAW_TPL)

    # execute the generated Python code
    exec(generated_code, globals())

    ComplexePartitionField = globals()["ComplexePartitionField"]

    assert ComplexePartitionField.Index.name == "complexe-partition-field"

    assert len(ComplexePartitionField._PARTITION_FIELD) == 3

    assert (
        ComplexePartitionField._PARTITION_FIELD_FORMAT
        == "{kw_field}-{int_field:03}-{date_field:%Y-%m}"
    )

    # test generic partition field
    inst = ComplexePartitionField(
        kw_field="some_keyword",
        int_field=42,
        date_field=datetime.datetime(2020, 6, 21),
    )

    assert (
        inst.partition_index_name == "complexe-partition-field-some_keyword-042-2020-06"
    )

    # test custom partition field
    inst2 = ComplexePartitionField(
        kw_field="some_keyword",
        int_field=None,
        mydate_field=datetime.datetime(2020, 6, 21),
    )

    # this should throw error
    with pytest.raises(TypeError):
        inst2.partition_index_name

    assert inst2.has_partition_field_value is False
