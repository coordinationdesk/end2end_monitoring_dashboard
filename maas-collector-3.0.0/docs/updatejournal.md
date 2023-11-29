

# **`Update Journal Index`**

## `Contents`

1. [With curl command](#with-curl-command)
2. [With update_journal script](#with-update_journal-script)


## **`With curl command`**

To update the dates of an identifier in an index of an elastic database, we can use the following curl command : 

```
curl -XPOST -u admin:admin --header 'Content-Type: application/json' http://localhost:9200/maas-collector-journal/_update_by_query?pretty -d '{"query":{"term":{"_id":"LTA_Werum"}},"script":"ctx._source.last_collect_date=\"2021-12-15T08:30:00.549Z\";ctx._source.last_date=\"2021-12-15T08:30:00.549Z\""}'
```

where :

| Arguments               | Description                                                      |
|-------------------------|------------------------------------------------------------------|
| `admin:admin`           | identification information for elastic database (user:password)  |
| `http://localhost:9200` | url of elastic database                                          |
| `maas-collector-journal`| index in elastic database                                        |
| `{"query": ....}`       | update json description                                          |


Update json description :

```json
{
   "query":{
      "term":{
         "_id":"LTA_Werum"
      }
   },
   "script":"ctx._source.last_collect_date=\"2021-12-15T08:30:00.549Z\";ctx._source.last_date=\"2021-12-15T08:30:00.549Z\""
}
```

where :

| Fields        |   Description                               |
|---------------|---------------------------------------------|
| `_id`         | id in index elastic database                |
| `script`      | attribut with its value to update <br> in example last_collect_date take 2021-12-15T08:30:00.549Z for new value |


For more information about curl command see [curl man](https://curl.se/docs/manpage.html)


## **`With update_journal script`**

To update the dates of an identifier in an index of an elastic database, we can use the update_journal.sh script.
The script is available here [update_journal.sh](../scripts/update_journal.sh)

### **Simple use of the script**

```
./update_journal.sh LTA_Werum 2021-12-15T08:30:00.549Z 2021-12-18T08:30:00.549Z
```

- Default values :

| Value                   |   Description                               |
|-------------------------|---------------------------------------------|
| `http://localhost:9200` | elastic url                                 |
| `admin`                 | elastic user                                |
| `admin`                 | elastic password                            |
| `last_collect_date`     | first field to be updated                   |
| `last_date`             | second field to be updated                  |

- Arguments values :

| Arguments                                              |   Description                               |
|--------------------------------------------------------|---------------------------------------------|
| `first argument` (LTA_Werum in example)                | id in index elastic database                |
| `second argument` (2021-12-15T08:30:00.549Z in example)| value for first field (last_collect_date)   |
| `third argument` (2021-12-15T08:30:00.549Z in example) | value for second field (last_date)          |


### **Use script with full options**

```
./update_journal.sh -e http://localhost:9200 -u admin -p admin -i maas-collector-journal --field1=last_collect_date --field2=last_date LTA_Werum 2021-12-15T08:30:00.549Z 2021-12-17T08:30:00.549Z
```

| Options        |   Description                               |
|----------------|---------------------------------------------|
| `-e`           | elastic url                                 |
| `-u`           | elastic user                                |
| `-p`           | elastic password                            |
| `-i`           | elastic index                               |
| `--field1`     | first field name                            |
| `--field2`     | second field name                           |

It is possible to update only one field with keyword `None` :

```
./update_journal.sh -e http://localhost:9200 -u admin -p admin -i maas-collector-journal --field1=None --field2=last_date LTA_Werum 2021-12-15T08:30:00.549Z
```

For more information, launch helper :
```
./update_journal.sh -h
```
