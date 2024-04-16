"""
Define Exchanges, Queues, Binding
"""

from kombu import Exchange, Queue

COLLECT_EXCHANGE = Exchange("s3-exchange", type="topic", durable=True)

COLLECT_QUEUE_LIST = [
    Queue(
        "collect-new-raw-data",
        COLLECT_EXCHANGE,
        routing_key="new.raw.data",
        durable=True,
        exclusive=False,
        max_priority=9,
    )
]

PUBLISH_EXCHANGE = Exchange("collect-exchange", type="topic", durable=True)
