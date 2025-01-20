# Common options

Those options are available for all collector entry points.

## Command line options

All collectors implementations support the options detailed in the next subsections.

### General options

| CLI option          | Environment variable | Description                             |
| ------------------- | -------------------- | --------------------------------------- |
| --version           |                      | show program's version number and exit  |
| -v, --verbose       |                      | Activate verbose mode                   |
| -vv, --very-verbose |                      | set loglevel to DEBUG                   |
| --working-directory | WORKING_DIRECTORY    | Directory for downloads (default: /tmp) |
| --credential-file   | CREDENTIAL_FILE      | Credential file (default: None)         |

> By default, only warnings and errors are reported on the standard output, you can use `-v` option for a reasonable amount of logs.

### Ingestion options

| CLI option                      | Environment variable | Description                                                  |
| ------------------------------- | -------------------- | ------------------------------------------------------------ |
| -f, --force                     |                      | Force rawdata update                                         |
| --force-message                 |                      | Notify unmodified documents on the AMQP bus (default: False) |
| -p WATCH_PERIOD, --watch-period | WATCH_PERIOD         | Watch period for filesystem and sftp (default: 60)           |

> If WATCH_PERIOD is zero, then the collector will run a single time before quitting.

### Configuration location options

maas-collector configuration can be stored in a single file, or for a more maintainable large configuration, split in a directory tree that is recursively merged.

| CLI option                       | Environment variable | Description                                      |
| -------------------------------- | -------------------- | ------------------------------------------------ |
| -c or --rawdata-config           | RAWDATA_CONFIG       | Raw data configuration path (default: None)      |
| -d or --rawdata-config-directory | RAWDATA_CONFIG_DIR   | Raw data configuration directory (default: None) |

See [configuration](configuration.md)

### Message bus options

maas-collector notifies database updates with messages sent over an AMQP implementation, RabbitMQ.

| CLI option      | Environment variable | Description                                                   |
| --------------- | -------------------- | ------------------------------------------------------------- |
| --amqp-username | AMQP_USERNAME        | AMQP user name (default: guest)                               |
| --amqp-password | AMQP_PASSWORD        | AMQP user password (default: guest)                           |
| --amqp-url      | AMQP_URL             | AMQP cluster URL (default: amqp://localhost:5672//)           |
| --amqp-retries  | AMQP_RETRIES         | AMQP number of retries (default: 0). 0 for infinite           |
| --amqp-priority | AMQP_PRIORITY        | AMQP message priority (default: 5). Higher is higher priority |

### Database options

maas-collector stores data in a document database, referred as _raw data_: OpenSearch (after a first implementation with ElasticSearch).

| CLI option                     | Environment variable         | Description                                                         |
| ------------------------------ | ---------------------------- | ------------------------------------------------------------------- |
| --es-username                  | ES_USERNAME                  | OpenSearch user identifier (default: admin)                         |
| --es-password                  | ES_PASSWORD                  | OpenSearch user password (default: admin)                           |
| --es-url                       | ES_URL                       | OpenSearch cluster URL (default: http://localhost)                  |
| --es-timeout                   | ES_TIMEOUT                   | OpenSearch request timeout in seconds (default: 120)                |
| --es-retries                   | ES_RETRIES                   | OpenSearch number of retries (default: 3)                           |
| --es-ignore-certs-verification | ES_IGNORE_CERTS_VERIFICATION | If set, the SSL cert of opensearch is not verified (default: False) |

### Health check options

Health check is required to inform cluster software of the status of the service.

| CLI option             | Environment variable | Description                                                 |
| ---------------------- | -------------------- | ----------------------------------------------------------- |
| --healthcheck-hostname | HEALTHCHECK_HOSTNAME | Health check host name (default: 0.0.0.0)                   |
| --healthcheck-port     | HEALTHCHECK_PORT     | Health check port (default: 8127)                           |
| --healthcheck-timeout  | HEALTHCHECK_TIMEOUT  | Time before set status to error in seconds. (default: 1800) |

> **HEALTHCHECK_TIMEOUT** shall be chosen wisely : it has been implemented to make Kubernetes automatically restart stuck collectors (a rare case that sometimes happens with network connectivity problems).

### Backup options

-b BACKUP_ENABLED, --backup BACKUP_ENABLED
Enable backup (default: 1)
-bt {SFTP,S3}, --backup_type {SFTP,S3}
Choose backup type to use (default: SFTP)
--backup-dir BACKUP_DIR
Backup directory (default: /home/jdoe/backup)
--backup-calendar-tree BACKUP_CALENDAR_TREE
Create YYYY/MM/DD backup file tree (default: False)
--backup-gzip BACKUP_GZIP
Compress backup with gzip (default: False)
--backup-s3-endpoint BACKUP_S3_ENDPOINT
Backup S3 endpoint URL (default: None)
--backup-s3-key-id BACKUP_S3_KEY_ID
Backup S3 key identifier (default: None)
--backup-s3-access-key BACKUP_S3_ACCESS_KEY
Backup S3 access key (default: None)
--backup-s3-bucket BACKUP_S3_BUCKET
Backup S3 bucket (default: None)
--backup-hostname BACKUP_HOSTNAME
Backup host name (default: localhost)
--backup-port BACK_PORT
Backup host port(default: 22)
--backup-username BACKUP_USERNAME
Backup user name (default: jdoe)
--backup-password BACKUP_PASSWORD
Backup user password (default: jdoe)
