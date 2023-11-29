"""Abstract base class for extractor"""
import abc
import datetime
from dateutil.parser import parse as parse_datetime
import logging
import hashlib
import re
import typing

# could be a static method of BaseExtractor
def get_hash_func(*fields: str) -> typing.Callable[[list], str]:
    """generate a function that compute field list from a dict to md5"""

    def generate_id(data_dict: dict) -> str:
        md5 = hashlib.md5()
        for name in fields:
            try:
                md5.update(str(data_dict[name]).encode())
            except KeyError as error:
                raise ValueError(f"Field {name} is missing from {data_dict}") from error
        return md5.hexdigest()

    return generate_id


class BaseExtractor(abc.ABC):
    """Base class for data file extraction"""

    def __init__(self, converter_map: dict = None, allow_partial: bool = False):
        """constructor

        Args:
            converter_map (dict, optional): [description]. Defaults to None.
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.converter_map = {}

        self.allow_partial = allow_partial

        self.should_stop = False

        if converter_map:
            self.setup_converter_map(converter_map)

    def stop(self):
        """Indicate the implementation to stop exctractiong"""
        self.logger.info("Extractor should stop")
        self.should_stop = True

    @abc.abstractmethod
    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """generator method that yields data dictionnary extracted from a file"""

    def setup_converter_map(self, converter_map):
        """populate the converter_map"""
        for name, value in converter_map.items():
            if callable(value):
                self.converter_map[name] = value
            elif isinstance(value, dict):
                self.converter_map[name] = self.build_converter(value)
            else:
                raise ValueError(f"Cannot build converter from {repr(value)}")

    @staticmethod
    def build_converter(value: dict):
        """return a callable to convert a field value"""

        if value["type"] == "regex":
            value_format = value.get("format", "{}")
            expression = value["expression"]

            def regex_conv(input_str):
                results = re.findall(expression, input_str)
                if not results:
                    msg = f"no result for {expression} in {input_str}"
                    raise ValueError(msg)
                result = results[0]
                if isinstance(result, str):
                    result = (result,)
                return value_format.format(*result)

            return regex_conv

        if value["type"] == "python":
            # warning EVIL is here BUT legit
            # pylint: disable=W0123
            func = eval(value["python"], {})
            assert callable(func)
            return func

        raise ValueError(f"Cannot build converter from {repr(value)}")

    def convert_data_extract_values(self, data_dict: dict) -> dict:
        """process data_dict to convert values according to converter_map"""
        if not self.converter_map:
            return data_dict

        for name, convert_func in self.converter_map.items():
            try:
                data_dict[name] = convert_func(data_dict[name])
            # catch broad exception to allow partial extraction if necessary
            # pylint: disable=W0703
            except Exception:
                if not self.allow_partial:
                    self.logger.error(
                        "Error converting field %s type: %s value: %s",
                        name,
                        type(data_dict[name]),
                        data_dict[name],
                    )
                    raise

                self.logger.debug("field convertion failed: omit field %s", name)

                data_dict[name] = None

        return data_dict

    def compile_lambda(self, lambda_dict: dict) -> typing.Callable:
        """
        Evaluate a field containing a lambda

        Args:
            lambda_dict (dict): field configuration

        Raises:
            ValueError: if not a callable

        Returns:
            typing.Callable: lambda callable
        """
        # do some check
        if not "python" in lambda_dict:
            raise ValueError(f"{lambda_dict} is not an extractor lambda")

        code = lambda_dict["python"]

        # warning EVIL is here BUT legit
        # pylint: disable=W0123
        func = eval(
            code, {"re": re, "datetime": datetime, "parse_datetime": parse_datetime}
        )
        # pylint: enable=W0123

        if not callable(func):
            raise ValueError(f"{code} is not callable")

        return func

    def evaluate_callable(
        self, func: typing.Callable, argument: typing.Any
    ) -> typing.Any:
        """
        Execute a lambda and allow it to fail if allow_partial is set

        Args:
            func (typing.Callable): compiled lambda
            argument (typing.Any): argument from extractor (csv row, xml node ...)

        Returns:
            typing.Any: return value of func(arg) or None
        """
        value = None
        # catch broad exception to allow partial extraction if necessary
        # pylint: disable=W0703
        try:
            value = func(argument)
        except Exception as error:
            self.logger.debug("lambda failed: %s", error)
            if not self.allow_partial:
                raise
        # pylint: enable=W0703
        return value
