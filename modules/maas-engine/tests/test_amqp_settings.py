# # from pytests.
# from pytest_rabbitmq import factories
import os
from maas_engine.consumer.amqp_settings import AMQPSettings
from maas_engine.engine.query import QueryEngine

# # rabbitmq = factories.rabbitmq_proc(port=5671)

# CONFIG1 = {
#     "amqp": [
#         {
#             "name": "test-exchange",
#             "queues": [
#                 {
#                     "name": "maas-engine-test",
#                     "routing_key": "new.maas.engine.test",
#                     "events": ["MAAS_ENGINE_TEST"],
#                 }
#             ],
#         }
#     ]
# }


def test_AMQPSettings_build():
    #     # settings = AMQPSettings("amqp://localhost:5672//")
    settings = AMQPSettings("amqp://localhost:5676//")


#     connection = settings.connect()
#     settings.build_queues(CONFIG1)
#     # TODO assert about builded Exchange & Queues


def test_config_directory_load():
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
    result = {
        "amqp": [
            {
                "name": "collect-exchange",
                "queues": [
                    {
                        "name": "collect-new.raw.data.lta-product",
                        "routing_key": "new.raw.data.lta-product",
                        "events": [
                            "CONSOLIDATE_REPLICATE",
                            {"id": "CONSOLIDATE_REPLICATE", "send_reports": True},
                        ],
                    }
                ],
            },
            {
                "name": "etl-exchange",
                "queues": [
                    {
                        "name": "etl-compute.cds-datatake",
                        "routing_key": "compute.cds-datatake",
                        "events": ["CONSOLIDATE_REPLICATE"],
                    },
                    {
                        "name": "etl-new.cds-product-s1",
                        "routing_key": "new.cds-product-s1",
                        "events": ["CONSOLIDATE_REPLICATE"],
                    },
                    {
                        "name": "etl-update.cds-product-s1",
                        "routing_key": "update.cds-product-s1",
                        "events": ["CONSOLIDATE_REPLICATE"],
                    },
                    {
                        "name": "etl-new.cds-product-s2",
                        "routing_key": "new.cds-product-s2",
                        "events": ["CONSOLIDATE_REPLICATE"],
                    },
                    {
                        "name": "etl-update.cds-product-s2",
                        "routing_key": "update.cds-product-s2",
                        "events": ["CONSOLIDATE_REPLICATE"],
                    },
                    {
                        "name": "etl-new.cds-datatake-s1",
                        "routing_key": "new.cds-datatake-s1",
                        "events": [{"id": "CONSOLIDATE_REPLICATE"}],
                    },
                    {
                        "name": "etl-update.cds-datatake-s1",
                        "routing_key": "update.cds-datatake-s1",
                        "events": [{"id": "CONSOLIDATE_REPLICATE"}],
                    },
                    {
                        "name": "etl-new.cds-datatake-s2",
                        "routing_key": "new.cds-datatake-s2",
                        "events": [{"id": "CONSOLIDATE_REPLICATE"}],
                    },
                    {
                        "name": "etl-update.cds-datatake-s2",
                        "routing_key": "update.cds-datatake-s2",
                        "events": [{"id": "CONSOLIDATE_REPLICATE"}],
                    },
                    {
                        "name": "etl-new.cds-product-s3",
                        "routing_key": "new.cds-product-s3",
                        "events": ["CONSOLIDATE_REPLICATE"],
                    },
                    {
                        "name": "etl-update.cds-product-s3",
                        "routing_key": "update.cds-product-s3",
                        "events": ["CONSOLIDATE_REPLICATE"],
                    },
                ],
            },
        ]
    }
    engine = QueryEngine
    engine.load_config_directory(ASSETS_DIR)
    assert engine.CONFIG_DICT == result
