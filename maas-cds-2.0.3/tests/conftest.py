"""
    Dummy conftest.py for maas_cds.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest
from data.s5_data_test import *
from data.s1_data_test import *
from data.s2_data_test import *
from data.s3_data_test import *
from data.dataflow_stub import *
from data.metrics_product_test import *
from data.dd_attrs import *
