# maas_migrate

The CLI utility `maas_migrate` helps to perform install opensearch template updates and reindex.

It uses standard maas environment variables:

```bash
$ maas_migrate -h
```

Will output:

```bash
usage: maas_migrate [-h] [--es-username ES_USERNAME] [--es-password ES_PASSWORD] [--es-url ES_URL] [--es-timeout ES_TIMEOUT] [--es-retries ES_RETRIES] [-d] [-v] [-vv]
                    [-r RESOURCES] [-i INSTALL [INSTALL ...]] [-l] [-m MIGRATE [MIGRATE ...]]

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
  -d, --dry-run         Don''t modify database
  -v, --verbose         Activate verbose mode
  -vv, --very-verbose   set loglevel to DEBUG
  -r RESOURCES, --resources RESOURCES
                        resources directory
  -i INSTALL [INSTALL ...], --install INSTALL [INSTALL ...]
                        Install one or more index template (put). ('all' for all templates)
  -l, --list            list available templates
  -m MIGRATE [MIGRATE ...], --migrate MIGRATE [MIGRATE ...]
                        Migrate one or more index template (put) and reindex. ('all' for all templates)
  -p PARTITION [PARTITION ...], --partition PARTITION [PARTITION ...]
                        migrate only a set of partitions
  --populate POPULATE [POPULATE ...]
                        put bulk data into ES (can be xz-compressed)
  --script SCRIPT       script to use during index migrating
  --nuke NUKE [NUKE ...]
                        💣 nuke the database : delete indexes, reinstall templates, create indexes (all for all indexes)
```

Note that command is silent by default: use `-v` for information or `-vv` for debug logs.

## List available templates

```bash
$ maas_migrate -v -l
[2022-04-25 15:12:50] INFO:root: Base class for migrations
[2022-04-25 15:12:50] INFO:MaasMigrator: Found 11 local templates in /app/resources
[2022-04-25 15:12:50] INFO:MaasMigrator: Setup connection to opensearch: http://admin:admin@localhost
[2022-04-25 15:12:50] INFO:opensearch: GET http://localhost:9200/*/_alias [status:200 request:0.423s]
[2022-04-25 15:12:50] INFO:MaasMigrator: Found 80 remote indices
cds-datatake
cds-product
cds-publication
raw-data-app-product
raw-data-auxip-product
raw-data-dd-product
raw-data-ddp-data-available
raw-data-lta-product
raw-data-mp-product
raw-data-prip-product
raw-data-sat-unavailability
```

## Install or update a template

```bash
$ maas_migrate -v -i cds-product
[2022-04-25 15:17:10] INFO:root: Base class for migrations
[2022-04-25 15:17:10] INFO:MaasMigrator: Found 11 local templates in /app/resources
[2022-04-25 15:17:10] INFO:MaasMigrator: Setup connection to opensearch: http://admin:admin@localhost
[2022-04-25 15:17:10] INFO:opensearch: GET http://localhost:9200/*/_alias [status:200 request:0.008s]
[2022-04-25 15:17:10] INFO:MaasMigrator: Found 80 remote indices
[2022-04-25 15:17:10] INFO:MaasMigrator: Reading template /app/resources/templates/cds-product_template.json
[2022-04-25 15:17:10] INFO:opensearch: PUT http://localhost:9200/_template/template_cds-product [status:200 request:0.088s]
```

Using `all` as index name will install all the templates.

## Index migration

Some mapping changes, like changing a field type can not be performed by only putting the new template: a reindex operation is necessary.

Initial index is reindex into a temporary index and deleted. The temporary index is then reindexed to the initial index name.

The deletions are only performed after all the initial reindex operations are successfull to avoid data loss.

```bash
$ maas_migrate -v -m cds-datatake
[2022-04-25 15:22:17] INFO:root: Base class for migrations
[2022-04-25 15:22:17] INFO:MaasMigrator: Found 11 local templates in /app/resources
[2022-04-25 15:22:17] INFO:MaasMigrator: Setup connection to opensearch: http://admin:admin@localhost
[2022-04-25 15:22:17] INFO:opensearch: GET http://localhost:9200/*/_alias [status:200 request:0.007s]
[2022-04-25 15:22:17] INFO:MaasMigrator: Found 80 remote indices
[2022-04-25 15:22:17] INFO:MaasMigrator: Reading template /app/resources/templates/cds-datatake_template.json
[2022-04-25 15:22:17] INFO:opensearch: GET http://localhost:9200/cds-datatake-*/_alias [status:200 request:0.007s]
[2022-04-25 15:22:17] INFO:MaasMigrator: Found 1 indices to migrate: ['cds-datatake-2022-04']
[2022-04-25 15:22:17] INFO:opensearch: PUT http://localhost:9200/_template/template_migrating-cds-datatake [status:200 request:0.059s]
[2022-04-25 15:22:17] INFO:MaasMigrator: Migrating cds-datatake-2022-04
[2022-04-25 15:22:17] INFO:MaasMigrator: Reindexing documents from cds-datatake-2022-04 to migrating-cds-datatake-2022-04
[2022-04-25 15:22:19] INFO:opensearch: POST http://localhost:9200/_reindex?refresh=true [status:200 request:2.434s]
[2022-04-25 15:22:19] INFO:MaasMigrator: {'took': 2402, 'timed_out': False, 'total': 1527, 'updated': 0, 'created': 1527, 'deleted': 0, 'batches': 2, 'version_conflicts': 0, 'noops': 0, 'retries': {'bulk': 0, 'search': 0}, 'throttled_millis': 0, 'requests_per_second': -1.0, 'throttled_until_millis': 0, 'failures': []}
[2022-04-25 15:22:19] INFO:opensearch: PUT http://localhost:9200/_template/template_cds-datatake [status:200 request:0.030s]
[2022-04-25 15:22:19] INFO:MaasMigrator: Deleting cds-datatake-2022-04
[2022-04-25 15:22:19] INFO:opensearch: DELETE http://localhost:9200/cds-datatake-2022-04 [status:200 request:0.060s]
[2022-04-25 15:22:19] INFO:MaasMigrator: Reindexing documents from migrating-cds-datatake-2022-04 to cds-datatake-2022-04
[2022-04-25 15:22:21] INFO:opensearch: POST http://localhost:9200/_reindex?refresh=true [status:200 request:1.452s]
[2022-04-25 15:22:21] INFO:MaasMigrator: {'took': 1447, 'timed_out': False, 'total': 1527, 'updated': 0, 'created': 1527, 'deleted': 0, 'batches': 2, 'version_conflicts': 0, 'noops': 0, 'retries': {'bulk': 0, 'search': 0}, 'throttled_millis': 0, 'requests_per_second': -1.0, 'throttled_until_millis': 0, 'failures': []}
[2022-04-25 15:22:21] INFO:MaasMigrator: Deleting temporary index migrating-cds-datatake-2022-04
[2022-04-25 15:22:21] INFO:opensearch: DELETE http://localhost:9200/migrating-cds-datatake-2022-04 [status:200 request:0.042s]
[2022-04-25 15:22:21] INFO:opensearch: DELETE http://localhost:9200/_template/template_migrating-cds-datatake [status:200 request:0.042s]
```

## Populating Data

Use the 'populate' command to ingest data into an opensearch index.

```bash
maas_migrate -v --populate filename-to-ingest
```

Data format:
Data in json, one entry per line. File can be xz-compressed.

```javascript
{"_op_type": "index","_index":"name-of-index","_source": {json-data}}
```

Example:

```javascript
{
  "_op_type": "index",
  "_index": "s2-tilpar-tiles",
  "_source": {
    "name": "01CCV",
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [
          [177.18928449, -72.01265627],
          [180.0, -72.075577560973],
          [180.0, -72.6058661128217],
          [179.93922476, -72.972797991],
          [176.89507973, -72.9043013],
          [177.18928449, -72.01265627]
        ]
      ]
    },
    "type": "Feature"
  }
}
```

## Custom migration

TODO

See maas_cds/update/patch_1_1_0.py for an implementation example.

## Script in during reindex

For specific a script to use during reindex you can specify the script in args using the `--script` option followed by the script

Example

```bash
maas_migrate -m raw-data-aps-product -p 2022  --script "{\"source\": \"ctx._source.downlink_orbit = '' + (int)ctx._source.downlink_orbit\"}"
```

## 💣 Nuke : reset the database, installing available template, create index

This option is perfect to reset the whole database and create first index with the available template (see Example 1)

Also perfect to reset a part of the environment (see Example 2)

Example 1:

To clear all template and all indices, reinstall all template in ressources folder, create current index of all templatated indices

```bash
maas_migrate -r resources -v --nuke all
```

Example 2:

Clear only two indices ex cds-datatake and maas-collector-journal

```bash
maas_migrate -r resources -v --nuke cds-datatake maas-collector-journal
```

For cds-datatake :

- All previous indices is deleted
- Go the new template,
- A new index cds-datatake is create cause template is available

For maas-collector-journal:

- Index is deleted
- No template cause he didn't exist
- No new index cause template not exist

For others indices/templates:

- Nothing change
