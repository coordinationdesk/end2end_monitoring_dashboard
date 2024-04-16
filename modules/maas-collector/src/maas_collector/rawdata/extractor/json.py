"""JSON extractor implementation """
import json
import os
import typing

from jsonpath_ng import parse

from .base import BaseExtractor


class JSONExtractor(BaseExtractor):
    """
    extract data from json files mapping data attributes using json-path expression
    with jsonpath_ng module.

    Provide similar iteration mecanism like XML extractor
    """

    def __init__(
        self,
        attr_map: dict,
        converter_map: dict = None,
        iterate_nodes: str = None,
        allow_partial: bool = False,
        parsing_method: typing.Callable = parse,
    ):
        super().__init__(converter_map=converter_map, allow_partial=allow_partial)
        self.attr_map = {}

        # populate attr map with compiled json-path expression
        for name, value in attr_map.items():
            if isinstance(value, str):
                self.attr_map[name] = self.get_json_mapper_func(value, parsing_method)

            elif isinstance(value, dict):
                if "python" in value:
                    self.attr_map[name] = self.compile_lambda(value)
                else:
                    raise ValueError(f"Unexpected attribute mapper: {value}")

            else:
                raise ValueError(f"Unexpected data type for json attr_map: {value}")

        if isinstance(iterate_nodes, str):
            iterate_expression = parsing_method(iterate_nodes)
            iterate_nodes = iterate_expression.find

        self.iterate_nodes = iterate_nodes

    @staticmethod
    def get_json_mapper_func(jp_value, parsing_method=parse):
        """Build a function to extract values from json content.

        This function:
         - raises IndexError if node not found
         - returns the node value if one node is found
         - returns the list of node values if many nodes are found

        Args:
            jp_value (str): JSON Path expression

        Returns:
            [function]: callable function
        """
        # parse the JSONPath expression
        jp_expr = parsing_method(jp_value)

        def func(json_content):
            result = jp_expr.find(json_content)

            if len(result) == 0:
                raise IndexError(f"JSONPath {jp_expr} returned no value.")

            if len(result) == 1:
                value = result[0].value

            else:
                value = [node.value for node in result]

            return value

        return func

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""

        with open(path, encoding="UTF-8") as json_fd:
            json_content = json.load(json_fd)

        if self.iterate_nodes:
            nodes = self.iterate_nodes(json_content)[0].value
        else:
            # single entity
            nodes = [json_content]

        basepath = os.path.basename(path)

        for node_content in nodes:
            if self.should_stop:
                break

            extract_dict = {"reportName": basepath}

            for name, func in self.attr_map.items():
                try:
                    value = func(node_content)

                    extract_dict[name] = value

                # catch broad exception to allow partial extraction if necessary
                # pylint: disable=W0703
                except IndexError:
                    if self.allow_partial:
                        extract_dict[name] = None
                        self.logger.debug("field %s not extracted", name)
                        continue
                    self.logger.error("Cannot extract field %s", name)
                    raise

            yield self.convert_data_extract_values(extract_dict)
