"""Note: Data for this test is partially generated manually"""
import pytest
import datetime

from maas_cds.engines.reports.base import BaseProductConsolidatorEngine
from maas_cds.model import CdsDatatakeS2

TOLERANCE = BaseProductConsolidatorEngine.S2_DATATAKE_ATTACHEMENT_DELTA

#


# s2_product_without_datatake
# "sensing_start_date": "2022-07-01T00:07:44.000Z",
# "sensing_end_date": "2022-07-01T00:10:26.000
def test_s2_product_rattachement_easy_1(s2_product_without_datatake):
    # No datatake
    available_datatakes = []

    nearest_datatake = s2_product_without_datatake.find_nearest_datatake(
        available_datatakes,
        datetime.timedelta(seconds=TOLERANCE),
    )

    s2_product_without_datatake.fill_from_datatake(nearest_datatake)

    assert s2_product_without_datatake.datatake_id is None


def test_s2_product_rattachement_easy_2(s2_product_without_datatake):
    # No neareset
    datatake_doc = CdsDatatakeS2(
        **{
            "datatake_id": "36678-7",
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:07:00.962Z",
            "observation_time_stop": "2022-07-01T00:07:00.970Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )
    datatake_doc.full_clean()

    available_datatakes = [datatake_doc]

    nearest_datatake = s2_product_without_datatake.find_nearest_datatake(
        available_datatakes,
        datetime.timedelta(seconds=TOLERANCE),
    )

    s2_product_without_datatake.fill_from_datatake(nearest_datatake)

    assert s2_product_without_datatake.datatake_id is None


def test_s2_product_rattachement_easy_3(s2_product_without_datatake):
    # one datatake and matching it
    datatake_doc = CdsDatatakeS2(
        **{
            "datatake_id": "36678-7",
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:07:25.962Z",
            "observation_time_stop": "2022-07-01T00:10:11.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )
    datatake_doc.full_clean()

    available_datatakes = [datatake_doc]

    nearest_datatake = s2_product_without_datatake.find_nearest_datatake(
        available_datatakes,
        datetime.timedelta(seconds=TOLERANCE),
    )

    s2_product_without_datatake.fill_from_datatake(nearest_datatake)

    assert s2_product_without_datatake.datatake_id == "36678-7"


def test_s2_product_rattachement_medium_1(s2_product_without_datatake):
    # A list of datatake and matching one
    datatake_doc_1 = CdsDatatakeS2(
        **{
            "datatake_id": False,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:06:44.962Z",
            "observation_time_stop": "2022-07-01T00:07:20.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_2 = CdsDatatakeS2(
        **{
            "datatake_id": False,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:11:25.962Z",
            "observation_time_stop": "2022-07-01T00:11:55.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_3 = CdsDatatakeS2(
        **{
            "datatake_id": True,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:07:25.962Z",
            "observation_time_stop": "2022-07-01T00:10:11.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_1.full_clean()
    datatake_doc_2.full_clean()
    datatake_doc_3.full_clean()

    available_datatakes = [datatake_doc_1, datatake_doc_2, datatake_doc_3]

    nearest_datatake = s2_product_without_datatake.find_nearest_datatake(
        available_datatakes,
        datetime.timedelta(seconds=TOLERANCE),
    )

    s2_product_without_datatake.fill_from_datatake(nearest_datatake)

    assert s2_product_without_datatake.datatake_id


def test_s2_product_rattachement_medium_2(s2_product_without_datatake):
    # A list of datatake and matching one
    datatake_doc_1 = CdsDatatakeS2(
        **{
            "datatake_id": False,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:06:44.962Z",
            "observation_time_stop": "2022-07-01T00:07:20.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_2 = CdsDatatakeS2(
        **{
            "datatake_id": False,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:11:25.962Z",
            "observation_time_stop": "2022-07-01T00:11:55.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_3 = CdsDatatakeS2(
        **{
            "datatake_id": False,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:12:25.962Z",
            "observation_time_stop": "2022-07-01T00:13:11.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_1.full_clean()
    datatake_doc_2.full_clean()
    datatake_doc_3.full_clean()

    available_datatakes = [datatake_doc_1, datatake_doc_2, datatake_doc_3]

    nearest_datatake = s2_product_without_datatake.find_nearest_datatake(
        available_datatakes,
        datetime.timedelta(seconds=TOLERANCE),
    )

    s2_product_without_datatake.fill_from_datatake(nearest_datatake)

    assert s2_product_without_datatake.datatake_id is None


def test_s2_product_rattachement_hardcore_1(s2_product_without_datatake):
    # A list of datatake and matching one with tolerance
    datatake_doc_1 = CdsDatatakeS2(
        **{
            "datatake_id": False,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:06:44.962Z",
            "observation_time_stop": "2022-07-01T00:07:20.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_2 = CdsDatatakeS2(
        **{
            "datatake_id": True,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:06:30.962Z",
            "observation_time_stop": "2022-07-01T00:07:30.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_3 = CdsDatatakeS2(
        **{
            "datatake_id": False,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:12:25.962Z",
            "observation_time_stop": "2022-07-01T00:13:11.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_1.full_clean()
    datatake_doc_2.full_clean()
    datatake_doc_3.full_clean()

    available_datatakes = [datatake_doc_1, datatake_doc_2, datatake_doc_3]

    nearest_datatake = s2_product_without_datatake.find_nearest_datatake(
        available_datatakes,
        datetime.timedelta(seconds=TOLERANCE),
    )

    s2_product_without_datatake.fill_from_datatake(nearest_datatake)

    assert s2_product_without_datatake.datatake_id


def test_s2_product_rattachement_hardcore_2(s2_product_without_datatake):
    # A list of datatake and matching one with tolerance
    datatake_doc_1 = CdsDatatakeS2(
        **{
            "datatake_id": False,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:06:44.962Z",
            "observation_time_stop": "2022-07-01T00:07:20.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_2 = CdsDatatakeS2(
        **{
            "datatake_id": True,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:10:30.962Z",
            "observation_time_stop": "2022-07-01T00:10:50.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_3 = CdsDatatakeS2(
        **{
            "datatake_id": False,
            "satellite_unit": "S2A",
            "mission": "S2",
            "observation_time_start": "2022-07-01T00:12:25.962Z",
            "observation_time_stop": "2022-07-01T00:13:11.930Z",
            "absolute_orbit": "36678",
            "timeliness": "NOMINAL",
        }
    )

    datatake_doc_1.full_clean()
    datatake_doc_2.full_clean()
    datatake_doc_3.full_clean()

    available_datatakes = [datatake_doc_1, datatake_doc_2, datatake_doc_3]

    nearest_datatake = s2_product_without_datatake.find_nearest_datatake(
        available_datatakes,
        datetime.timedelta(seconds=TOLERANCE),
    )

    s2_product_without_datatake.fill_from_datatake(nearest_datatake)

    assert s2_product_without_datatake.datatake_id
