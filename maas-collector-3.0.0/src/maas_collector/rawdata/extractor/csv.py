"""CSV extractor implementation"""
import csv
import os
import typing

from .base import BaseExtractor


class CSVExtractor(BaseExtractor):
    """read log text file line per line and extract data using regular expression from one line

    if attr_map is a dict, cvs.DictReader is used to extract fields.
    if attr_map is a list, csv.reader is used, as it is assumed the csv do not contains headers.
    """

    def __init__(
        self,
        attr_map,
        converter_map: dict = None,
        allow_partial: bool = False,
    ):
        super().__init__(converter_map=converter_map, allow_partial=allow_partial)
        self.attr_map = attr_map

    def extract(self, path, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""

        basepath = os.path.basename(path)

        # depending the attr_map type, choose the according extract method
        reader = (
            self._extract_with_dictreader
            if isinstance(self.attr_map, dict)
            else self._extract_with_reader
        )

        with open(path, encoding="utf-8-sig") as input_fd:

            # automatically setup the csv dialect
            reader_kwargs = {}
            try:
                # configure csv delimiter
                reader_kwargs["dialect"] = csv.Sniffer().sniff(
                    input_fd.readline(), delimiters=",;"
                )
            except csv.Error as error:
                # single column csv will legitimaly fail detecting the dialect
                # but it has hoprefully no impact
                self.logger.debug(error)
            finally:
                # rewind the file descriptor for proper reading
                input_fd.seek(0)

            for extract_dict in reader(input_fd, reader_kwargs):

                extract_dict["reportName"] = basepath

                yield self.convert_data_extract_values(extract_dict)

    def _extract_with_reader(self, input_fd, reader_kwargs):
        """generate data dict from rows using standard cvs reader

        Args:
            input_fd (file): csv file descriptor

        Yields:
            dict: dictionnary based on attr_map
        """

        # list of simple columns
        field_names = [name for name in self.attr_map if isinstance(name, str)]

        # dictionnary of lambda expressions
        lambdas = {}

        # precompile lambdas for performance
        for lambda_dict in [
            lambda_dict
            for lambda_dict in self.attr_map
            if isinstance(lambda_dict, dict) and "python" in lambda_dict
        ]:
            lambdas[lambda_dict["field"]] = self.compile_lambda(lambda_dict)

        for row in csv.reader(input_fd, **reader_kwargs):

            if self.should_stop:
                break

            extract_dict = {}

            # populate standard row fields
            for field, value in zip(field_names, row):
                extract_dict[field] = value

            # populate calculate fields from lambdas
            for field, func in lambdas.items():
                extract_dict[field] = self.evaluate_callable(func, row)

            yield extract_dict

    def _extract_with_dictreader(self, input_fd, reader_kwargs):
        """generate data dict from rows using cvs dict reader

        Args:
            input_fd (file): csv file descriptor

        Yields:
            dict: dictionnary based on attr_map
        """
        # list of simple columns
        field_map = {
            name: value
            for name, value in self.attr_map.items()
            if isinstance(value, str)
        }

        lambdas = {}
        for name, value in self.attr_map.items():
            if isinstance(value, dict):
                if "python" in value:
                    lambdas[name] = self.compile_lambda(value)
                else:
                    raise ValueError(f"Unexpected attribute mapper: {value}")

        for csv_dict in csv.DictReader(input_fd, **reader_kwargs):

            if self.should_stop:
                break

            extract_dict = {}

            # populate from the extracted dictionnary
            for name, value in field_map.items():
                try:
                    extract_dict[name] = csv_dict[value]
                except KeyError:
                    if self.allow_partial:
                        extract_dict[name] = None
                        self.logger.debug("field %s not extracted", name)
                        continue
                    self.logger.error("Cannot extract field %s", name)
                    raise

            # populate calculate fields from lambdas
            for field, func in lambdas.items():
                extract_dict[field] = self.evaluate_callable(func, csv_dict)

            yield extract_dict
