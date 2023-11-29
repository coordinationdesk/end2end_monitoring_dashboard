# Single index with no time partitioning

Sometime, time-based index partitioning is not necessary for some needs, like low
cardinality indices that will be separated in many indices containing only one or two
documents. That would be somehow overkill, despite it won't cause any serious issue.

To make DAO classes rely on a single index, it is possible to use meta
attributes in the template to bypass the time-base partitioning system.

The `partition_format` meta attribute of an index stores a string format that will be
used as the parameter of the `datetime.strftime()` method.

Time-based partitioning typically uses time formats like `%Y` or `%Y-%m`, but it is
possible to set any static string that does not contain any time format character. `datetime.strftime()` will then output the string without modification.

The `partition_format` value will then be the **suffix of the index name**.

## Example

Note that the `"single"` value of `partition_format` **is just an example** and can be any valid string value for index naming.

```json
{
  "aliases": {
    "my-document": {}
  },
  "index_patterns": ["my-document-*"],
  "settings": {
    "index": {
      "number_of_shards": 3,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "some_field": {
        "type": "keyword"
      },
      "ingestionTime": {
        "type": "date",
        "format": "date_time",
        "locale": "utc"
      }
    },
    "_meta": {
      "partition_field": "ingestionTime",
      "partition_format": "single"
    }
  }
}
```

`maas-model` will then use the `my-document-single` index as storage for all the
`MyDocument` instances and won't populate a set of indices with low cardinality.

## Renaming existing index

`ElasticSearch` does not provide a built-in function to rename an index. Instead, the existing index has to be copied to a new one using the `_reindex` operation:

```
POST /_reindex
{
  "source": {
    "index": "my-document"
  },
  "dest": {
    "index": "my-document-single"
  }
}
```

And then delete the original index:

```
DELETE /my-document
```

**Double-check the new index before deleting to avoid data losses !**
