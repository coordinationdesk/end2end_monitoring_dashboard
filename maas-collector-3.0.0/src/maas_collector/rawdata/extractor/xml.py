"""XMLExtractor implementation"""
import os
import typing
import xml.etree.ElementTree as ET

from .base import BaseExtractor


class XMLExtractor(BaseExtractor):
    """
    extract data from xml files mapping extracted data attributes with xpath expression.
    """

    # yes, extractors need many arguments
    # pylint: disable=R0913
    def __init__(
        self,
        attr_map: dict,
        converter_map: dict = None,
        iterate_nodes=None,
        allow_partial: bool = False,
        default_namespace: str = None,
        namespace_map: dict = None,
    ):
        super().__init__(converter_map=converter_map, allow_partial=allow_partial)
        self.attr_map = {}
        self.default_namespace = default_namespace
        self.namespace_map = namespace_map

        # populate attr_map with callable values
        for name, value in attr_map.items():
            self.attr_map[name] = self._get_xml_mapper_func(name, value)

        if isinstance(iterate_nodes, str):
            # convert path to findall lambda
            path = self._path_with_ns(None, iterate_nodes)
            iterate_nodes = lambda root: root.findall(path)

        self.iterate_nodes = iterate_nodes

    def _path_with_ns(self, name: str, path: str) -> str:
        """add namespace prefix to xpath expression if needed

        Args:
            name (str): name of the attribute
            path (str): XPath expression

        Returns:
            [str]: final XPath expression with namespace if neded
        """
        if self.default_namespace:
            namespace = self.default_namespace
        elif self.namespace_map and name in self.namespace_map:
            namespace = self.namespace_map[name]
        else:
            return path
        return f"{{{namespace}}}{path}"

    def _get_xml_mapper_func(self, name, value) -> typing.Callable:
        """return a callable object to extract a value from a xml document"""
        func = None

        if value is None:
            # node text. useless
            func = lambda node: node.text

        elif callable(value):
            # already a lambda or function
            func = value

        elif isinstance(value, str):
            # node text content
            path = self._path_with_ns(name, value)

            def findtext(element):
                value = element.findtext(path, namespaces=self.namespace_map)
                if value is None:
                    raise ValueError(f"{path} returned None")

                return value

            func = findtext

        elif isinstance(value, dict):
            if "attr" in value:
                # attribute content
                attrname = value["attr"]
                if "path" in value:
                    path = self._path_with_ns(name, value["path"])

                    def findattr(element):
                        node = element.find(path)
                        if node is None:
                            msg = (
                                f"Node {path} does not exist. "
                                + f"Won't find attribute {attrname}. {self.default_namespace}"
                            )
                            raise ValueError(msg)
                        return node.attrib[attrname]

                    # child node attribute
                    func = findattr
                else:
                    # root attribute
                    def findrootattr(element):
                        if not attrname in element.attrib:
                            msg = f"Attribute {attrname} not found on root element"
                            raise ValueError(msg)
                        return element.attrib[attrname]

                    func = findrootattr

            elif "python" in value:
                func = self.compile_lambda(value)

        else:
            raise ValueError(f"Invalid value mapper in XMLExtractor: {repr(value)}")

        if self.converter_map and name in self.converter_map:
            # add converter to the call stack
            target_func = func
            func = lambda element: self.converter_map[name](target_func(element))

        # enforce func check
        assert func is not None and callable(func)

        return func

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""
        tree = ET.parse(path)

        root = tree.getroot()

        if self.iterate_nodes:
            nodes = self.iterate_nodes(root)
        else:
            # single entity
            nodes = [root]

        basepath = os.path.basename(path)

        for element in nodes:

            if self.should_stop:
                break

            extract_dict = {"reportName": basepath}

            for name, func in self.attr_map.items():

                try:
                    extract_dict[name] = func(element)
                # catch broad exception to allow partial extraction if necessary
                # pylint: disable=W0703
                except Exception as error:
                    if not self.allow_partial:
                        self.logger.critical(
                            "Can not extract field %s from %s", name, element.tag
                        )
                        raise error

                    extract_dict[name] = None

                    self.logger.debug("Partial extract: field %s not yet present", name)

            yield extract_dict
