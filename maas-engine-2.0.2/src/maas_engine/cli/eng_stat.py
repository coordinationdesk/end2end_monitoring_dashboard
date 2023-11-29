"""

Simple maas-engine statistics extractor from pod logs.

Wait, it's an ETL in 150 lines ? :D
"""
import collections
import os
import re
import sys
import typing

import numpy
import prettytable


StatRow = collections.namedtuple(
    "StatRow", ["engine", "calls", "min", "mean", "max", "std", "cum"]
)


def load_stats(filename: str) -> dict:
    """
    Read log file and return a dictionnary with duration and performance statistics
    """
    stat_dict = {}
    with open(filename, encoding="utf-8") as fd:
        for line in fd:
            res = re.search(
                r"INFO:(.+): (\d+) created, (\d+) updated, .* (\d+\.\d+)s", line
            )
            if not res:
                continue

            engine, created, updated, duration = res.groups()

            if not engine in stat_dict:
                stat_dict[engine] = {"perfo": [], "duration": []}

            duration = float(duration)

            stat_dict[engine]["duration"].append(duration)

            count = int(created) + int(updated)

            stat_dict[engine]["perfo"].append(count / duration)

    return stat_dict


def build_stat_rows(stat_dict: dict, key: str, sort_key: str) -> typing.List[StatRow]:
    """Build a list of StatRow

    Args:
        stat_dict (dict): statistics
        key (str): statistic key (duration or perfo)
        sort_key (str): sort key

    Returns:
        typing.List[StatRow]: _description_
    """
    rows = []

    for engine in stat_dict.keys():
        stat_array = numpy.array(stat_dict[engine][key])
        rows.append(
            StatRow(
                engine,
                len(stat_array),
                stat_array.min(),
                stat_array.mean(),
                stat_array.max(),
                stat_array.std(),
                stat_array.sum(),
            )
        )

    rows.sort(key=lambda row: getattr(row, sort_key), reverse=True)

    return rows


def build_stat_table(
    rows: typing.List[StatRow], cumulate=True
) -> prettytable.PrettyTable:
    """Build a PrettyTable instance from a list of statistic rows

    Args:
        rows (typing.List[StatRow]): rowq

    Returns:
        prettytable.PrettyTable: populated table
    """
    field_names = ["Engine", "Calls", "Min", "Mean", "Max", "Std"]

    if cumulate:
        field_names.extend(["Cum", "%"])

    table = prettytable.PrettyTable(field_names)

    table.set_style(prettytable.MARKDOWN)

    total_cum = sum(row.cum for row in rows)

    for row in rows:
        table_row = [
            row.engine,
            row.calls,
            f"{row.min:.3f}",
            f"{row.mean:.3f}",
            f"{row.max:.3f}",
            f"{row.std:.3f}",
        ]

        if cumulate:
            table_row.extend(
                [
                    f"{row.cum:.3f}",
                    f"{row.cum / total_cum * 100:.2f}",
                ]
            )

        table.add_row(table_row)

    summary_row = [
        "Total",
        sum(row.calls for row in rows),
        "",
        "",
        "",
        "",
    ]

    if cumulate:
        summary_row.extend(
            [
                f"{total_cum:.3f}",
                "",
            ]
        )

    table.add_row(summary_row)
    return table


def run():
    """Entry point"""
    stats = load_stats(sys.argv[1])

    print(os.linesep * 2 + "## Duration summary in seconds" + os.linesep)

    print(build_stat_table(build_stat_rows(stats, "duration", "cum")))

    print(os.linesep * 2 + "## Performance summary in document per second" + os.linesep)

    print(build_stat_table(build_stat_rows(stats, "perfo", "mean"), cumulate=False))


if __name__ == "__main__":
    run()
