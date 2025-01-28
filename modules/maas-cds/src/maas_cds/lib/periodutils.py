import datetime

from collections import namedtuple
from typing import List


Period = namedtuple("Period", ("start", "end"))


def compute_total_sensing_product(periods: list[Period]) -> int:
    """Compute total sensing period

    Note: periods must be sort

    """

    sensing = 0
    last_period = None

    for period in periods:

        if last_period is None or period.start >= last_period.end:
            sensing += (period.end - period.start).total_seconds() * 1000000
        elif period.start < last_period.end and last_period.end < period.end:
            sensing += (period.end - last_period.end).total_seconds() * 1000000

        last_period = period

    return sensing


def compute_total_sensing_period(periods: list[Period]) -> Period:
    """Compute sensing period covered by products"""

    total_period = None

    for period in periods:
        if total_period is None:
            total_period = Period(period.start, period.end)
        else:
            minstart = min(total_period.start, period.start)
            maxend = max(total_period.end, period.end)
            total_period = Period(minstart, maxend)

    return total_period


def reduce_periods(
    periods: List[Period],
    tolerance_value=datetime.timedelta(seconds=15),
) -> List[Period]:
    """Reduce a list of period"""

    # periods.sort(key=lambda p: (p.start, p.end))  # sort by start date
    periods.sort(key=lambda p: p.start)  # sort by start date

    reduced = []

    for period in periods:

        adjusted_period = Period(
            period.start - tolerance_value, period.end + tolerance_value
        )

        if not reduced:
            reduced.append(adjusted_period)

        elif adjusted_period.start <= reduced[-1].end:
            reduced[-1] = Period(
                reduced[-1].start, max(reduced[-1].end, adjusted_period.end)
            )
        else:
            reduced.append(adjusted_period)

    return reduced


def compute_missing_sensing_periods(
    range_to_evaluate: Period,
    periods: List[Period],
    maximal_offset,
    tolerance_value=0,
) -> List[Period]:
    """Identify missing products within sensing period"""

    period_start = range_to_evaluate.start
    period_stop = range_to_evaluate.end

    if not periods:
        # No coverage at all, return the whole period
        return [Period(period_start, period_stop)]

    period_stop += datetime.timedelta(microseconds=tolerance_value)

    previous = None
    missing_periods = []

    start_offset = (periods[0].start - period_start).total_seconds() * 1000000

    # Missing period at start
    if start_offset > maximal_offset:
        # Fake product ending at the begin of the datatake
        previous = Period(period_start, period_start)

    else:
        # move end date cursor
        period_stop += datetime.timedelta(microseconds=start_offset)

    for brother in periods:
        if previous and brother.start > previous.end:
            # Missing period between products
            missing_periods.append(Period(previous.end, brother.start))
        previous = brother

    end_offset = (period_stop - periods[-1].end).total_seconds()

    if end_offset > 0:
        # Missing period at stop
        missing_periods.append(
            Period(
                periods[-1].end,
                period_stop,
            )
        )

    return missing_periods


def compute_missing_sensing_periods(
    range_to_evaluate: Period,
    periods: List[Period],
    maximal_offset,
    tolerance_value=0,
) -> List[Period]:
    """Identify missing products within sensing period"""

    period_start = range_to_evaluate.start
    period_stop = range_to_evaluate.end

    if not periods:
        # No coverage at all, return the whole period
        return [Period(period_start, period_stop)]

    period_stop += datetime.timedelta(microseconds=tolerance_value)

    previous = None
    missing_periods = []

    start_offset = (periods[0].start - period_start).total_seconds() * 1000000

    # Missing period at start
    if start_offset > maximal_offset:
        # Fake product ending at the begin of the datatake
        previous = Period(period_start, period_start)

    else:
        # move end date cursor
        period_stop += datetime.timedelta(microseconds=start_offset)

    for brother in periods:
        if previous and brother.start > previous.end:
            # Missing period between products
            missing_periods.append(Period(previous.end, brother.start))
        previous = brother

    end_offset = (period_stop - periods[-1].end).total_seconds()

    if end_offset > 0:
        # Missing period at stop
        missing_periods.append(
            Period(
                periods[-1].end,
                period_stop,
            )
        )

    return missing_periods


def compute_duplicated_indicator(
    periods: List[Period],
) -> List[Period]:
    """Identify missing products within sensing period"""

    duplicated_indicator = {
        "min_percentage": 0.0,
        "avg_percentage": 0.0,
        "max_percentage": 0.0,
        "min_duration": 0,
        "avg_duration": 0,
        "max_duration": 0,
    }

    duplicated_percentage = []
    duplicated_duration = []

    if len(periods) < 2:
        # No coverage at all, return the whole period
        return duplicated_indicator

    for previous, brother in zip(periods[:-1], periods[1:]):

        if brother.start < previous.end:
            common_time = (
                min(previous.end, brother.end) - brother.start
            ).total_seconds() * 1000
            duplicated_duration.append(common_time)

            total_period = (previous.end - previous.start).total_seconds() * 1000

            common_percentage = common_time / total_period * 100
            duplicated_percentage.append(common_percentage)
        else:
            duplicated_duration.append(0)
            duplicated_percentage.append(0)

    duplicated_indicator = {
        "min_percentage": float(min(duplicated_percentage)),
        "avg_percentage": float(
            sum(duplicated_percentage) / len(duplicated_percentage)
        ),
        "max_percentage": float(max(duplicated_percentage)),
        "min_duration": int(min(duplicated_duration)),
        "avg_duration": int(sum(duplicated_duration) / len(duplicated_duration)),
        "max_duration": int(max(duplicated_duration)),
    }

    return duplicated_indicator
