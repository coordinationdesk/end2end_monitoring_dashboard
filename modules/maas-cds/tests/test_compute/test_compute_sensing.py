from unittest.mock import patch
import datetime

from maas_cds.lib.periodutils import compute_total_sensing_product, Period

from maas_cds.model.datatake_s1 import (
    CdsDatatakeS1,
)


class ProductTest:
    """test class"""

    def __init__(self, sensing_start_date, sensing_end_date):
        self.sensing_start_date = sensing_start_date
        self.sensing_end_date = sensing_end_date
        self.sensing_duration = sensing_end_date - sensing_start_date
        self.key = "KEYKEY"
        self.datatake_id = "RANDOM_DATATAKE_ID"


@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_get_datatake_product_type_brother(mock_find_brother_products_scan):
    """get_datatake_product_type_brother test"""

    periode_1 = ProductTest(
        datetime.datetime(2022, 12, 7, 15, 0, 10, 000000, tzinfo=datetime.timezone.utc),
        datetime.datetime(2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc),
    )

    periode_2 = ProductTest(
        datetime.datetime(2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc),
        datetime.datetime(2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc),
    )

    # Empty product
    periode_3 = ProductTest(
        datetime.datetime(2022, 12, 7, 15, 0, 50, 000000, tzinfo=datetime.timezone.utc),
        datetime.datetime(2022, 12, 7, 15, 0, 50, 000000, tzinfo=datetime.timezone.utc),
    )

    mock_find_brother_products_scan.return_value = [periode_1, periode_2, periode_3]

    datatake_doc = CdsDatatakeS1()

    list_result = datatake_doc.get_datatake_product_type_brother("PRODUCT_TYPE")

    assert list_result == [
        Period(
            start=datetime.datetime(2022, 12, 7, 15, 0, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2022, 12, 7, 15, 0, 20, tzinfo=datetime.timezone.utc),
        ),
        Period(
            start=datetime.datetime(
                2022, 12, 7, 15, 0, 10, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(2022, 12, 7, 15, 0, 20, tzinfo=datetime.timezone.utc),
        ),
    ]


@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_get_period_output_is_sort_1(mock_find_brother_products_scan):
    """get_datatake_product_type_brother test"""

    periode_1 = ProductTest(
        datetime.datetime(2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc),
        datetime.datetime(2022, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc),
    )

    periode_2 = ProductTest(
        datetime.datetime(2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc),
        datetime.datetime(2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc),
    )

    mock_find_brother_products_scan.return_value = [periode_1, periode_2]

    datatake_doc = CdsDatatakeS1()

    list_result = datatake_doc.get_datatake_product_type_brother("PRODUCT_TYPE")

    assert list_result == [
        Period(
            start=datetime.datetime(
                2022, 12, 7, 15, 0, 0, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(2022, 12, 7, 15, 0, 20, tzinfo=datetime.timezone.utc),
        ),
        Period(
            start=datetime.datetime(
                2022, 12, 7, 15, 0, 0, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(2022, 12, 7, 15, 0, 30, tzinfo=datetime.timezone.utc),
        ),
    ]


@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_get_period_output_is_sort_2(mock_find_brother_products_scan):
    """get_datatake_product_type_brother test"""

    periode_1 = ProductTest(
        datetime.datetime(2022, 12, 7, 14, 0, 0, 000000, tzinfo=datetime.timezone.utc),
        datetime.datetime(2022, 12, 7, 14, 0, 29, 000000, tzinfo=datetime.timezone.utc),
    )

    periode_2 = ProductTest(
        datetime.datetime(2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc),
        datetime.datetime(2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc),
    )

    periode_3 = ProductTest(
        datetime.datetime(2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc),
        datetime.datetime(2022, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc),
    )

    periode_4 = ProductTest(
        datetime.datetime(2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc),
        datetime.datetime(2022, 12, 7, 15, 0, 50, 000000, tzinfo=datetime.timezone.utc),
    )

    mock_find_brother_products_scan.return_value = [
        periode_3,
        periode_1,
        periode_2,
        periode_4,
    ]

    datatake_doc = CdsDatatakeS1()

    list_result = datatake_doc.get_datatake_product_type_brother("PRODUCT_TYPE")

    assert list_result == [
        Period(
            datetime.datetime(
                2022, 12, 7, 14, 0, 0, 000000, tzinfo=datetime.timezone.utc
            ),
            datetime.datetime(
                2022, 12, 7, 14, 0, 29, 000000, tzinfo=datetime.timezone.utc
            ),
        ),
        Period(
            datetime.datetime(
                2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc
            ),
            datetime.datetime(
                2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc
            ),
        ),
        Period(
            datetime.datetime(
                2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc
            ),
            datetime.datetime(
                2022, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc
            ),
        ),
        Period(
            datetime.datetime(
                2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc
            ),
            datetime.datetime(
                2022, 12, 7, 15, 0, 50, 000000, tzinfo=datetime.timezone.utc
            ),
        ),
    ]


def test_compute_total_sensing_product_1():
    """compute_total_sensing_product periode test continue"""

    periode_1_start = datetime.datetime(
        2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc
    )

    periode_1_end = datetime.datetime(
        2022, 12, 7, 15, 0, 10, 000000, tzinfo=datetime.timezone.utc
    )

    periode_2_start = datetime.datetime(
        2022, 12, 7, 15, 0, 10, 000000, tzinfo=datetime.timezone.utc
    )

    periode_2_end = datetime.datetime(
        2022, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc
    )

    period_list = [
        Period(periode_1_start, periode_1_end),
        Period(periode_2_start, periode_2_end),
    ]

    acc = compute_total_sensing_product(period_list)

    assert acc == 30 * 1000000


def test_compute_total_sensing_product_2():
    """compute_total_sensing_product test overlapping period"""

    periode_1_start = datetime.datetime(
        2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc
    )

    periode_1_end = datetime.datetime(
        2022, 12, 7, 15, 0, 10, 000000, tzinfo=datetime.timezone.utc
    )

    periode_2_start = datetime.datetime(
        2022, 12, 7, 15, 0, 5, 000000, tzinfo=datetime.timezone.utc
    )

    periode_2_end = datetime.datetime(
        2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc
    )

    period_list = [
        Period(periode_1_start, periode_1_end),
        Period(periode_2_start, periode_2_end),
    ]

    acc = compute_total_sensing_product(period_list)

    assert acc == 20 * 1000000


def test_compute_total_sensing_product_3():
    """compute_total_sensing_product test not continue period"""

    periode_1_start = datetime.datetime(
        2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc
    )

    periode_1_end = datetime.datetime(
        2022, 12, 7, 15, 0, 10, 000000, tzinfo=datetime.timezone.utc
    )

    periode_2_start = datetime.datetime(
        2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc
    )

    periode_2_end = datetime.datetime(
        2022, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc
    )

    period_list = [
        Period(periode_1_start, periode_1_end),
        Period(periode_2_start, periode_2_end),
    ]

    acc = compute_total_sensing_product(period_list)

    assert acc == 20 * 1000000


def test_compute_total_sensing_product_4():
    """compute_total_sensing_product test period in period"""

    periode_1_start = datetime.datetime(
        2022, 12, 7, 15, 0, 0, 000000, tzinfo=datetime.timezone.utc
    )

    periode_1_end = datetime.datetime(
        2022, 12, 7, 15, 0, 20, 000000, tzinfo=datetime.timezone.utc
    )

    periode_2_start = datetime.datetime(
        2022, 12, 7, 15, 0, 5, 000000, tzinfo=datetime.timezone.utc
    )

    periode_2_end = datetime.datetime(
        2022, 12, 7, 15, 0, 10, 000000, tzinfo=datetime.timezone.utc
    )

    period_list = [
        Period(periode_1_start, periode_1_end),
        Period(periode_2_start, periode_2_end),
    ]

    acc = compute_total_sensing_product(period_list)

    assert acc == 20 * 1000000
