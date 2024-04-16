""" Enumerations CDS model definition """
import enum

__all__ = ["CompletenessStatus", "CompletenessScope"]


class CompletenessStatus(enum.Enum):
    """

    Enumeration to describe completeness status of CdsDatatake
    """

    MISSING = "Missing"

    COMPLETE = "Complete"

    PARTIAL = "Partial"

    UNKNOWN = "Unknown"


class CompletenessScope(enum.Enum):
    """

    Enumeration to describe the scope for completeness
    """

    SLICE = "slice"

    LOCAL = "local"

    GLOBAL = "global"

    FINAL = "final"
