# Queue utilities

`maas-engine` comes with scripts to help with RabbitMQ queues:

- `maas_backup_queue` to download messages and empty a queue
- `maas_aggregate_payloads` to process a set of messages and tune their chunk size
- `maas_publish_message` to publish a folder containing message payloads

Those scripts can help with a saturated queue with too small chunk size, or lower too high chunk size that lead to database timeouts.

They all use the standard options and environment variables.

## Queue Backup

As it uses `drain_events`, **the script does not end and has to be stopped manually** with Ctrl-C when the queue is empty.

```bash
maas_backup_queue -v --ack etl-exchange  etl-new.cds-product-s2 new.cds-product-s2
```

This will create a directory `etl-new.cds-product-s2_1683124931` (queue name with a timestamp) containing payload JSON files, named with uuid.

## Changing payload size

This will process the payloads in `etl-new.cds-product-s2_1683124931`, aggregate them with a chunk size of 512 identifiers and save the messages in `output` directory.

```bash
maas_aggregate_payloads --chunk-size 512 etl-new.cds-product-s2_1683124931 output
```

## Publish a folder of messages

This will publish all messages contained in the `output` directory to the routing key `new.cds-product-s2` on the exchange `etl-exchange`

```bash
maas_publish_message -v  etl-exchange new.cds-product-s2 output
```
