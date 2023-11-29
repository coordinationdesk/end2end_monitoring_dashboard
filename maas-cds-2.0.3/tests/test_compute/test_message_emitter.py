from unittest.mock import patch
from pytest import fixture

from maas_cds.lib.message_emitter import MessageEmitter
from maas_engine.engine.base import EngineReport


def test_message_emitter_split_report_single_message():

    message_emitter = MessageEmitter(chunk_size=10, url="")

    report = EngineReport(action="", data_ids=["A", "A", "A", "A", "A"])

    messages = []
    for message in message_emitter._split_report(report):
        messages.append(message)

    assert len(messages) == 1

    for message in messages:
        assert len(set(message.document_ids)) == 1


def test_message_emitter_split_report_no_ids():

    message_emitter = MessageEmitter(chunk_size=2, url="")

    report = EngineReport(action="", data_ids=[])

    messages = []
    for message in message_emitter._split_report(report):
        messages.append(message)

    assert len(messages) == 0


def test_message_emitter_split_report_more_complexe():

    message_emitter = MessageEmitter(chunk_size=2, url="")

    report = EngineReport(action="", data_ids=["A", "A", "B", "B", "C"])

    messages = []
    for message in message_emitter._split_report(report):
        messages.append(message)

    assert len(messages) == 3

    for message in messages:
        assert len(set(message.document_ids)) == 1
