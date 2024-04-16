import datetime
from unittest.mock import patch

import pytest
from maas_cds.lib.periodutils import compute_missing_sensing_periods, Period


@pytest.mark.parametrize(
    "test_name,brother_of_datatake_documents,expected_missing_periods",
    [
        (
            "3 ds, two overlapping",
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 55, 58, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 32, tzinfo=datetime.timezone.utc
                    ),
                ),
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 20, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 40, tzinfo=datetime.timezone.utc
                    ),
                ),
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 50, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 57, 10, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 40, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 50, tzinfo=datetime.timezone.utc
                    ),
                ),
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 57, 10, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022,
                        3,
                        29,
                        14,
                        57,
                        15,
                        392000,
                        tzinfo=datetime.timezone.utc,
                    ),
                ),
            ),
        ),
        (
            "No DS",
            (),
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 1, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 57, 23, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
        ),
        (
            "1 big, overlapping ds",
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 1, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 57, 30, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
            (),
        ),
        (
            "2 ds, overlapping",
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 50, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 52, tzinfo=datetime.timezone.utc
                    ),
                ),
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 51, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 53, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 1, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 50, tzinfo=datetime.timezone.utc
                    ),
                ),
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 53, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 57, 18, 392000, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
        ),
        (
            "1 ds",
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 50, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 53, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 1, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 50, tzinfo=datetime.timezone.utc
                    ),
                ),
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 53, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 57, 18, 392000, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
        ),
        (
            "3 ds, two overlapping, overlapping start stop",
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 55, 58, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 10, tzinfo=datetime.timezone.utc
                    ),
                ),
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 20, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 57, 10, tzinfo=datetime.timezone.utc
                    ),
                ),
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 50, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 57, 18, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 10, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 20, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
        ),
        (
            "2 ds, two overlapping, overlapping stop",
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 30, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 57, 5, tzinfo=datetime.timezone.utc
                    ),
                ),
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 55, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 57, 30, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
            (
                Period(
                    start=datetime.datetime(
                        2022, 3, 29, 14, 56, 1, tzinfo=datetime.timezone.utc
                    ),
                    end=datetime.datetime(
                        2022, 3, 29, 14, 56, 30, tzinfo=datetime.timezone.utc
                    ),
                ),
            ),
        ),
    ],
)
def test_missing_sensing_period(
    test_name,
    brother_of_datatake_documents,
    expected_missing_periods,
):
    """Test missing products detection low-level function"""

    missing_periods = tuple(
        compute_missing_sensing_periods(
            Period(
                start=datetime.datetime(
                    2022, 3, 29, 14, 56, 1, tzinfo=datetime.timezone.utc
                ),
                end=datetime.datetime(
                    2022, 3, 29, 14, 57, 23, tzinfo=datetime.timezone.utc
                ),
            ),
            brother_of_datatake_documents,
            6000000,
            -(3608000 + 1000000),
        )
    )

    assert missing_periods == expected_missing_periods, test_name


def test_missing_sensing_period_tolerance_1():
    """Test missing products detection low-level function, with tolerance"""

    brother_of_datatake_documents = (
        Period(
            start=datetime.datetime(
                2022, 3, 29, 14, 56, 10, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2022, 3, 29, 14, 56, 35, tzinfo=datetime.timezone.utc
            ),
        ),
    )

    # First, check plain run
    missing_periods = tuple(
        compute_missing_sensing_periods(
            Period(
                start=datetime.datetime(
                    2022, 3, 29, 14, 56, 10, tzinfo=datetime.timezone.utc
                ),
                end=datetime.datetime(
                    2022, 3, 29, 14, 56, 40, tzinfo=datetime.timezone.utc
                ),
            ),
            brother_of_datatake_documents,
            6000000,
        )
    )

    assert missing_periods == (
        Period(
            start=datetime.datetime(
                2022, 3, 29, 14, 56, 35, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2022, 3, 29, 14, 56, 40, tzinfo=datetime.timezone.utc
            ),
        ),
    )

    # Add tolerance
    missing_periods = tuple(
        compute_missing_sensing_periods(
            Period(
                start=datetime.datetime(
                    2022, 3, 29, 14, 56, 10, tzinfo=datetime.timezone.utc
                ),
                end=datetime.datetime(
                    2022, 3, 29, 14, 56, 40, tzinfo=datetime.timezone.utc
                ),
            ),
            brother_of_datatake_documents,
            6000000,
            tolerance_value=-5000000,
        )
    )

    assert missing_periods == tuple()


def test_missing_sensing_period_tolerance_2():
    """Test missing products detection low-level function, with tolerance"""

    brother_of_datatake_documents = (
        Period(
            start=datetime.datetime(
                2022, 3, 29, 14, 56, 10, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2022, 3, 29, 14, 56, 35, tzinfo=datetime.timezone.utc
            ),
        ),
    )

    # First, check plain run
    missing_periods = tuple(
        compute_missing_sensing_periods(
            Period(
                start=datetime.datetime(
                    2022, 3, 29, 14, 56, 10, tzinfo=datetime.timezone.utc
                ),
                end=datetime.datetime(
                    2022, 3, 29, 14, 56, 40, tzinfo=datetime.timezone.utc
                ),
            ),
            brother_of_datatake_documents,
            6000000,
        )
    )

    assert missing_periods == (
        Period(
            start=datetime.datetime(
                2022, 3, 29, 14, 56, 35, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2022, 3, 29, 14, 56, 40, tzinfo=datetime.timezone.utc
            ),
        ),
    )

    # Add tolerance
    missing_periods = tuple(
        compute_missing_sensing_periods(
            Period(
                start=datetime.datetime(
                    2022, 3, 29, 14, 56, 10, tzinfo=datetime.timezone.utc
                ),
                end=datetime.datetime(
                    2022, 3, 29, 14, 56, 40, tzinfo=datetime.timezone.utc
                ),
            ),
            brother_of_datatake_documents,
            6000000,
            tolerance_value=-10000000,
        )
    )

    assert missing_periods == tuple()
