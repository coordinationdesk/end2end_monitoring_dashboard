import datetime
from unittest.mock import patch

from maas_cds.model.anomaly_mixin import AnomalyMixin
from maas_cds.model import CdsCamsTickets


class AnomalyMixinTestModel(AnomalyMixin):
    """
    A test model mixin class for generic anomaly handling
    """

    def __init__(self, cams_tickets=None) -> None:
        super().__init__()

        # populate the required instance attribute for the mixin to work
        self.cams_tickets = [] if cams_tickets is None else cams_tickets


@patch("maas_cds.model.CdsCamsTickets.mget_by_ids")
def test_anomaly_mixin(mock_cams_mget):
    # cook up test data
    for number, ticket in enumerate(
        tickets := [
            CdsCamsTickets(
                url=f"host.domain/ticket-ID-{index}",
                origin=f"origin-{index}",
                description=f"description-{index}",
                created=datetime.datetime(2024, 11, index + 1),
                updated=datetime.datetime(2024, 11, index + 1),
            )
            for index in range(3)
        ]
    ):
        ticket.meta.id = f"ID-{number}"
        ticket.full_clean()

    obj = AnomalyMixinTestModel()

    assert obj.cams_tickets == []

    # test ticket attachment
    for index, ticket in enumerate(tickets):

        obj.set_last_attached_ticket(ticket)

        assert obj.cams_tickets == [
            some_ticket.meta.id for some_ticket in tickets[: index + 1]
        ]

        assert obj.last_attached_ticket == ticket.meta.id
        assert obj.last_attached_ticket_url == ticket.url
        assert obj.cams_origin == ticket.origin
        assert obj.cams_description == ticket.description

    assert len(obj.cams_tickets) == len(tickets)

    # test ticket reset
    for index in reversed(range(1, len(tickets))):
        mock_cams_mget.return_value = tickets[:index]

        ticket = tickets[index - 1]

        # attribute management is done in engine mixin class
        obj.cams_tickets.pop()

        obj.unset_last_attached_ticket()

        assert obj.last_attached_ticket == ticket.meta.id
        assert obj.last_attached_ticket_url == ticket.url
        assert obj.cams_origin == ticket.origin
        assert obj.cams_description == ticket.description

    # last ticket
    obj.cams_tickets.pop()
    obj.unset_last_attached_ticket()

    assert obj.last_attached_ticket is None
    assert obj.last_attached_ticket_url is None
    assert obj.cams_origin is None
    assert obj.cams_description is None

    # Missing input document test
    for ticket in tickets:
        obj.set_last_attached_ticket(ticket)

    # emulate missing document ID-1 with a None value in mget return
    mock_cams_mget.return_value = [tickets[0], None, tickets[2]]

    obj.unset_last_attached_ticket()

    assert obj.last_attached_ticket == "ID-2"

    assert obj.cams_tickets == ["ID-0", "ID-2"]
