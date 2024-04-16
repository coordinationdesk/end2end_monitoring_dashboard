"""
Common model features for MAAS projects:

 - base document classes: MAASDocument, MAASRawDocument
 - python DAO code generation from index templates
 - json model code generation for maas-collector

"""

from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

__all__ = [
    "MAASDocument",
    "MAASRawDocument",
    "ZuluDate",
    "datestr_to_zulu",
    "datetime_to_zulu",
    "datestr_to_utc_datetime",
    "MAASMessage",
    "MAASQueryMessage",
    "MAASBaseMessage",
    "DataAction",
]

# import core maas-model symbols
from maas_model.zulu_date import ZuluDate
from maas_model.document import MAASDocument, MAASRawDocument
from maas_model.date_utils import (
    datetime_to_zulu,
    datestr_to_zulu,
    datestr_to_utc_datetime,
)
from maas_model.message import (
    MAASBaseMessage,
    DataAction,
    MAASQueryMessage,
    MAASMessage,
)


try:
    # Change here if project is renamed and does not equal the package name
    # pylint: disable=C0103
    dist_name = "maas-model"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
