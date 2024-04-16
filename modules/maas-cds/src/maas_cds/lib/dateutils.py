"""Date related functions"""


def get_microseconds_delta(start_date, end_date):
    """return the difference between two datetimes in microseconds"""
    if start_date and end_date:
        if start_date > end_date:
            # swap start and end to be permissive
            start_date, end_date = end_date, start_date
        delta = end_date - start_date
        return delta.total_seconds() * 1000000
    return None
