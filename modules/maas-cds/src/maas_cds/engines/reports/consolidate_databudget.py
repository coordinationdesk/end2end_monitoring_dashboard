"""Module responsible for consolidation of databudget raw data"""

from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import re
import typing
from maas_engine.engine.rawdata import DataEngine
from maas_model import MAASMessage
from maas_cds.model.generated import Databudget, CdsDatabudget


class ConsolidateDatabudget(DataEngine):
    """Class responsible to consolidate raw data budget ingested by the collector"""

    ENGINE_ID = "CONSOLIDATE_DATABUDGET"

    def __init__(
        self,
        args=None,
        send_reports=False,
        chunk_size=1,
        regex_replace_to_perform=None,
        override_value_dict=None,
        timeliness_lut=None,
        mission=None,
        level_to_ignore=None,
        service_type=None,
    ):
        super().__init__(args, chunk_size=chunk_size, send_reports=send_reports)
        self.regex_replace_to_perform = regex_replace_to_perform
        self.override_value_dict = override_value_dict
        self.databudget_version = None
        self.report_name = ""
        self.timeliness_lut = timeliness_lut
        self.mission = mission
        self.databudget_version = None
        self.level_to_ignore = level_to_ignore
        self.service_type = service_type

    def action_iterator(self) -> typing.Generator:
        """override

        Iter throught input documents and extract fields from it to populate a consolidated document

        Yields:
            Iterator[typing.Generator]: bulk actions
        """
        for report_name in self.input_documents:
            self.report_name = report_name
            thresholds_and_luts = []
            cleaned_raw_data = []
            for data in self.get_to_be_consolidated_raw_data(report_name):
                data = self.clean_raw_data(data)
                data = self.perform_regex_replacement(data)
                data = self.perform_override(data)
                if data.level in self.level_to_ignore:
                    self.logger.warning(
                        "The element of the input data where level are in the list %s are ignored. Ignored element %s ",
                        self.level_to_ignore,
                        data.type,
                    )
                    continue
                cleaned_raw_data.append(data)

            if cleaned_raw_data and cleaned_raw_data[0].version:
                self.databudget_version = cleaned_raw_data[0].version
            else:
                self.logger.error("Could not determine the version of the databudget")

            thresholds_and_luts.extend(
                self.generate_databudget_database_timeliness_lut()
            )

            # Note : Make sure to execute 'calculate_global_thresholds' and
            #  'calculate_specific_thresholds' before 'expand_databudget_type'
            thresholds_and_luts.extend(
                self.calculate_global_thresholds(cleaned_raw_data)
            )
            thresholds_and_luts.extend(
                self.calculate_specific_thresholds(cleaned_raw_data)
            )

            expanded_raw_data = self.expand_databudget_type(cleaned_raw_data)

            # Clear old databudgets data for same version
            for element_to_delete in (
                CdsDatabudget.search()
                .filter("term", reportName=self.report_name)
                .params(
                    version=True,
                    seq_no_primary_term=True,
                    size=10000,
                )
                .execute()
            ):
                yield element_to_delete.to_bulk_action("delete")

            # Insert new databudget data in db
            for element in expanded_raw_data + thresholds_and_luts:
                element.ingestionTime = datetime.now(tz=timezone.utc)
                element.version = self.databudget_version
                element.reportName = self.report_name
                yield element.to_bulk_action()

    def get_input_documents(self, message: MAASMessage) -> list[str]:
        """Get the input documents. Can be overriden for custom behaviour

        Args:
            message (maas_model.MAASMessage): input message

        Returns:
            list[str]: list of documents id (name of raw databudget file in this particular case)
        """
        return message.document_ids

    def get_to_be_consolidated_raw_data(
        self, report_name: str
    ) -> typing.List[CdsDatabudget]:
        """Try to retrieve in database all documents of the "
        "report_name if they already exist else create it

        Args:
            report_name (str): The input_data report name

        Returns:
            List[CdsDatabudget]: the consolidated documents retrieved "
            "from database + none elements for the ones which has not been found
        """
        search = Databudget.search().filter("term", reportName=report_name)
        self.logger.debug("[%s] to consolidate query : %s", report_name, search)
        search = search.params(ignore=404)
        return list(search.scan())

    def clean_raw_data(self, data: Databudget) -> Databudget:
        """This function perform some cleaning action to make parsing more easier
            The following actions are performed;

            Replace ',' by '.' so that numeric calculatifa

        Args:
            data (Databudget): 1 line of the raw input document "
            "ingested by the consolidation engine buged

        Returns:
            Databudget: Data budget raw line whiere data have been cleaned
        """

        # Clean input data
        for x in (
            "archived",
            "disseminated",
            "archived",
            "level",
            "num_day",
            "produced",
            "timeliness",
            "type",
            "volume_day",
        ):
            if getattr(data, x):
                field = getattr(data, x, "")

                setattr(data, x, field.strip())

                if re.search(r"^[- \.]*+$", field):
                    setattr(data, x, "")

        # Make sure . is used instead of , for fields about to be converted to numeric
        for x in ("num_day", "volume_day"):
            if getattr(data, x):
                field = getattr(data, x, "")
                if "," in field:
                    setattr(data, x, field.replace(",", "."))

        if "level" in data:

            # Level shall start with L
            if data["level"] in ("0", "1", "2"):
                data["level"] = "L" + data["level"]

            # Merge L1A or L1B into L1 level ... same for L0 or L2
            if re.search(r"^L\d[A-Z]$", data["level"]):
                data["level"] = data["level"][:-1]

        return data

    def perform_regex_replacement(self, data: Databudget) -> Databudget:
        """This function use a dict defined in the engine default conf value to
        perform so actions on the input line in of raw databudget

        for each key in the dictionnary,  The 3 following variables shall
        be defined : mission, field, textreplacement and test
        The fonction will look if the input document match

        mission : only perform regex if mission match
        field : only perform regex on a specific named field
        text : search for this text
        replacement= : Replace 'text' by this field

        Args:
            data (Databudget): Source Raw Data input Raw Data Vibudget

        Returns:
            Databudget: Raw Databudget element where regex operations have been performed
        """
        for regex_element in self.regex_replace_to_perform:
            if regex_element["mission"] == data.mission:
                try:
                    old_txt = getattr(data, regex_element["field"], "")
                    setattr(
                        data,
                        regex_element["field"],
                        re.sub(
                            regex_element["text"],
                            regex_element["replacement"],
                            old_txt,
                        ),
                    )
                except TypeError:
                    self.logger.error(
                        "Could not perform regex replacement, make sure all values in "
                        "key field of the regex list are valid. field value used is '%s'",
                        regex_element["field"],
                    )
        return data

    def perform_override(self, data: Databudget) -> Databudget:
        """This function allow user to fill an override dict in the engine default conf
        Then this dict is used to identify which field of which element shall be overriden

        Each element in the dict shall contain:
        - mission : The override will occur only if the document match the mission field of the override dict
        - selector_field & selector_value : An override will only occur if the field defined by selector_field has
                                             the value selector_value. it is used as a document filter

        - override_field : The field where the overriden value shall be written
        - override_value : The value of the overriden value

        Args:
            data (Databudget): Databudget retrieved through the report name in action_iterator

        Returns:
            Databudget: Databudget with overriden data
        """

        for override_element in self.override_value_dict:
            if override_element["mission"] == data.mission:
                try:
                    if (
                        getattr(data, override_element["selector_field"], "")
                        == override_element["selector_value"]
                    ):
                        msg = (
                            f"Override action: field '{override_element['override_field']}'"
                            f"replaced with value '{override_element['override_value']}'"
                            f"for element with type '{data.type}'"
                        )
                        self.logger.info(msg)
                        setattr(
                            data,
                            override_element["override_field"],
                            override_element["override_value"],
                        )
                except TypeError:
                    self.logger.error(
                        "Could not perform override action, make sure  "
                        "mission, selector_field, selector_value,"
                        " override_field  and override_value are defined "
                        "for each element in the override_value_dict"
                    )
        return data

    def calculate_global_thresholds(
        self, data: typing.List[Databudget]
    ) -> typing.List[CdsDatabudget]:
        """This function will create for (PRIP,LTA,DA) for each mission.
        The expected volume value and count value and then store it in a list which is returned
        The expected values are retrieved by doing the sum of the field num_day and volume_day in the raw data

        Args:
            data (List[Databudget]): A single line of the collected data (note:
            When in this function, it already has been cleaned)

        Returns:
            List[CdsDatabudget]: A list filled with the global thresholds ( count and volume)
        """

        out_list = []
        global_threshold_dict = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        )

        for mission in self.mission:
            for element in [x for x in data if x.mission == mission]:
                for stype in self.service_type:
                    e_type = getattr(element, stype, None)
                    if e_type:
                        try:
                            val = float(element.num_day)
                        except ValueError:
                            self.logger.warning(
                                "Could not convert field num_day (%s) "
                                "to float from element with type %s",
                                element.num_day,
                                element.type,
                            )
                        else:
                            global_threshold_dict[mission][stype]["count"][
                                element.type
                            ] += val
                        try:
                            val = float(element.volume_day)
                        except ValueError:
                            self.logger.warning(
                                "Could not convert field volume_day (%s) "
                                "to float from element with type %s",
                                element.volume_day,
                                element.type,
                            )
                        else:
                            global_threshold_dict[mission][stype]["volume"][
                                element.type
                            ] += val

            for stype in self.service_type:
                new_data = CdsDatabudget()
                new_data.mission = mission
                new_data.data_category = "GLOBAL_THRESHOLD"
                new_data.threshold_subtype = stype
                new_data.threshold_volume = sum(
                    global_threshold_dict[mission][stype]["volume"].values()
                )
                new_data.threshold_count = sum(
                    global_threshold_dict[mission][stype]["count"].values()
                )
                new_data.meta.id = self.get_consolidated_id(new_data)
                out_list.append(new_data)

        return out_list

    def calculate_specific_thresholds(
        self, data: typing.List[Databudget]
    ) -> typing.List[CdsDatabudget]:
        """This function is used to generate specific threshold values using data from the databudget
         It shall has a volume and a count value for each combination  mission/level/timeliness/(LTA or PRIP or DA)

        Args:
            data (List[Databudget]): a list of Databudget

        Returns:
            List[CdsDatabudget]: A list containing all specific threshold values
        """

        out_list = []
        threshold_dict = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
            )
        )
        for mission in self.mission:
            for element in [x for x in data if x.mission == mission]:
                for stype in self.service_type:
                    e_type = getattr(element, stype, None)
                    if not (e_type and element.level and element.timeliness):
                        self.logger.warning(
                            "type:%s level:%s timeliness;%s will"
                            "not be used for specific threshold calculation due to missing values",
                            e_type,
                            element.level,
                            element.timeliness,
                        )
                        continue

                    try:
                        val = float(element.volume_day)
                    except ValueError:
                        self.logger.warning(
                            "Specific threshold calculation : Could not convert field num_day (%s) "
                            "to float from element with type %s",
                            element.volume_day,
                            element.type,
                        )
                    else:
                        threshold_dict[mission][stype][element.level][
                            element.timeliness
                        ]["volume"] += val
                    try:
                        val = float(element.num_day)
                    except ValueError:
                        self.logger.warning(
                            "Specific threshold calculation : Could not "
                            "convert field volume_day (%s) "
                            "to float from element with type %s.",
                            element.num_day,
                            element.type,
                        )
                    else:
                        threshold_dict[mission][stype][element.level][
                            element.timeliness
                        ]["count"] += val

            # Generate threshold documents
            for stype in threshold_dict[mission]:
                for level, _ in threshold_dict[mission][stype].items():
                    for timeliness, _ in threshold_dict[mission][stype][level].items():
                        new_data = CdsDatabudget()
                        new_data.version = self.databudget_version
                        new_data.mission = mission
                        new_data.data_category = "SPECIFIC_THRESHOLD"
                        new_data.level = level
                        new_data.timeliness = timeliness
                        new_data.threshold_subtype = stype
                        new_data.threshold_volume = threshold_dict[mission][stype][
                            level
                        ][timeliness]["volume"]

                        new_data.threshold_count = threshold_dict[mission][stype][
                            level
                        ][timeliness]["count"]

                        new_data.meta.id = self.get_consolidated_id(new_data)
                        out_list.append(new_data)
        return out_list

    def expand_databudget_type(
        self, data: typing.List[Databudget]
    ) -> typing.List[CdsDatabudget]:
        """The databudget store some element in a compacted form
           a single line S[1..6]_ETA in the databudget shall lead to the creation of
           6 CdsDatabudget document where databudget shall not change but database_type
           shall be equal to S1_ETA,S2_ETA  etc..

           This function is reponsible for this expansion

        Args:
            data (List[Databudget]): Databudget input document

        Returns:
            List[CdsDatabudget]: CdsDatabudget list wil expanded documents in it
        """

        # expand databudget type for threshold calculation
        # a type like S[1..6]_ETA__AX shall lead to 6 element with their database_type set to
        #   S1_ETA__AX , S2_ETA__AX , S3_ETA__AX  etc....
        out_list = []
        for element in data:
            type_str = element.type

            # eg: S[1..6]_ETA__AX
            match_type1 = re.search(r"\[\d\.+\d\]", type_str)
            # eg: S(1.2.3.4.5.6)_GRDH_1S
            match_type2 = re.search(r"\([\d|\.]+\)", type_str)
            # eg: SR_2_SIC{N,S}AX
            match_type3 = re.search(r"{.+}", type_str)

            if match_type1 or match_type2:
                match_type = match_type2 if match_type2 else match_type1
                start = match_type.span()[0]
                stop = match_type.span()[1]
                nb_element = int(type_str[stop - 2])
                for i in range(1, nb_element + 1):
                    database_type = type_str[:start] + str(i) + type_str[stop:]
                    out_list.append(
                        self.convert_raw_databudget_to_cds_databudget(
                            element, database_type
                        )
                    )
            elif match_type3:
                start = match_type3.span()[0]
                stop = match_type3.span()[1]
                matched_str = match_type3[0][1:-1]
                for x in matched_str.split(","):
                    database_type = type_str[:start] + x + type_str[stop:]
                    out_list.append(
                        self.convert_raw_databudget_to_cds_databudget(
                            element, database_type
                        )
                    )
            else:
                out_list.append(self.convert_raw_databudget_to_cds_databudget(element))
        return out_list

    def generate_databudget_database_timeliness_lut(self) -> typing.List[CdsDatabudget]:
        """This function is responsbile to keep track through a look up table array of the
        timeliness link between the data in the database and the databudget

        Returns:
            List[CdsDatabudget]: Lookup table which associate for each"
            " databudget_type, its database_type equivalent in the database
        """

        lut = []
        for mission in self.mission:
            if mission in self.timeliness_lut:
                index = mission
            else:
                raise IndexError(
                    f"Mission {mission} is missing in the Timeliness look up table"
                )
            for key, value_list in self.timeliness_lut[index].items():
                for timeliness_database in value_list:
                    newdata = CdsDatabudget()
                    newdata.data_category = "TIMELINESS_LUT"
                    newdata.database_timeliness = timeliness_database
                    newdata.timeliness = key
                    newdata.mission = mission
                    newdata.version = self.databudget_version
                    newdata.meta.id = self.get_consolidated_id(newdata)
                    lut.append(newdata)
        return lut

    def get_consolidated_id(self, consolidated_element: CdsDatabudget) -> str:
        """This function is responsible to generate a "
        "consolidated_id using all fields from the CdsDataBudget with md5

        Args:
            consolidated_element (CdsDatabudget): The CdsDatabudget which needs a consolidated ID

        Raises:
            error: In case a field needed for md5 creation has not been found

        Returns:
            str: The consolidated_id string
        """
        md5 = hashlib.md5()
        for name in (
            "archived",
            "produced",
            "disseminated",
            "data_category",
            "database_type",
            "database_timeliness",
            "databudget_type",
            "level",
            "mission",
            "threshold_subtype",
            "timeliness",
            "version",
        ):
            try:
                md5.update(str(getattr(consolidated_element, name, "")).encode())
            except KeyError as error:
                msg = (
                    f"Field {name} is missing from {consolidated_element}."
                    f"Cannot retrieve consolidated id"
                )

                self.logger.error(msg)
                raise error
            else:
                md5.update((self.report_name).encode())
        return md5.hexdigest()

    def convert_raw_databudget_to_cds_databudget(
        self, raw_databudget: Databudget, database_type: str = ""
    ) -> CdsDatabudget:
        """This function is responsible for the conversion of a Databudget into a CdsDatabudget

        Args:
            raw_databudget (Databudget): The raw Databudget input document
            database_type (str, optional): If set, it forces the database_type of
            the CdsDatabudget"" . Defaults to "".

        Returns:
            CdsDatabudget: The converted raw document in CdsDatabudget format
        """

        dtb = CdsDatabudget()
        dtb.archived = raw_databudget.archived
        dtb.data_category = "RAW"
        dtb.database_type = database_type if database_type else raw_databudget.type
        dtb.databudget_type = raw_databudget.type
        dtb.disseminated = raw_databudget.disseminated
        dtb.level = raw_databudget.level
        dtb.mission = raw_databudget.mission
        dtb.produced = raw_databudget.produced
        dtb.timeliness = raw_databudget.timeliness
        dtb.version = raw_databudget.version

        try:
            dtb.volume_day = float(raw_databudget.volume_day)
        except ValueError:
            self.logger.warning(
                "Could not convert the document with mission:%s, database_type:%s due to"
                " a conversion issue on field %s",
                dtb.mission,
                dtb.database_type,
                dtb.volume_day,
            )

        try:
            dtb.num_day = float(raw_databudget.num_day)
        except ValueError:
            self.logger.warning(
                "Could not convert the document with mission:%s, database_type:%s due to"
                " a conversion issue on field %s",
                dtb.mission,
                dtb.database_type,
                dtb.volume_day,
            )
        dtb.meta.id = self.get_consolidated_id(dtb)
        return dtb
