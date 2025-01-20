# `JSONExtractor`

```{eval-rst}
:class:`maas_collector.rawdata.extractors.JSONExtractor`
` uses the :py:mod:`json` module of the python standard library to read files and [jsonpath-ng](https://github.com/h2non/jsonpath-ng) module to evaluate JSONPath expression.
```

## Basic usage

`JSONExtractor` requires a `attr_map` object as argument. The keys of this object are model field names and the values are JSONPath expressions.

Given the following extractor configuration:

```json
{
  "...": "...",
  "extractor": {
    "class": "JSONExtractor",
    "args": {
      "attr_map": {
        "fieldName": "$.key1.key2.key3"
      }
    }
  }
}
```

And this input file:

```json
{
  "key1": {
    "key2": {
      "key3": "value"
    }
  }
}
```

The extractor will extract the following object:

```python
{
    "fieldName":  "value"
}
```

> A JSONPath expression that returns a list of nodes will be extracted as a list of values.

## Iterate over a set of objects,

Like `XMLExtractor`, `JSONExtractor` supports node iteration by providing an iterate_nodes JSONPath argument to indicate a list of objects, like in Jira issue extraction :

```json
  "extractor": {
      "class": "JSONExtractor",
      "args": {
          "attr_map": {
              "ticket_id": "`this`.id",
              "spr_key": "`this`.key",
              "spr_title": "`this`.fields.summary",
              "target_production": "`this`.fields.customfield_10043[:].value",
              "data_processor_name": "`this`.fields.customfield_10030.content[:].content[:].text",
              "data_processor_version": "`this`.fields.customfield_10031.content[:].content[:].text",
              "spr_status_id": "`this`.fields.status.id",
              "spr_status": "`this`.fields.status.name",
              "related_ar":"`this`.fields.issuelinks[0].inwardIssue|outwardIssue.id",
              "end_date": "`this`.fields.customfield_10049",
              "reportName": "`this`.self"
          },
          "iterate_nodes": "$.issues",
          "allow_partial": true
      }
  }
```
