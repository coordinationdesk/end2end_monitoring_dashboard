from opensearchpy import Keyword
import pytest
from maas_model import MAASDocument


def test_sort():
    assert MAASDocument._get_sort() is None


class NonePartitionDocument(MAASDocument):
    _PARTITION_FIELD = "foo"

    foo = Keyword()

    class Index:
        name = "bar"


class ADocument(MAASDocument):
    _PARTITION_FIELD = "foo"

    foo = Keyword()

    zap = Keyword()

    bar = Keyword()

    class Index:
        name = "bar"


class BDocument(MAASDocument):
    _PARTITION_FIELD = "foo"

    foo = Keyword()

    zap = Keyword()

    not_common = Keyword()

    class Index:
        name = "bar"


def test_copy_common():
    a_doc = ADocument(foo="zip", zap="gz", bar="plop")
    b_doc = BDocument(foo="tar", zap="hz", not_common="unique")

    a_doc.fill_common_fields(b_doc)
    assert a_doc.to_dict() == {"foo": "tar", "zap": "hz", "bar": "plop"}

    a_doc = ADocument(foo="zip", zap="gz", bar="plop")
    a_doc.fill_common_fields(b_doc, include=("foo",))
    assert a_doc.to_dict() == {"foo": "tar", "zap": "gz", "bar": "plop"}

    a_doc = ADocument(foo="zip", zap="gz", bar="plop")
    a_doc.fill_common_fields(b_doc, exclude=("foo",))
    assert a_doc.to_dict() == {"foo": "zip", "zap": "hz", "bar": "plop"}
