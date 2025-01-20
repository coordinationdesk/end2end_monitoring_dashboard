""" 
Report entities are transform to rabbit mq messages
"""

from dataclasses import dataclass, field
import math
from typing import List, Dict


__all__ = ["EngineReport"]


@dataclass
class EngineReport:
    """Dataclass to store engines execution results
    Args:
        document_class (str, optionnal)
        action (str): name of the action the engine did. It is related to the concerned data
        data_ids (list[str]): identifier of the data that have been created/updated/deleted
        chunk_size (int): maximum data_ids length for the emitting the final message

    """

    action: str

    data_ids: List[str]

    document_class: str = ""

    chunk_size: int = 0

    document_indices: List[str] = field(default_factory=lambda: [])

    def __str__(self):
        """format report to show only number of elements, not all identifiers

        Returns:
            str: string representation
        """
        return (
            f"<{self.__class__.__name__} document_class={self.document_class} "
            + f"action={self.action} with {self.size} ids in {self.document_indices}>"
        )

    @property
    def size(self) -> int:
        """return length of identifier list"""
        return len(self.data_ids)

    @staticmethod
    def merge_reports(reports: List["EngineReport"]) -> List["EngineReport"]:
        """Merge the given reports into list of reports with unique action values.
        In other word, if multiple reports have the same action values they are merged
        and put to the returned list

        Args:
            reports (list[EngineReport]): list of reports to merge

        Returns:
            list[EngineReport]: merged report list
        """
        merged_report: Dict[str, "EngineReport"] = {}

        for report in reports:
            if len(report.data_ids) > 0:
                exist_report = merged_report.get(report.action, None)
                if exist_report is None:
                    merged_report[report.action] = report
                else:
                    merged_report[report.action].data_ids.extend(report.data_ids)
                    merged_report[report.action].document_indices.extend(
                        report.document_indices
                    )

                # in any case keep unique ids and keep order
                merged_report[report.action].data_ids = list(
                    dict.fromkeys(merged_report[report.action].data_ids)
                )

                # deduplicate index names (no order)
                merged_report[report.action].document_indices = list(
                    set(merged_report[report.action].document_indices)
                )

        return list(merged_report.values())

    @staticmethod
    def split_reports(reports: List["EngineReport"]):
        """yield reports with data length matching chunk_size"""
        for report in reports:
            if report.chunk_size == 0 or len(report.data_ids) <= report.chunk_size:
                # no chunk
                yield report
                continue

            for index in range(math.ceil(len(report.data_ids) / report.chunk_size)):
                yield EngineReport(
                    report.action,
                    report.data_ids[
                        index * report.chunk_size : index * report.chunk_size
                        + report.chunk_size
                    ],
                    document_class=report.document_class,
                    document_indices=report.document_indices,
                )
