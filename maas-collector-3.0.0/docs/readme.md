# maas-collector

Raw data extraction from files to raw database.

## Usage

Add the `-h` to the following calls to know about options (AMQP broker, opensearch3 ...).

It is also convenient to use environment variables:

```bash
# Common arguments
export RAWDATA_CONFIG=/conf/maas-collector-conf.json

export AMQP_URL=amqp://localhost:5672//
export AMQP_USERNAME=guest
export AMQP_PASSWORD=guest

export ES_URL=http://localhost
export ES_USERNAME=admin
export ES_PASSWORD=admin

# For S3 only
export S3_ACCESS_KEY=maasminio
export S3_BUCKET=rawdata
export S3_ENDPOINT=http://s3.maas.telespazio.corp
export S3_KEY_ID=maasminio

# For remote sftp only
export SFTP_HOSTNAME=localhost
export SFTP_PORT=22
export SFTP_USERNAME=jdoe
export SFTP_PASSWORD=jdoe
# path prefix for directory arguments and SFTP_INGESTED_DIR and SFTP_REJECTED_DIR
export SFTP_INBOX_ROOT=/home/jdoe/INBOX
# ingested files are moved to $SFTP_INGESTED_DIR, can be relative or absolute
export SFTP_INGESTED_DIR=INGESTED
# rejected files are moved to $SFTP_REJECTED_DIR, can be relative or absolute
export SFTP_REJECTED_DIR=REJECTED
# age limit in seconds for temporary processing file before it is considered stalled
export SFTP_AGE_LIMIT=900

# for Jira conly
export JIRA_ENDPOINT=https://jirahost.domain.com/rest/api/3/
export JIRA_USERNAME=somejirauser@somedomain.com
export JIRA_TOKEN=somejiratoken


# For health check service
export HEALTHCHECK_HOSTNAME=0.0.0.0
export HEALTHCHECK_PORT=80

# For HTTP OData only
export ODATA_TIMEOUT=30
# see keypass in External Interfaces / Collector API Credentials File
export CREDENTIAL_FILE=/path/to/credential_file.json
```

While running, an HTTP endpoint is available for service health check.

All collectors run periodically ; for one-shot extraction use `-p 0` argument.

### Local file system

Call the `maas_collector.rawdata.cli.filesystem` entry point with a list of files or directories as argument.

```
python -m maas_collector.rawdata.cli.filesystem tests/data/ /var/ingest/
```

Command line options:

```
usage: filesystem.py [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--amqp-username AMQP_USERNAME] [--amqp-password AMQP_PASSWORD]
                     [--amqp-url AMQP_URL] [-f] [-v] [-vv] [--version] -c RAWDATA_CONFIG [-p WATCH_PERIOD] [--working-directory WORKING_DIRECTORY]
                     [--healthcheck-hostname HEALTHCHECK_HOSTNAME] [--healthcheck-port HEALTHCHECK_PORT]
                     PATH [PATH ...]

positional arguments:
  PATH                  Files or directories, space separated

optional arguments:
  -h, --help            show this help message and exit
  --es-username ES_USERNAME
                        opensearcher identifier (default: None)
  --es-password ES_PASSWORD
                        opensearcher password (default: None)
  --es-url ES_URL       opensearchuster URL (default: None)
  --amqp-username AMQP_USERNAME
                        AMQP user name (default: None)
  --amqp-password AMQP_PASSWORD
                        AMQP user password (default: None)
  --amqp-url AMQP_URL   AMQP cluster URL (default: None)
  -f, --force           Force rawdata update
  -v, --verbose         Activate verbose mode
  -vv, --very-verbose   set loglevel to DEBUG
  --version             show program's version number and exit
  -c RAWDATA_CONFIG, --rawdata-config RAWDATA_CONFIG
                        Raw data configuration path (default: None)
  -p WATCH_PERIOD, --watch-period WATCH_PERIOD
                        Watch period for filesystem and sftp (default: 60)
  --working-directory WORKING_DIRECTORY
                        Directory for sftp and s3 downloads (default: /tmp)
  --healthcheck-hostname HEALTHCHECK_HOSTNAME
                        Health check host name (default: 0.0.0.0)
  --healthcheck-port HEALTHCHECK_PORT
                        Health check port (default: 80)

```

### S3 / minio

Call the `maas_collector.rawdata.cli.s3` entry point:

```
python -m maas_collector.rawdata.cli.s3
```

Command line options:

```
usage: s3.py [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--amqp-username AMQP_USERNAME] [--amqp-password AMQP_PASSWORD]
             [--amqp-url AMQP_URL] [-f] [-v] [-vv] [--version] -c RAWDATA_CONFIG [-p WATCH_PERIOD] [--working-directory WORKING_DIRECTORY]
             [--healthcheck-hostname HEALTHCHECK_HOSTNAME] [--healthcheck-port HEALTHCHECK_PORT] [--s3-endpoint S3_ENDPOINT] [--s3-key-id S3_KEY_ID]
             [--s3-access-key S3_ACCESS_KEY] [--s3-bucket S3_BUCKET]

optional arguments:
  -h, --help            show this help message and exit
  --es-username ES_USERNAME
                        opensearcher identifier (default: None)
  --es-password ES_PASSWORD
                        opensearcher password (default: None)
  --es-url ES_URL       opensearchuster URL (default: None)
  --amqp-username AMQP_USERNAME
                        AMQP user name (default: None)
  --amqp-password AMQP_PASSWORD
                        AMQP user password (default: None)
  --amqp-url AMQP_URL   AMQP cluster URL (default: None)
  -f, --force           Force rawdata update
  -v, --verbose         Activate verbose mode
  -vv, --very-verbose   set loglevel to DEBUG
  --version             show program's version number and exit
  -c RAWDATA_CONFIG, --rawdata-config RAWDATA_CONFIG
                        Raw data configuration path (default: None)
  -p WATCH_PERIOD, --watch-period WATCH_PERIOD
                        Watch period for filesystem and sftp (default: 60)
  --working-directory WORKING_DIRECTORY
                        Directory for sftp and s3 downloads (default: /tmp)
  --healthcheck-hostname HEALTHCHECK_HOSTNAME
                        Health check host name (default: 0.0.0.0)
  --healthcheck-port HEALTHCHECK_PORT
                        Health check port (default: 80)
  --s3-endpoint S3_ENDPOINT
                        S3 endpoint URL (default: None)
  --s3-key-id S3_KEY_ID
                        S3 key identifier (default: None)
  --s3-access-key S3_ACCESS_KEY
                        S3 access key (default: None)
  --s3-bucket S3_BUCKET
                        S3 bucket (default: None)
```

### SFTP

Call the `maas_collector.rawdata.cli.sftp` entry point:

```
python -m maas_collector.rawdata.cli.sftp /path/to/remote/dir_or_file /another_path
```

Command line options:

```
usage: sftp.py [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--amqp-username AMQP_USERNAME] [--amqp-password AMQP_PASSWORD]
               [--amqp-url AMQP_URL] [-f] [-v] [-vv] [--version] -c RAWDATA_CONFIG [-p WATCH_PERIOD] [--working-directory WORKING_DIRECTORY]
               [--healthcheck-hostname HEALTHCHECK_HOSTNAME] [--healthcheck-port HEALTHCHECK_PORT] [--sftp-hostname SFTP_HOSTNAME] [--sftp-port SFTP_PORT]
               [--sftp-username SFTP_USERNAME] [--sftp-password SFTP_PASSWORD] [--sftp-process-prefix SFTP_PROCESS_PREFIX] [--sftp-inbox-root SFTP_INBOX_ROOT]
               [--sftp-ingested-dir SFTP_INGESTED_DIR] [--sftp-rejected-dir SFTP_REJECTED_DIR] [--sftp-force-suffix SFTP_FORCE_SUFFIX] [--sftp-age-limit SFTP_AGE_LIMIT]
               REMOTEPATH [REMOTEPATH ...]

positional arguments:
  REMOTEPATH            Remote files or directories, space separated

optional arguments:
  -h, --help            show this help message and exit
  --es-username ES_USERNAME
                        opensearcher identifier (default: None)
  --es-password ES_PASSWORD
                        opensearcher password (default: None)
  --es-url ES_URL       opensearchuster URL (default: None)
  --amqp-username AMQP_USERNAME
                        AMQP user name (default: None)
  --amqp-password AMQP_PASSWORD
                        AMQP user password (default: None)
  --amqp-url AMQP_URL   AMQP cluster URL (default: None)
  -f, --force           Force rawdata update
  -v, --verbose         Activate verbose mode
  -vv, --very-verbose   set loglevel to DEBUG
  --version             show program's version number and exit
  -c RAWDATA_CONFIG, --rawdata-config RAWDATA_CONFIG
                        Raw data configuration path (default: None)
  -p WATCH_PERIOD, --watch-period WATCH_PERIOD
                        Watch period for filesystem and sftp (default: 60)
  --working-directory WORKING_DIRECTORY
                        Directory for sftp and s3 downloads (default: /tmp)
  --healthcheck-hostname HEALTHCHECK_HOSTNAME
                        Health check host name (default: 0.0.0.0)
  --healthcheck-port HEALTHCHECK_PORT
                        Health check port (default: 80)
  --sftp-hostname SFTP_HOSTNAME
                        SFTP host name (default: None)
  --sftp-port SFTP_PORT
                        SFTP port(default: 22)
  --sftp-username SFTP_USERNAME
                        SFTP user name (default: None)
  --sftp-password SFTP_PASSWORD
                        SFTP user password (default: None)
  --sftp-process-prefix SFTP_PROCESS_PREFIX
                        File prefix for processing file (default: .maas-process-)
  --sftp-inbox-root SFTP_INBOX_ROOT
                        Inbox root directory to store INGESTED and REJECTED directories (default: )
  --sftp-ingested-dir SFTP_INGESTED_DIR
                        Directory to store successfully ingested files (default: INGESTED)
  --sftp-rejected-dir SFTP_REJECTED_DIR
                        Directory to store rejected files (default: REJECTED)
  --sftp-force-suffix SFTP_FORCE_SUFFIX
                        File suffix for forcing file ingestion (default: .MAAS-FORCE)
  --sftp-age-limit SFTP_AGE_LIMIT
                        Age limit in seconds for a file to be considered abandonned and ingested again (default: 900 seconds)

```

### FTP

Call the `maas_collector.rawdata.cli.ftp` entry point:

```
python -m maas_collector.rawdata.cli.ftp /path/to/remote/dir_or_file /another_path
```

Command line options:

```
usage: ftp.py [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--amqp-username AMQP_USERNAME] [--amqp-password AMQP_PASSWORD]
               [--amqp-url AMQP_URL] [-f] [-v] [-vv] [--version] -c RAWDATA_CONFIG [-p WATCH_PERIOD] [--working-directory WORKING_DIRECTORY]
               [--healthcheck-hostname HEALTHCHECK_HOSTNAME] [--healthcheck-port HEALTHCHECK_PORT] [--ftp-hostname FTP_HOSTNAME] [--sftp-port FTP_PORT]
               [--ftp-username FTP_USERNAME] [--ftp-password SFTP_PASSWORD]
               REMOTEPATH [REMOTEPATH ...]

positional arguments:
  REMOTEPATH            Remote files or directories, space separated

optional arguments:
  -h, --help            show this help message and exit
  --es-username ES_USERNAME
                        opensearcher identifier (default: None)
  --es-password ES_PASSWORD
                        opensearcher password (default: None)
  --es-url ES_URL       opensearchuster URL (default: None)
  --amqp-username AMQP_USERNAME
                        AMQP user name (default: None)
  --amqp-password AMQP_PASSWORD
                        AMQP user password (default: None)
  --amqp-url AMQP_URL   AMQP cluster URL (default: None)
  -f, --force           Force rawdata update
  -v, --verbose         Activate verbose mode
  -vv, --very-verbose   set loglevel to DEBUG
  --version             show program's version number and exit
  -c RAWDATA_CONFIG, --rawdata-config RAWDATA_CONFIG
                        Raw data configuration path (default: None)
  -p WATCH_PERIOD, --watch-period WATCH_PERIOD
                        Watch period for filesystem and sftp (default: 60)
  --working-directory WORKING_DIRECTORY
                        Directory for sftp and s3 downloads (default: /tmp)
  --healthcheck-hostname HEALTHCHECK_HOSTNAME
                        Health check host name (default: 0.0.0.0)
  --healthcheck-port HEALTHCHECK_PORT
                        Health check port (default: 80)
  --ftp-hostname FTP_HOSTNAME
                        SFTP host name (default: None)
  --ftp-port FTP_PORT
                        FTP port(default: 21)
  --ftp-username FTP_USERNAME
                        FTP user name (default: None)
```

### Jira

Call the `maas_collector.rawdata.cli.jira` entry point:

```
python -m maas_collector.rawdata.cli.jira
```

Command line options:

```console
usage: jira.py [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--amqp-username AMQP_USERNAME] [--amqp-password AMQP_PASSWORD]
               [--amqp-url AMQP_URL] [-f] [-v] [-vv] [--version] -c RAWDATA_CONFIG [-p WATCH_PERIOD] [--working-directory WORKING_DIRECTORY]
               [--healthcheck-hostname HEALTHCHECK_HOSTNAME] [--healthcheck-port HEALTHCHECK_PORT] [--jira-endpoint JIRA_ENDPOINT] [--jira-username JIRA_USERNAME]
               [--jira-token JIRA_TOKEN]

optional arguments:
  -h, --help            show this help message and exit
  --es-username ES_USERNAME
                        opensearcher identifier (default: None)
  --es-password ES_PASSWORD
                        opensearcher password (default: None)
  --es-url ES_URL       opensearchuster URL (default: None)
  --amqp-username AMQP_USERNAME
                        AMQP user name (default: None)
  --amqp-password AMQP_PASSWORD
                        AMQP user password (default: None)
  --amqp-url AMQP_URL   AMQP cluster URL (default: None)
  -f, --force           Force rawdata update
  -v, --verbose         Activate verbose mode
  -vv, --very-verbose   set loglevel to DEBUG
  --version             show program's version number and exit
  -c RAWDATA_CONFIG, --rawdata-config RAWDATA_CONFIG
                        Raw data configuration path (default: None)
  -p WATCH_PERIOD, --watch-period WATCH_PERIOD
                        Watch period for filesystem and sftp (default: 60)
  --working-directory WORKING_DIRECTORY
                        Directory for sftp and s3 downloads (default: /tmp)
  --healthcheck-hostname HEALTHCHECK_HOSTNAME
                        Health check host name (default: 0.0.0.0)
  --healthcheck-port HEALTHCHECK_PORT
                        Health check port (default: 80)
  --jira-endpoint JIRA_ENDPOINT
                        JIRA endpoint (default: None)
  --jira-username JIRA_USERNAME
                        JIRA user name (default: None)
  --jira-token JIRA_TOKEN
                        JIRA user token (default: None)

```

### OData

Call the `maas_collector.rawdata.cli.odata` entry point:

```bash
python -m maas_collector.rawdata.cli.odata
```

Command line options:

```console
usage: odata.py [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--amqp-username AMQP_USERNAME] [--amqp-password AMQP_PASSWORD]
               [--amqp-url AMQP_URL] [-f] [-v] [-vv] [--version] -c RAWDATA_CONFIG [-p WATCH_PERIOD] [--working-directory WORKING_DIRECTORY]
               [--healthcheck-hostname HEALTHCHECK_HOSTNAME] [--healthcheck-port HEALTHCHECK_PORT] [--odata-timeout ODATA_TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  --es-username ES_USERNAME
                        opensearcher identifier (default: None)
  --es-password ES_PASSWORD
                        opensearcher password (default: None)
  --es-url ES_URL       opensearchuster URL (default: None)
  --amqp-username AMQP_USERNAME
                        AMQP user name (default: None)
  --amqp-password AMQP_PASSWORD
                        AMQP user password (default: None)
  --amqp-url AMQP_URL   AMQP cluster URL (default: None)
  -f, --force           Force rawdata update
  -v, --verbose         Activate verbose mode
  -vv, --very-verbose   set loglevel to DEBUG
  --version             show program's version number and exit
  -c RAWDATA_CONFIG, --rawdata-config RAWDATA_CONFIG
                        Raw data configuration path (default: None)
  -p WATCH_PERIOD, --watch-period WATCH_PERIOD
                        Watch period for filesystem and sftp (default: 60)
  --working-directory WORKING_DIRECTORY
                        Directory for sftp and s3 downloads (default: /tmp)
  --healthcheck-hostname HEALTHCHECK_HOSTNAME
                        Health check host name (default: 0.0.0.0)
  --healthcheck-port HEALTHCHECK_PORT
                        Health check port (default: 80)
  --odata-timeout ODATA_TIMEOUT
                        Default timeout (default: 30)
  --odata-credential-file ODATA_CREDENTIAL_FILE
                        Credential file (default: None)
```

## Docker usage

### launch as a filesystem consumer

```
 docker run -it --rm \
   -v $PWD/tests/data/:/data \
   -v $PWD/tests/conf:/conf \
   -e "ES_URL=http://admin:admin@localhost:9200" \
   -e "AMQP_URL=http://guest:guest@localhost:5672" \
   maas-collector
```

### launch as a S3 bucket listener

```
 docker run -it --rm \
   -v $PWD/tests/conf:/conf \
   -e "ES_URL=http://admin:admin@localhost:9200" \
   -e "AMQP_URL=http://guest:guest@localhost:5672" \
   -e "S3_ENDPOINT=http://s3.maas.telespazio.corp" \
   -e "S3_KEY_ID=maasminio" \
   -e "S3_ACCESS_KEY=maasminio" \
   -e "S3_BUCKET=rawdata" \
   maas-collector maas_collector.rawdata.cli.s3
```

## Collector Configuration

maas-collector uses JSON file to store:

- a list of configurations in the root key `collectors`
- amqp fine-tuning in the root key `amqp`

```json
{
  "collectors": [
    {
      "id_field": "...",
      "file_pattern": "...",
      "routing_key": "...",
      "model": {},
      "extractor": {}
    }
  ],
  "amqp": {
    "some.routing.key": {
      "chunk_size": 512
    }
  }
}
```

### Collector configuration

A collector configuration is a JSON object containing the following keys:

`id_field`
: Name of the data attribute that will be used as a unique identifier. It can be a _single string_ or a _list of string_ whose values will be hashed to create a composite identifier in a deterministic way.

`file_pattern`
: A string providing a pattern to match a filename. It shall be compatible with the python module `fnmatch` available in the standard library.

`routing_key`
: A string providing the AMPQ queue name to emit message after model entity creation in the raw storage.

`model`
: An object describing the opensearchcument model. See below for details.

`extractor`
: An object describing the extractor configuration. See below for details.

### Model configuration

Model configuration is stored in an object with the following keys:

`index`
: Name of the opensearchdex to store extracted objects

`name`
: Name of the document class that will be dynamically created in Python.

`fields`
: List of field description object containing two keys: `name` string for the attribute name and `type` string for attribute type. `type` value shall be a class name available in the `opensearchpy.field` module.

`partition_field`
: Optional date field name used to create the index partition name. Defaults to `ingestionTime` model attribute.

`partition_format`
: Optional `datetime.strftime` compatible format string like`%Y-%m` used to create the partition name. Defaults to `%Y`.

#### Model configuration sample

```json
{
  "...": "...",
  "model": {
    "index": "es-sample-index-name",
    "name": "SampleModelClass",
    "partition_field": "fieldName2",
    "partition_format": "%Y-%m",
    "fields": [
      {
        "name": "fieldName1",
        "type": "Keyword"
      },
      {
        "name": "fieldName2",
        "type": "Date"
      },
      {
        "name": "fieldName3",
        "type": "Long"
      }
    ]
  },
  "...": "..."
}
```

### Zulu Date

`Date` fields are automatically replaced by a custom `ZuluDate` class instance to ensure correct serialization of any `datetime` data to Zulu string format.

### Extractor configuration

Extractors are configured by setting a `class` key in the `extractor` object of the configuration and a set of keys in a `args` object:

```json
{
  "...": "...",
  "extractor": {
    "class": "SampleExtractor",
    "args": {
      "custom_arg1": 42,
      "custom_arg2": "jdoe"
    }
  },
  "...": "..."
}
```

#### Extractor implementations

Current implementation provides three generic extractors to ingest some common text format:

- [XMLExtractor](xmlextractor) extracts data from XML document using xpath
- [JSONExtractor](jsonextractor) extracts data from JSON document using json-path
- [LogExtractor](logextractor) extracts data from text log file lines using python regex
- [CSVExtractor](csvextractor) extracts data from comma-separated-value file
- [XLSXExtractor](xlsxextractor) extracts data from XLSX document using xpath

#### Custom extractor implementation

For some special cases, custom implementations are easy to code by implementing an abstract class `BaseExtractor` that only requires to implement the `extract(path:str)` generator method (see custom extractor development guide).

## AMQP message grouping configuration

By default, if a `routing_key` is not empty for a collector configuration, a message will be sent on the `amqp` bus for _each_ entity insert or update.

To group the identifiers provided by extraction,

```json
{
  "collectors": [
    {
      "id_field": "...",
      "file_pattern": "...",
      "routing_key": "...",
      "model": {},
      "extractor": {}
    }
  ],
  "amqp": {
    "some.routing.key": {
      "chunk_size": 512
    }
  }
}
```
