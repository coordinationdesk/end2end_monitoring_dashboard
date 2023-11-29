"""Xlsx extractor implementation"""
import os
import typing
import xlrd3


from .base import BaseExtractor


class XLSXExtractor(BaseExtractor):
    """
    extract data from xlsx files mapping extracted data attributes.
    """

    def __init__(
        self,
        attr_map: dict,
        converter_map: dict = None,
        allow_partial: bool = False,
        data_row_offset: int = 1,
        sheet_id=0,
    ):
        super().__init__(converter_map=converter_map, allow_partial=allow_partial)
        self.attr_map = attr_map
        self.data_row_offset = data_row_offset

        self.sheet_id = sheet_id

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""

        basepath = os.path.basename(path)

        workbook = xlrd3.open_workbook(path)

        if isinstance(self.sheet_id, int):
            sheet = workbook.sheet_by_index(self.sheet_id)

        elif isinstance(self.sheet_id, str):
            sheet = workbook.sheet_by_name(self.sheet_id)

        else:
            raise TypeError("sheet_id shall be a string or an integer")

        row_extractor_func = self.build_extractor_callable(sheet)

        for row_index, row in enumerate(sheet):
            if self.should_stop:
                break

            # skip row until data start
            if row_index < self.data_row_offset:
                continue

            extract_dict = row_extractor_func(row)

            extract_dict["reportName"] = basepath

            yield self.convert_data_extract_values(extract_dict)

    def get_cell_value(self, cell: xlrd3.sheet.Cell) -> typing.Any:
        """
        Extract the value of a cell with a coherent type for database.

        Aka convert xlrd3.XL_CELL_DATE to standard datetime

        Args:
            cell (xlrd3.sheet.Cell): cell

        Returns:
            typing.Any: normalised cell value
        """

        if cell.ctype is xlrd3.XL_CELL_DATE:
            # handle special for date
            return xlrd3.xldate_as_datetime(cell.value, 0)

        return cell.value

    def build_extractor_callable(self, sheet: xlrd3.sheet.Sheet) -> typing.Callable:
        """row extraction callable factory

        Args:
            sheet (xlrd3.sheet.Sheet): sheet to extract from

        Raises:
            TypeError: if attr_map has the wrong type

        Returns:
            typing.Callable: row extraction function
        """
        if isinstance(self.attr_map, dict):
            row_extractor = self.build_dict_extractor(sheet)

        elif isinstance(self.attr_map, list):
            row_extractor = self.build_list_extractor()
        else:
            raise TypeError("attr_map is neither a dict or a list")

        return row_extractor

    def build_dict_extractor(self, sheet: xlrd3.sheet.Sheet) -> typing.Callable:
        """
        create a function to extract data_dict from header dictionnary

        Args:
            sheet (xlrd3.sheet.Sheet): sheet to proceed

        Raises:
            ValueError: bad lambda definition

        Returns:
            typing.Callable:  extraction function
        """

        # build the dict keys by merging the headers until data_row_offset
        full_headers = []

        for header_row_index in range(0, self.data_row_offset):
            header_row = sheet.row(header_row_index)

            if not full_headers:
                full_headers = [cell.value for cell in header_row]
                continue

            for col, cell in enumerate(header_row):
                if not cell.value:
                    continue

                full_headers[col] = " ".join((full_headers[col], cell.value))

        # build dictionnary with attribuet and her colums number
        header_dict = {
            header: header_id for header_id, header in enumerate(full_headers)
        }

        field_map = {
            name: value
            for name, value in self.attr_map.items()
            if isinstance(value, str)
        }

        # precompile lambdas
        lambdas = {}

        for name, value in self.attr_map.items():
            if isinstance(value, dict):
                if "python" in value:
                    lambdas[name] = self.compile_lambda(value)
                else:
                    raise ValueError(f"Unexpected attribute mapper: {value}")

        def dict_extractor(row: typing.List) -> typing.Dict:
            """extract attribute values"""

            extract_dict = {}

            # regular fields
            for name, value in field_map.items():
                try:
                    extract_dict[name] = self.get_cell_value(row[header_dict[value]])

                except (ValueError, KeyError) as error:
                    if self.allow_partial:
                        extract_dict[name] = None
                        self.logger.debug("field %s not extracted: %s", name, error)
                        continue
                    self.logger.error("Cannot extract field %s: %s", name, error)
                    raise

            # calculated fields
            for name, func in lambdas.items():
                extract_dict[name] = func(row)

            return extract_dict

        return dict_extractor

    def build_list_extractor(self) -> typing.Callable:
        """
        create a function to extract data_dict from a list

        Raises:
            ValueError: bad lambda definition

        Returns:
            Callable: extraction function
        """
        # precompile key list and lambdas

        # list of simple columns
        field_names = [
            (index, name)
            for index, name in enumerate(self.attr_map)
            if isinstance(name, str)
        ]

        # dictionnary of lambda expressions
        lambdas = {}

        for lambda_dict in [
            lambda_dict
            for lambda_dict in self.attr_map
            if isinstance(lambda_dict, dict)
        ]:
            if not "python" in lambda_dict:
                raise ValueError(f"{lambda_dict} is not an extractor lambda")

            if not "field" in lambda_dict:
                raise ValueError(
                    f"{lambda_dict} is has no field key to store lambda result"
                )

            # warning EVIL is here BUT legit
            # pylint: disable=W0123
            lambdas[lambda_dict["field"]] = eval(lambda_dict["python"], {})
            # pylint: enable=W0123

        def list_extractor(row: typing.List) -> typing.Dict:
            """
            extract row by merging classic fields and calculated
            """
            extract_dict = {}
            for index, name in field_names:
                try:
                    extract_dict[name] = self.get_cell_value(row[index])
                except (ValueError, IndexError) as error:
                    if self.allow_partial:
                        extract_dict[name] = None
                        self.logger.debug("field %s not extracted: %s", name, error)
                        continue
                    self.logger.error("Cannot extract field %s: %s", name, error)
                    raise

            # calculated fields
            for name, func in lambdas.items():
                extract_dict[name] = func(row)

            return extract_dict

        return list_extractor

    # def get_sheet


class XLSXColumnExtractor(XLSXExtractor):
    """

    Extract single values from columns
    """

    def __init__(
        self,
        header_field,
        column_field,
        attr_map: dict = None,
        converter_map: dict = None,
        allow_partial: bool = False,
        data_row_offset: int = 1,
        sheet_id=0,
    ):
        # attr_map is not mandatory due to the specification of header and column fields
        if attr_map is None:
            attr_map = {}

        super().__init__(
            attr_map=attr_map,
            sheet_id=sheet_id,
            data_row_offset=data_row_offset,
            converter_map=converter_map,
            allow_partial=allow_partial,
        )

        self.header_field = header_field

        self.column_field = column_field

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""

        basepath = os.path.basename(path)

        workbook = xlrd3.open_workbook(path)

        if isinstance(self.sheet_id, (int, str)):
            sheet = workbook.sheet_by_index(self.sheet_id)

        else:
            raise TypeError("sheet_id shall be a string or an integer")

        row_extractor_func = self.build_extractor(sheet)

        for row_index, row in enumerate(sheet):
            if self.should_stop:
                break

            # skip row until data start
            if row_index < self.data_row_offset:
                continue

            for extract_dict in row_extractor_func(row):
                extract_dict["reportName"] = basepath

                yield self.convert_data_extract_values(extract_dict)

    def build_extractor(self, sheet: xlrd3.sheet.Sheet) -> typing.Callable:
        """
        create a function to extract data_dict from header dictionnary

        Args:
            sheet (xlrd3.sheet.Sheet): sheet to proceed

        Raises:
            ValueError: bad lambda definition

        Returns:
            typing.Callable:  extraction function
        """

        # build the dict keys by merging the headers until data_row_offset
        full_headers = []

        for header_row_index in range(0, self.data_row_offset):
            header_row = sheet.row(header_row_index)

            if not full_headers:
                full_headers = [cell.value for cell in header_row]
                continue

            for col, cell in enumerate(header_row):
                if not cell.value:
                    continue

                full_headers[col] = " ".join((full_headers[col], cell.value))

        # precompile lambdas
        lambdas = {}

        for name, value in self.attr_map.items():
            if isinstance(value, dict):
                if "python" in value:
                    lambdas[name] = self.compile_lambda(value)
                else:
                    raise ValueError(f"Unexpected attribute mapper: {value}")

        def column_extractor(row: typing.List) -> typing.Dict:
            """extract attribute values"""

            for column_id, column_name in enumerate(full_headers):
                extract_dict = {self.header_field: column_name}

                # regular fields
                try:
                    value = extract_dict[self.column_field] = self.get_cell_value(
                        row[column_id]
                    )
                except (ValueError, KeyError) as error:
                    if self.allow_partial:
                        extract_dict[name] = None
                        self.logger.debug("field %s not extracted: %s", name, error)
                        continue
                    self.logger.error("Cannot extract field %s: %s", name, error)
                    raise

                if not value:
                    self.logger.debug(
                        "Skipping empty cell value in column %s %s",
                        column_id,
                        column_name,
                    )
                    continue

                # calculated fields
                for name, func in lambdas.items():
                    extract_dict[name] = func(row)

                yield extract_dict

        return column_extractor
