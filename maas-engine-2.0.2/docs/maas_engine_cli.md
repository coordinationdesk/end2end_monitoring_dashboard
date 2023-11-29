# `maas_engine_cli`: CLI one shot run

`maas-engine` provides a command-line utility that can run an engine in a one-shot way: `maas_engine_cli`.

It has the standard options of most MAAS projects:

```bash
usage: maas_engine_cli [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--es-timeout ES_TIMEOUT] [--es-retries ES_RETRIES]
              [--amqp-username AMQP_USERNAME] [--amqp-password AMQP_PASSWORD] [--amqp-url AMQP_URL] [--amqp-retries AMQP_RETRIES] [-f] [-v] [-vv] [--version] [-c CONFIG]
              [--healthcheck-hostname HEALTHCHECK_HOSTNAME] [--healthcheck-port HEALTHCHECK_PORT] -e ENGINE_ID [--routing-key ROUTING_KEY] [-p PAYLOAD]

optional arguments:
  -h, --help            show this help message and exit
  --es-username ES_USERNAME
                        opensearch user identifier (default: None)
  --es-password ES_PASSWORD
                        opensearch user password (default: None)
  --es-url ES_URL       opensearch cluster URL (default: None)
  --es-timeout ES_TIMEOUT
                        opensearch request timeout in seconds (default: 120)
  --es-retries ES_RETRIES
                        opensearch number of retries (default: 3)
  --amqp-username AMQP_USERNAME
                        AMQP user name (default: None)
  --amqp-password AMQP_PASSWORD
                        AMQP user password (default: None)
  --amqp-url AMQP_URL   AMQP cluster URL (default: None)
  --amqp-retries AMQP_RETRIES
                        AMQP number of retries (default: 0). 0 for infinite
  -f, --force           Force data update
  -v, --verbose         Activate verbose mode
  -vv, --very-verbose   set loglevel to DEBUG
  --version             show program's version number and exit
  -c CONFIG, --config CONFIG
                        Configuration path (default: None)
  --healthcheck-hostname HEALTHCHECK_HOSTNAME
                        Health check host name (default: 0.0.0.0)
  --healthcheck-port HEALTHCHECK_PORT
                        Health check port (default: 2501)
  -e ENGINE_ID, --engine-id ENGINE_ID
                        Engine identifier
  --routing-key ROUTING_KEY
                        Routing key (only if it has a meaning)
  -p PAYLOAD, --payload PAYLOAD
                        Json file containing a MAASMessage
```

The specific options of `maas_engine_cli` are:

- `-e ENGINE_ID, --engine-id ENGINE_ID`: the engine identifier, declared in the class attribute `ENGINE_ID` of the engine
- `--routing-key ROUTING_KEY`: optional routing key that the engine consumes. Only necessary if the engine implementation makes some use of it
- `-p PAYLOAD, --payload PAYLOAD`: optional JSON file path containing the `MAASMessage` payload as it is consumed from the amqp bus.

**Important**: `maas_engine_cli` does not connect to amqp bus (yet):

- It consumes the message provided by the `--payload` option (if any)
- It does not send report messages on the bus. Instead, reports are displayed on the standard input.

It can be useful for engine developments and cron-job on a cluster.
