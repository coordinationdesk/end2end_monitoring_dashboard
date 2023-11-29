import datetime
import os


import pytest

from maas_model.generator.meta import FieldMeta, ModelClassMeta

from maas_model.generator.pygen import generate as generate_python


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

TPL1 = os.path.join(DATA_DIR, "sample1-simple_template.json")

TPL2 = os.path.join(DATA_DIR, "sample2-meta_template.json")

TPL3 = os.path.join(DATA_DIR, "bad-partition-field_template.json")

TPL4 = os.path.join(DATA_DIR, "sample1-complex_template.json")

RAW_TPL = os.path.join(DATA_DIR, "raw-data-sample3_template.json")


def test_wrong_filename():
    with pytest.raises(ValueError):
        ModelClassMeta("somefile.json")


def test_wrong_partition_field():
    meta = ModelClassMeta(TPL3)

    with pytest.raises(ValueError):
        meta.load()


def test_read_sample1():
    meta = ModelClassMeta(TPL1)

    meta.load()

    assert meta.index_name == "sample1-simple"

    assert meta.class_name == "Sample1Simple"

    assert meta.es_types == {"Keyword", "Integer"}

    assert meta.partition_field is None

    assert meta.partition_format is None

    assert len(meta.fields) == 4

    f1, f2, f3, _ = meta.fields

    assert f1.name == "kw_field"
    assert f1.type_name == "Keyword"

    assert f2.name == "int_field"
    assert f2.type_name == "Integer"

    assert f3.name == "date_field"
    assert f3.type_name == "Date"


def test_read_sample2():
    meta = ModelClassMeta(TPL2)

    meta.load()

    assert meta.index_name == "sample2-meta"

    assert meta.class_name == "CustomNameDocument"

    assert meta.partition_field == "mydate_field"

    assert meta.partition_format == "%Y-%m"


def test_read_raw():
    meta = ModelClassMeta(RAW_TPL)

    assert meta.index_name == "raw-data-sample3"

    assert meta.class_name == "Sample3"


def test_generate_python_samples():
    generated_code = generate_python(TPL1, TPL2, TPL4)

    # execute the generated Python code
    exec(generated_code, globals())

    Sample1Simple = globals()["Sample1Simple"]

    assert Sample1Simple.Index.name == "sample1-simple"

    assert len(Sample1Simple._PARTITION_FIELD) == 0

    assert Sample1Simple._PARTITION_FIELD_FORMAT == "%Y"

    # test generic partition field
    inst = Sample1Simple(
        kw_field="some_keyword",
        int_field=42,
        mydate_field=datetime.datetime(2020, 6, 21),
    )

    assert inst.partition_index_name == "sample1-simple"

    CustomNameDocument = globals()["CustomNameDocument"]

    # test custom partition field
    inst2 = CustomNameDocument(
        kw_field="some_keyword",
        int_field=42,
        mydate_field=datetime.datetime(2020, 6, 21),
    )

    assert inst2.partition_index_name == "sample2-meta-2020-06"

    assert globals()["Sample1Complex"]
    assert globals()["Sample1ComplexMetadata"]
    assert globals()["Sample1ComplexProperties"]
    assert globals()["Sample1ComplexPropertiesMetadata"]

    Sample1complex = globals()["Sample1Complex"]

    assert Sample1complex.Index.name == "sample1-complex"


def test_duplicated():
    with pytest.raises(ValueError):
        generate_python(TPL1, TPL1)


def test_read_sample_complex():
    meta = ModelClassMeta(TPL4)

    meta.load()

    assert meta.index_name == "sample1-complex"

    assert meta.class_name == "Sample1Complex"

    assert meta.es_types == {"Keyword", "Integer", "Object", "GeoShape"}

    assert meta.partition_field is None

    assert meta.partition_format is None

    assert len(meta.fields) == 7

    f1, _, _, _, f5, f6, _ = meta.fields

    assert isinstance(f1, FieldMeta)
    assert f1.name == "metadata"
    assert f1.type_name == "Object"
    assert f1.properties

    assert isinstance(f5, FieldMeta)
    assert f5.name == "properties"
    assert f5.type_name == "Object"
    assert len(f5.properties) == 4

    metadata_field = f5.properties[1]
    assert isinstance(metadata_field, FieldMeta)
    assert metadata_field.type_name == "Object"

    footprint_field = f5.properties[3]
    assert isinstance(footprint_field, FieldMeta)
    assert footprint_field.type_name == "GeoShape"

    assert isinstance(f6, FieldMeta)
    assert f6.name == "footprint"
    assert f6.type_name == "GeoShape"
