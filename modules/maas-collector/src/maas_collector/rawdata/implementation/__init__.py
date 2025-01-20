"""

This module namespace stores all collector implementations in his namespace for

monitoring
"""

from maas_collector.rawdata.collector.filecollector import FileCollector

from maas_collector.rawdata.collector.ftpcollector import FTPCollector

from maas_collector.rawdata.collector.httpcollector import HttpCollector

from maas_collector.rawdata.collector.odatacollector import ODataCollector

from maas_collector.rawdata.collector.weathercollector import WeatherCollector

from maas_collector.rawdata.collector.rosftpcollector import ReadOnlySFTPCollector

#
# SFTPCollector is not imported because it does not use the credential file
#
# from maas_collector.rawdata.collector.sftpcollector import SFTPCollector

from maas_collector.rawdata.collector.webdavcollector import WebDAVCollector

from maas_collector.rawdata.collector.jiraxcollector import JIRAExtendedCollector

from maas_collector.rawdata.collector.lokicollector import LokiCollector

from maas_collector.rawdata.collector.mpipcollector import MpipCollector

from maas_collector.rawdata.collector.s3collector import S3Collector

# Duck typing: if it has a CONFIG_CLASS class attribute, then I would say it is a
# collector class
_CONFIG_TO_COLLECTOR_DICT = {
    globals()[collector_class].CONFIG_CLASS.__name__: globals()[collector_class]
    for collector_class in dir()
    if hasattr(globals()[collector_class], "CONFIG_CLASS")
}


def get_collector_class_by_config_classname(name):
    """get the class object associated with configuration class name

    Args:
        name (str): configuration class name

    Returns:
        class: Collector class object
    """
    return _CONFIG_TO_COLLECTOR_DICT[name]
