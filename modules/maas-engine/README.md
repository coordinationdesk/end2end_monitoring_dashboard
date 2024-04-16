# maas-engine

Task runner for maas project.

## Execute

The `maas_engine` module contains the main entry point with the following options:

```bash
python -m maas_engine -h

usage: __main__.py [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--es-timeout ES_TIMEOUT] [--es-retries ES_RETRIES] [--es-reject-errors]
                   [--amqp-username AMQP_USERNAME] [--amqp-password AMQP_PASSWORD] [--amqp-url AMQP_URL] [--amqp-retries AMQP_RETRIES]
                   [--amqp-max-priority AMQP_MAX_PRIORITY] [-f] [-v] [-vv] [--version] [-c CONFIG] [--healthcheck-hostname HEALTHCHECK_HOSTNAME]
                   [--healthcheck-port HEALTHCHECK_PORT]

optional arguments:
  -h, --help            show this help message and exit
  --es-username ES_USERNAME
                        opensearch user identifier (default: admin)
  --es-password ES_PASSWORD
                        opensearch user password (default: admin)
  --es-url ES_URL       opensearch cluster URL (default: http://localhost)
  --es-timeout ES_TIMEOUT
                        opensearch request timeout in seconds (default: 120)
  --es-retries ES_RETRIES
                        opensearch number of retries (default: 3)
  --es-reject-errors    Reject messages when opensearch errors
  --amqp-username AMQP_USERNAME
                        AMQP user name (default: guest)
  --amqp-password AMQP_PASSWORD
                        AMQP user password (default: guest)
  --amqp-url AMQP_URL   AMQP cluster URL (default: amqp://localhost:5672//)
  --amqp-retries AMQP_RETRIES
                        AMQP number of retries (default: 0). 0 for infinite
  --amqp-max-priority AMQP_MAX_PRIORITY
                        AMQP max priority (default: 10). 1 to 10
  -f, --force           Force data update
  -v, --verbose         Activate verbose mode
  -vv, --very-verbose   set loglevel to DEBUG
  --version             show program''s version number and exit
  -c CONFIG, --config CONFIG
                        Configuration path (default: None)
  --healthcheck-hostname HEALTHCHECK_HOSTNAME
                        Health check host name (default: 0.0.0.0)
  --healthcheck-port HEALTHCHECK_PORT
                        Health check port (default: 8127)

```

## Configuration

TBW
