# Discosweb Collector (Used in spaceops projects)

Discosweb collector is used to ingest data from Discosweb web services **[Discosweb web services](https://discosweb.esoc.esa.int/api/objects)**.

## Quick start

```bash
python3 -m -maas_collector.rawdata.cli.discosweb -d $WORK_DIR/maas-deploy-soserver/configuration/collector/discosweb --healthcheck-port 31400 -p 0 -f -v --credential-file "<path to credential-file.json>"
```

## Command Line Options

| CLI option               | Environment variable       | Description                                              |
| ------------------------ | -------------------------- | -------------------------------------------------------- |
| --http-common-timeout    | HTTP_COMMON_TIMEOUT        | Timeout in seconds                                       |
| --http-common-keep-files | HTTP_COMMON_KEEP_FILES     | Keep downloaded api pages (for debug). Defaults to false |

## Collector Configuration Options

| Configuration key | Description                              |
| ----------------- | ---------------------------------------- |
| class             | shall be DiscoswebCollectorConfiguration |

## Sample collector credential configuration

```json
    {
        "name": "discosweb-data-from-discosweb",
        "product_url": "https://discosweb.esoc.esa.int/api/objects",
        "token_field_header": "Authorization",
        "token": "Bearer xxxxxxxxx"
    }
```

## Sample collector configuration

ATTENTION concernant la provenance qui est utlisé pour la consolidation des données

> **⚠️️** **Notes**:

- Si les données proviennent de Discosweb, **provenance** est définie dans notre configuration de collecteur comme **"DISCOSweb"**.
- Si les données proviennent **d'une autre source**, comme un serveur SFTP pour des données simulées (voir la conf rosftp dans maas-deploy-sosserver pour exemple),**provenance** sera configurée selon la source (par exemple, **"TPZ"** ou un autre identifiant spécifique).

> **⚠️️** **Notes**

- **provenance** est fournie à la volée dans cette conf et ne provient pas des données raw
- **data_mode** (Ici REAL mais dans d'autre cas de figure nous pouvons avoir une autre valeur (voir la configuration rosftp pour des données simulées de discosweb dans rosftp dans le projet maas-deploy-ssoserver)) est fournie à la volée dans cette conf et ne provient pas des données raw

```json
{
    "collectors": [
        {
            "class": "DiscoswebCollectorConfiguration",
            "id_field": [
                "provenance",
                "id",
                "cosparId"
            ],
            "routing_key": "new.raw.discosweb.object",
            "interface_name": "discosweb-data-from-discosweb",
            "file_pattern": "discosweb-data-real-*.json",
            "refresh_interval": 0,
            "expected_collect_interval": 86400,
            "end_date_time_offset": 0,
            "discosweb_page_size": 100,
            "discosweb_first_page_index": 1,
            "http_query_params": "page[size]={page_size}&page[number]={page_number}&sort=id",
            "model": "DiscoswebObject",
            "protocol_version": "v2",
            "extractor": {
                "class": "JSONExtractor",
                "args": {
                    "attr_map": {
                        "id": "`this`.id",
                        "type": "`this`.type",
                        "height": "`this`.attributes.height",
                        "firstEpoch": "`this`.attributes.firstEpoch",
                        "cataloguedFragments": "`this`.attributes.cataloguedFragments",
                        "active": "`this`.attributes.active",
                        "xSectAvg": "`this`.attributes.xSectAvg",
                        "diameter": "`this`.attributes.diameter",
                        "depth": "`this`.attributes.depth",
                        "xSectMin": "`this`.attributes.xSectMin",
                        "xSectMax": "`this`.attributes.xSectMax",
                        "satno": "`this`.attributes.satno",
                        "vimpelId": "`this`.attributes.vimpelId",
                        "onOrbitCataloguedFragments": "`this`.attributes.onOrbitCataloguedFragments",
                        "mission": "`this`.attributes.mission",
                        "span": "`this`.attributes.span",
                        "predDecayDate": "`this`.attributes.predDecayDate",
                        "mass": "`this`.attributes.mass",
                        "cosparId": "`this`.attributes.cosparId",
                        "shape": "`this`.attributes.shape",
                        "width": "`this`.attributes.width",
                        "objectClass": "`this`.attributes.objectClass",
                        "name": "`this`.attributes.name",
                        "reentry_links": "`this`.relationships.reentry.links.self",
                        "destinationOrbits_links": "`this`.relationships.destinationOrbits.links.self",
                        "initialOrbits_links": "`this`.relationships.initialOrbits.links.self",
                        "constellations_links": "`this`.relationships.constellations.links.self",
                        "operators_links": "`this`.relationships.operators.links.self",
                        "states_links": "`this`.relationships.states.type.links.self",
                        "launch_links": "`this`.relationships.launch.links.self",
                        "tags_links": "`this`.relationships.tags.links.self",
                        "links": "`this`.links.self",
                        "data_mode": {
                            "python": "lambda c: 'REAL'"
                        },
                        "provenance": {
                            "python": "lambda c: 'DISCOSweb'"
                        }
                    },
                    "iterate_nodes": "$.data",
                    "allow_partial": true
                }
            }
        }
    ],
    "amqp": {
        "new.raw.discosweb.object": {
            "chunk_size": 128
        }
    }
}
```
