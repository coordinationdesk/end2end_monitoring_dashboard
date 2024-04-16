"""extractor package contains extractor classes in its namespace"""

# import builtin extractors and core functions

from .base import get_hash_func
from .csv import CSVExtractor
from .json import JSONExtractor
from .json_extended import JSONExtractorExtended
from .log import LogExtractor
from .xml import XMLExtractor
from .xlsx import XLSXExtractor
from .xlsx import XLSXColumnExtractor

# import custom extractor classes
# star import is used because namespace in plugins package is specified with __all__

from .plugins import *
