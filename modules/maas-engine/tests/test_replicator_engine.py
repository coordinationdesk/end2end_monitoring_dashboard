from unittest import mock

import pytest

from opensearchpy import Keyword, Long


from maas_model import MAASDocument, MAASRawDocument

from maas_engine.engine.replicate import ReplicatorEngine


class MAASTestRawDocument(MAASRawDocument):

    kw_field = Keyword()

    long_field = Long()


class MAASTestConsolidatedDocument(MAASDocument):

    kw_field = Keyword()

    long_field = Long()


def test_replicator_engine_consolidate():

    with mock.patch.object(
        ReplicatorEngine,
        "get_model",
        new=lambda obj, name: MAASTestConsolidatedDocument,
    ):

        engine = ReplicatorEngine(target_model="MAASTestConsolidatedDocument")

        raw_document = MAASTestRawDocument(
            kw_field="Some string value",
            long_field=42,
            ingestionTime="2022-10-09T14:42:23.456Z",
        )

        document = engine.consolidate(raw_document, MAASTestConsolidatedDocument())

        assert raw_document.to_dict() | document.to_dict() == raw_document.to_dict()


def test_replicator_engine_get_consolidated_id():
    raw_document = MAASTestRawDocument()

    raw_document.meta.id = "identifier"

    with mock.patch.object(
        ReplicatorEngine,
        "get_model",
        new=lambda obj, name: MAASTestConsolidatedDocument,
    ):
        engine = ReplicatorEngine(target_model="MAASTestConsolidatedDocument")

    assert raw_document.meta.id == engine.get_consolidated_id(raw_document)


def test_replicator_engine_constructor_args():

    with mock.patch.object(
        ReplicatorEngine,
        "get_model",
        new=lambda obj, name: MAASTestConsolidatedDocument,
    ):
        with pytest.raises(ValueError):
            ReplicatorEngine(target_model=None)


def test_replicator_engine_exclude_fields():
    with mock.patch.object(
        ReplicatorEngine,
        "get_model",
        new=lambda obj, name: MAASTestConsolidatedDocument,
    ):

        engine = ReplicatorEngine(
            target_model="MAASTestConsolidatedDocument", exclude_fields=["kw_field"]
        )

        raw_document = MAASTestRawDocument(
            kw_field="Some string value",
            long_field=42,
            ingestionTime="2022-10-09T14:42:23.456Z",
        )

        document = engine.consolidate(raw_document, MAASTestConsolidatedDocument())

        assert "kw_field" not in document.to_dict()
