import datetime


from dateutil.tz import tzutc

from maas_model.message import MAASMessage, MAASOperationMessage


def test_message1():
    m = MAASMessage(
        document_class="SomeModel",
        document_ids=["1", "2", "3"],
        document_indices=[
            "raw-data-metrics-product-2023",
            "raw-data-metrics-product-2022",
        ],
        date="1977-01-23T20:15:01.777Z",
    )

    m_dict = m.to_dict()

    assert (
        m_dict
        | {
            "document_class": "SomeModel",
            "document_ids": ["1", "2", "3"],
            "document_indices": [
                "raw-data-metrics-product-2023",
                "raw-data-metrics-product-2022",
            ],
            "date": "1977-01-23T20:15:01.777Z",
        }
        == m_dict
    )

    assert m.msg_datetime == datetime.datetime(
        1977, 1, 23, 20, 15, 1, 777000, tzinfo=tzutc()
    )

    # check date serialization
    m.msg_datetime = datetime.datetime(1947, 2, 27, 18, 20, 43, 945000, tzinfo=tzutc())

    assert m.date == "1947-02-27T18:20:43.945Z"


def test_message2():
    m = MAASMessage(document_class="SomeModel")

    assert m.document_ids == []

    assert m.ancestor_ids == []

    # testing automatic date initialization to now is tricky, so a small timedelta
    # seems enough despite depending of the host performances

    delta = datetime.datetime.now(tz=tzutc()) - m.msg_datetime

    assert delta.total_seconds() < 1


def test_post_deserialization():
    m = MAASMessage(document_class="SomeModel", document_ids=["a", "a"])

    m.post_deserialization()

    assert m.document_ids == ["a"]


def test_operation_message():
    m = MAASOperationMessage(
        date="2023-06-06T14:30:17.281Z",
        message_id="889879d8-97d6-484c-bf3a-7dc8eabfa89c",
        operation_name="Test Operation",
    )

    assert (
        m.to_dict()
        | {
            "ancestor_ids": [],
            "document_class": "",
            "query_string": "*",
            "output_routing_key": "",
            "chunk_size": 0,
            "dry_run": False,
            "operation_name": "Test Operation",
            "operation_args": {},
            "send_reports": False,
        }
        == m.to_dict()
    )
