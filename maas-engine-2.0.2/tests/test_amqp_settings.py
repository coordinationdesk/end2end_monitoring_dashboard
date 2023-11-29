# # from pytests.
# from pytest_rabbitmq import factories

from maas_engine.consumer.amqp_settings import AMQPSettings

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
