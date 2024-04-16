"""JSON extractor with extended jsonpath rules implementation """
import typing
from maas_collector.rawdata.extractor.json import JSONExtractor
from jsonpath_ng.ext import parse


class JSONExtractorExtended(JSONExtractor):
    """
    Expand capabilities of the JSONExtractor by using jsonpath_ng.ext instead of jsonpath_ng
    This extractor shall be used when complex jsonpath rules is used like this one
    '`this`.Attributes[?Name=="qualityStatus"].Value'
    This extractor is however slower so use it only when absolutely needed
    """

    def __init__(
        self,
        attr_map: dict,
        converter_map: dict = None,
        iterate_nodes: str = None,
        allow_partial: bool = False,
        parsing_method: typing.Callable = parse,
    ):
        super().__init__(
            attr_map=attr_map,
            converter_map=converter_map,
            iterate_nodes=iterate_nodes,
            allow_partial=allow_partial,
            parsing_method=parsing_method,
        )
