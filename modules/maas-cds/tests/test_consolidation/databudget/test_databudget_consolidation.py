from collections import defaultdict
import uuid

from maas_cds.engines.reports.consolidate_databudget import (
    ConsolidateDatabudget,
)
from maas_cds.model import Databudget
from maas_cds.model.generated import CdsDatabudget


def test_databudget_cleaning():
    engine = ConsolidateDatabudget()
    engine.mission = ["S1", "S2", "S3", "S5"]
    engine.service_type = ["produced", "disseminated", "archived"]

    raw_databudget = Databudget()
    raw_databudget.archived = "alpha"
    raw_databudget.disseminated = " "
    raw_databudget.level = "._ "
    raw_databudget.num_day = "8,9"
    raw_databudget.produced = "a_a"
    raw_databudget.timeliness = "a.a"
    raw_databudget.type = "b_v.a n"
    raw_databudget.volume_day = "1215,3"

    output = engine.clean_raw_data(raw_databudget)
    assert output.archived == "alpha"
    assert output.level == "._"
    assert output.disseminated == ""
    assert output.num_day == "8.9"
    assert output.produced == "a_a"
    assert output.timeliness == "a.a"
    assert output.type == "b_v.a n"
    assert output.volume_day == "1215.3"

    # 0 => L0  etc..
    for i in range(3):
        raw_databudget.level = str(i)
        assert engine.clean_raw_data(raw_databudget).level == "L" + str(i)

    # L1B => L1 etc..
    for i in range(3):
        for x in ["A", "B", "C", "D", "E", "F", "G", "X", "Y", "Z"]:
            raw_databudget.level = "L" + str(i) + x
        assert engine.clean_raw_data(raw_databudget).level == "L" + str(i)


def test_databudget_regex():

    regex_list = [
        {"mission": "S1", "field": "type", "text": "TOTO", "replacement": "TITI"},
        {
            "mission": "S1",
            "field": "timeliness",
            "text": "ECHO",
            "replacement": "FOXTROT",
        },
        {"mission": "S2", "field": "type", "text": "ALPHA", "replacement": "BRAVO"},
        {
            "mission": "S2",
            "field": "timeliness",
            "text": "CHARLIE",
            "replacement": "DELTA",
        },
    ]

    engine = ConsolidateDatabudget(regex_replace_to_perform=regex_list)
    engine.mission = ["S1", "S2", "S3", "S5"]
    engine.service_type = ["produced", "disseminated", "archived"]

    raw_databudget = Databudget()
    raw_databudget.mission = "S1"
    raw_databudget.type = "ALPHA"
    raw_databudget.timeliness = "CHARLIE"

    out = engine.perform_regex_replacement(raw_databudget)
    assert raw_databudget == out

    raw_databudget.mission = "S2"
    out = engine.perform_regex_replacement(raw_databudget)
    assert out.type == "BRAVO"
    assert out.timeliness == "DELTA"

    raw_databudget.mission = "S1"
    raw_databudget.type = "TOTO"
    raw_databudget.timeliness = "ECHO"
    out = engine.perform_regex_replacement(raw_databudget)
    assert out.type == "TITI"
    assert out.timeliness == "FOXTROT"


def test_timeliness_lut_generation():

    engine = ConsolidateDatabudget()
    engine.mission = ["S1", "S2", "S3", "S5"]
    engine.service_type = ["produced", "disseminated", "archived"]
    engine.timeliness_lut = {
        "S3": {
            "NTC": ["NT"],
            "NRT": ["NR", "AL"],
            "STC": ["ST"],
            "AUX": ["SN", "NS", "NN", "_"],
        },
        "S1": {
            "NTC": ["NT", "NTC", "OPER", "OFFL", "NOMINAL"],
            "NRT": ["NRT", "NRT-PT"],
            "UNDERSCORE": ["_"],
            "A": ["NRT-PT", "NTC", "NRT", "_"],
            "AUX": ["_"],
        },
        "S5": {"NTC": ["OPER", "OFFL"], "AUX": ["_"], "NRT": ["NRTI"]},
        "S2": {
            "AUX": ["AUX"],
            "NTC": ["NOMINAL", "NOT_RECORDING"],
            "UNDERSCORE": ["_"],
        },
    }
    out_data = engine.generate_databudget_database_timeliness_lut()

    ##Compare with other calculation
    lut = []
    for mission in engine.mission:
        for db_timeliness, database_timeliness_array in engine.timeliness_lut[
            mission
        ].items():
            for timeliness in database_timeliness_array:
                newdata = CdsDatabudget()
                newdata.data_category = "TIMELINESS_LUT"
                newdata.database_timeliness = timeliness
                newdata.timeliness = db_timeliness
                newdata.mission = mission
                newdata.version = engine.databudget_version
                newdata.meta.id = engine.get_consolidated_id(newdata)
                lut.append(newdata)
    assert out_data == lut


def test_databudget_type_expansion():
    engine = ConsolidateDatabudget()
    engine.mission = ["S1", "S2", "S3", "S5"]
    engine.service_type = ["produced", "disseminated", "archived"]

    db1 = Databudget()
    db1.archived = "ALPHA_1"
    db1.disseminated = "BRAVO_1"
    db1.level = "CHARLIE_1"
    db1.mission = "DELTA_1"
    db1.num_day = 666.6
    db1.produced = "ECHO_1"
    db1.reportFolder = "FOXTROT_1"
    db1.timeliness = "GOLF_1"
    db1.type = "S[1..9]_ETA__AX"
    db1.version = "INDIA_1"
    db1.volume_day = 999.9

    db2 = Databudget()
    db2.archived = "ALPHA_2"
    db2.disseminated = "BRAVO_2"
    db2.level = "CHARLIE_2"
    db2.mission = "DELTA_2"
    db2.num_day = 6666.6
    db2.produced = "ECHO_2"
    db2.reportFolder = "FOXTROT_2"
    db2.timeliness = "GOLF_2"
    db2.type = "S(1.2.3.4.5.6.7.8)_GRDH_1S"
    db2.version = "INDIA_2"
    db2.volume_day = 9999.9

    db3 = Databudget()
    db3.archived = "ALPHA_3"
    db3.disseminated = "BRAVO_3"
    db3.level = "CHARLIE_3"
    db3.mission = "DELTA_3"
    db3.num_day = 66666.6
    db3.produced = "ECHO_3"
    db3.reportFolder = "FOXTROT_3"
    db3.timeliness = "GOLF_3"
    db3.type = "SR_2_SIC{N,S,T}AX"
    db3.version = "INDIA_3"
    db3.volume_day = 99999.9

    db4 = Databudget()
    db4.archived = "ALPHA_4"
    db4.disseminated = "BRAVO_4"
    db4.level = "CHARLIE_4"
    db4.mission = "DELTA_4"
    db4.num_day = 666666.6
    db4.produced = "ECHO_4"
    db4.reportFolder = "FOXTROT_4"
    db4.timeliness = "GOLF_4"
    db4.type = "TOTO"
    db4.version = "INDIA_4"
    db4.volume_day = 999999.9

    raw_data = [db1, db2, db3, db4]
    expanded_raw_data = engine.expand_databudget_type(raw_data)

    assert len(expanded_raw_data) == (
        9 + 8 + 3 + 1
    )  # db1 lead to 9 expansion db2 to 8 and db3 to 3 and db4 to 1

    for i in range(9):
        assert expanded_raw_data[i].archived == "ALPHA_1"
        assert expanded_raw_data[i].disseminated == "BRAVO_1"
        assert expanded_raw_data[i].level == "CHARLIE_1"
        assert expanded_raw_data[i].mission == "DELTA_1"
        assert expanded_raw_data[i].num_day == 666.6
        assert expanded_raw_data[i].produced == "ECHO_1"
        assert expanded_raw_data[i].timeliness == "GOLF_1"
        assert expanded_raw_data[i].databudget_type == "S[1..9]_ETA__AX"
        assert expanded_raw_data[i].database_type == "S" + str(i + 1) + "_ETA__AX"
        assert expanded_raw_data[i].version == "INDIA_1"
        assert expanded_raw_data[i].volume_day == 999.9

    for i in range(9, 9 + 8):
        assert expanded_raw_data[i].archived == "ALPHA_2"
        assert expanded_raw_data[i].disseminated == "BRAVO_2"
        assert expanded_raw_data[i].level == "CHARLIE_2"
        assert expanded_raw_data[i].mission == "DELTA_2"
        assert expanded_raw_data[i].num_day == 6666.6
        assert expanded_raw_data[i].produced == "ECHO_2"
        assert expanded_raw_data[i].timeliness == "GOLF_2"
        assert expanded_raw_data[i].databudget_type == "S(1.2.3.4.5.6.7.8)_GRDH_1S"
        assert expanded_raw_data[i].database_type == "S" + str(i - 8) + "_GRDH_1S"
        assert expanded_raw_data[i].version == "INDIA_2"
        assert expanded_raw_data[i].volume_day == 9999.9

    for i, type_name in ((17, "SR_2_SICNAX"), (18, "SR_2_SICSAX"), (19, "SR_2_SICTAX")):
        assert expanded_raw_data[i].archived == "ALPHA_3"
        assert expanded_raw_data[i].disseminated == "BRAVO_3"
        assert expanded_raw_data[i].level == "CHARLIE_3"
        assert expanded_raw_data[i].mission == "DELTA_3"
        assert expanded_raw_data[i].num_day == 66666.6
        assert expanded_raw_data[i].produced == "ECHO_3"
        assert expanded_raw_data[i].timeliness == "GOLF_3"
        assert expanded_raw_data[i].databudget_type == "SR_2_SIC{N,S,T}AX"
        assert expanded_raw_data[i].database_type == type_name
        assert expanded_raw_data[i].version == "INDIA_3"
        assert expanded_raw_data[i].volume_day == 99999.9

    assert expanded_raw_data[20].archived == "ALPHA_4"
    assert expanded_raw_data[20].disseminated == "BRAVO_4"
    assert expanded_raw_data[20].level == "CHARLIE_4"
    assert expanded_raw_data[20].mission == "DELTA_4"
    assert expanded_raw_data[20].num_day == 666666.6
    assert expanded_raw_data[20].produced == "ECHO_4"
    assert expanded_raw_data[20].timeliness == "GOLF_4"
    assert expanded_raw_data[20].databudget_type == "TOTO"
    assert expanded_raw_data[20].database_type == "TOTO"
    assert expanded_raw_data[20].version == "INDIA_4"
    assert expanded_raw_data[20].volume_day == 999999.9


def test_global_threshold_calculation():

    engine = ConsolidateDatabudget()
    engine.mission = ["S1", "S2", "S3", "S5"]
    engine.service_type = ["produced", "disseminated", "archived"]
    expected_value_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

    # Generate test data
    # 6 elements per service type.
    input_data = []
    for mission_index in (1, 2, 3, 5):
        for produced, archived, disseminated, multiplier in (
            ("P", "", "", 1),
            ("P", "A", "", 2),
            ("P", "A", "D", 3),
            ("", "A", "D", 4),
            ("", "", "D", 5),
            ("P", "", "D", 6),
        ):

            db = Databudget()
            db.archived = archived
            db.disseminated = disseminated
            db.level = "CHARLIE"
            db.mission = "S" + str(mission_index)
            db.num_day = 1.2 * multiplier * mission_index
            db.produced = produced
            db.reportFolder = "FOXTROT"
            db.timeliness = "GOLF"
            db.type = uuid.uuid4()
            db.version = "INDIA"
            db.volume_day = 10.4 * multiplier * mission_index
            input_data.append(db)

            if produced:
                expected_value_dict[db.mission]["produced"]["count"] += db.num_day
                expected_value_dict[db.mission]["produced"]["volume"] += db.volume_day
            if disseminated:
                expected_value_dict[db.mission]["disseminated"]["count"] += db.num_day
                expected_value_dict[db.mission]["disseminated"][
                    "volume"
                ] += db.volume_day
            if archived:
                expected_value_dict[db.mission]["archived"]["count"] += db.num_day
                expected_value_dict[db.mission]["archived"]["volume"] += db.volume_day

    out_data = engine.calculate_global_thresholds(input_data)
    assert len(out_data) == len(engine.mission) * len(engine.service_type)

    for element in out_data:

        assert element.data_category == "GLOBAL_THRESHOLD"

        assert (
            element.threshold_volume
            == expected_value_dict[element.mission][element.threshold_subtype]["volume"]
        )
        assert (
            element.threshold_count
            == expected_value_dict[element.mission][element.threshold_subtype]["count"]
        )


def test_specific_threshold_calculation():

    engine = ConsolidateDatabudget()
    engine.mission = ["S1", "S2", "S3", "S5"]
    engine.service_type = ["produced", "disseminated", "archived"]
    expected_value_dict = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        )
    )

    # Generate test data
    input_data = []
    for mission_index in (1, 2, 3, 5):
        for level, level_multiplier in (("L1", 11), ("L2", 22), ("L3", 33)):
            for timeliness, timeliness_multiplier in (
                ("NTC", 333),
                ("NRT", 666),
                ("STC", 999),
            ):
                for produced, archived, disseminated, multiplier in (
                    ("P", "", "", 1),
                    ("P", "A", "", 2),
                    ("P", "A", "D", 3),
                    ("", "A", "D", 4),
                    ("", "", "D", 5),
                    ("P", "", "D", 6),
                ):
                    db = Databudget()
                    db.archived = archived
                    db.disseminated = disseminated
                    db.level = level
                    db.mission = "S" + str(mission_index)
                    db.num_day = (
                        1.2
                        * multiplier
                        * mission_index
                        * level_multiplier
                        * timeliness_multiplier
                    )
                    db.produced = produced
                    db.reportFolder = "FOXTROT"
                    db.timeliness = timeliness
                    db.type = uuid.uuid4()
                    db.version = "INDIA"
                    db.volume_day = (
                        10.4
                        * multiplier
                        * mission_index
                        * level_multiplier
                        * timeliness_multiplier
                    )
                    input_data.append(db)

                    if produced:
                        expected_value_dict[db.mission]["produced"][level][timeliness][
                            "count"
                        ] += db.num_day
                        expected_value_dict[db.mission]["produced"][level][timeliness][
                            "volume"
                        ] += db.volume_day
                    if disseminated:
                        expected_value_dict[db.mission]["disseminated"][level][
                            timeliness
                        ]["count"] += db.num_day
                        expected_value_dict[db.mission]["disseminated"][level][
                            timeliness
                        ]["volume"] += db.volume_day
                    if archived:
                        expected_value_dict[db.mission]["archived"][level][timeliness][
                            "count"
                        ] += db.num_day
                        expected_value_dict[db.mission]["archived"][level][timeliness][
                            "volume"
                        ] += db.volume_day

    out_data = engine.calculate_specific_thresholds(input_data)

    for element in out_data:
        assert element.data_category == "SPECIFIC_THRESHOLD"

        mission = element.mission
        timeliness = element.timeliness
        level = element.level
        threshold_subtype = element.threshold_subtype
        threshold_volume = element.threshold_volume
        threshold_count = element.threshold_count
        assert (
            threshold_count
            == expected_value_dict[mission][threshold_subtype][level][timeliness][
                "count"
            ]
        )
        assert (
            threshold_volume
            == expected_value_dict[mission][threshold_subtype][level][timeliness][
                "volume"
            ]
        )

    assert len(out_data) == len(engine.mission) * len(
        engine.service_type * 3 * 3  # 3 timeliness and 3 level in test data
    )


def test_override_function():

    engine = ConsolidateDatabudget()
    engine.mission = ["S1", "S2", "S3", "S5"]
    engine.service_type = ["produced", "disseminated", "archived"]
    engine.override_value_dict = [
        {
            "mission": "S1",
            "selector_field": "type",
            "selector_value": "S[1..6]_ETA__AX",
            "override_field": "timeliness",
            "override_value": "A",
        }
    ]

    db1 = Databudget()
    db1.mission = "S1"
    db1.type = "S[1..6]_ETA__AX"
    db1.timeliness = "TOTO"
    assert engine.perform_override(db1).timeliness == "A"

    db1 = Databudget()
    db1.mission = "S2"
    db1.type = "S[1..6]_ETA__AX"
    db1.timeliness = "TOTO"
    assert engine.perform_override(db1).timeliness == "TOTO"

    db2 = Databudget()
    db2.type = "S[1.x.6]_ETA__AX"
    db2.timeliness = "TOTO"
    assert engine.perform_override(db2).timeliness == "TOTO"

    db1 = Databudget()
    db1.archived = "S[1..6]_ETA__AX"
    db1.timeliness = "TOTO"
    assert engine.perform_override(db1).timeliness == "TOTO"
