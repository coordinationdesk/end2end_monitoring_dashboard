# `XMLExtractor`

```{eval-rst}
:class:`maas_collector.rawdata.extractor.XMLExtractor` uses the :py:mod:`xml.etree.ElementTree` module of the python standard library, so it inherits some limitations of the `xpath` implementation of this module, typically ancestors cannot be selected and requires specific extractor implementation (hopefully easy to create with few lines of code, see :class:`maas_collector.rawdata.extractor.ProductExtractor`).
```

## Basic usage

`XMLExtractor` requires an `attr_map` object as argument. The keys of this object are model field names and the values can be:

- a single string: the text content of the xpath selected node will be extracted
- an object to select a node attribute or to evaluate some python

## Text node content

Text node content is selected with an XPath expression as value of an attribute map:

```json
{
  "attr_map": {
    "someModelFieldName": "path/to/interesting/element"
  }
}
```

Given the following configuration:

```json
{
  "...": "...",
  "extractor": {
    "class": "XMLExtractor",
    "args": {
      "attr_map": {
        "sessionID": "session_id",
        "dataSize": "data_size",
        "timeFinished": "time_finished"
      }
    }
  },
  "...": "..."
}
```

And this input file:

```xml
<DCSU_Session_Information_Block>
    <session_id>L20191003131732787001008</session_id>
    <time_start>2019-12-08T05:08:15Z</time_start>
    <time_stop>2019-12-08T05:12:55Z</time_stop>
    <time_created>2019-12-08T05:08:15Z</time_created>
    <time_finished>2019-12-08T05:12:27Z</time_finished>
    <data_size>8819975080</data_size>
    <dsdb_list>
        <dsdb_name>...</dsdb_name>
        <dsdb_name>...</dsdb_name>
        <dsdb_name>...</dsdb_name>
    </dsdb_list>
</DCSU_Session_Information_Block>
```

The extractor will extract the following object:

```python
{
    "sessionID":  "L20191003131732787001008",
    "dataSize": "8819975080",
    "timeFinished": "2019-12-08T05:12:27Z"
}
```

## Attribute value

Python `elementree` module does not allow the usage of `@` in XPath expressions, but attributes are still accessible in the python node object.

To extract the value of an attribute, provide a configuration object with an `attr` key whose value is the name of the node attribute, with an optional `path` key describing, using an XPath expression, the node path. This `path` key is omitted to extract the root node attribute.

```json
{
  "attr_map": {
    "someModelFieldName": {
      "attr": "nodeAttribute",
      "path": "path/to/interesting/element"
    }
  }
}
```

Given the following configuration:

```json
{
  "...": "...",
  "extractor": {
    "class": "XMLExtractor",
    "args": {
      "attr_map": {
        "productName": {
          "path": "Product",
          "attr": "name"
        },
        "size": "Product/Size"
      }
    }
  },
  "...": "..."
}
```

And this input file:

```xml
<EISP_Output>
    <Product name="S2A_OPER_PRD_L0_DS_SGS__20201201T141044_S20191208T030316">
        <Size>132456789</Size>
    </Product>
</EISP_Output>

```

The extractor will extract the following object:

```python
{
    "productName":  "S2A_OPER_PRD_L0_DS_SGS__20201201T141044_S20191208T030316",
    "size": "132456789"
}
```

## Python expression

> Warning: using this feature can be dangerous. Configuration file shall have strong permissions so introducing malicious code shall not be possible.

> _Special cases aren't special enough to break the rules._ The Zen of Python, by Tim Peters

A model field can be mapped to some python lambda code that will receive the root node as parameter. This can be handy in some border cases, for example populating a model field value with multiple values.

Given this attribute map configuration:

```json
{
  "attr_map": {
    "someListFieldName": {
      "python": "lambda root: [ element.text for element in root.findall('path/to/interesting/element') ]"
    }
  }
}
```

With this input:

```xml
<document>
    <path>
        <to>
            <interesting>
                <element>Text1</element>
                <element>Text2</element>
                <element>Text3</element>
                <element>Text4</element>
            </interesting>
        </to>
    </path>
</document>
```

The extractor will extract the following object:

```python
{
    "someListFieldName": [ "Text1", "Text2", "Text3", "Text4" ]
}
```

## Multiple model instances in one document

When there are many instances to extract and not only a single one, XMLExtractor has the `iterate_node` argument that provides an XPath expression returning a list of nodes. The attribute map will be applied for each of these nodes to create different instances.

Given this configuration:

```json
{
  "...": "...",
  "extractor": {
    "class": "XMLExtractor",
    "args": {
      "attr_map": {
        "name": "element"
      },
      "iterate_node": "path/to/interesting"
    }
  },
  "...": "..."
}
```

With this input:

```xml
<document>
    <path>
        <to>
            <interesting>
                <element>Text1</element>
                <element>Text2</element>
                <element>Text3</element>
                <element>Text4</element>
            </interesting>
        </to>
    </path>
</document>
```

The extractor will extract the following objects:

```python
[
    { "name": "Text1" },
    { "name": "Text2" },
    { "name": "Text3" },
    { "name": "Text4" }
]
```
