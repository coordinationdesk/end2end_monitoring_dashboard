# `LogExtractor`

```{eval-rst}
:class:`maas_collector.rawdata.extractors.LogExtractor`
` uses the :py:mod:`re` module of the python standard library to extract data using regex with python group dict.
```

## Basic usage

`LogExtractor` does not require a `attr_map` object as argument but a `pattern` string containing the regular expression for line matching with named groups for attribute mapping.

Given the following extractor configuration:

```json
{
  "...": "...",
  "extractor": {
    "class": "LogExtractor",
    "args": {
      "pattern": "\\[(?P<logDate>\\d{4}-\\d{2}-\\d{2}\\s\\d{2}:\\d{2}:\\d{2}\\.\\d{3})\\]\\[(?P<level>.+)\\]\\s*(?P<message>.+)"
    }
  }
}
```

And this input file:

```
[2021-08-23 17:59:23.042][INFO] A test log
[2021-08-23 18:01:28.401][ERROR] A test error message
```

The extractor will extract the following objects:

```python
[
    {
        "logDate":  "2021-08-23 17:59:23.042",
        "level": "INFO",
        "message": "A test log"

    },
    {
        "logDate":  "2021-08-23 18:01:28.401",
        "level": "ERROR",
        "message": "A test error message"

    },
]
```

## Advices to build regex

Writing directly the regular expression in the configuration file may be tough due to the number of characters to escape: double quote and anti-slash.

So it is convenient to:

- use [pythex](https://pythex.org/) online tool
- write a tiny Python script or use a Python like `ipython` and write the pattern using raw strings (`r` prefixed) that does not require escaping anti-slashes and allows writing multi-lines with concatenation.

```python
import re

sample = "[2021-08-23 17:59:23.042][INFO] A test log"

pattern = r"\[(?P<logDate>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3})\]"
    + r"\[(?P<level>.+)\]\s*(?P<message>.+)"


# this will output {'logDate': '2021-08-23 17:59:23.042', 'level': 'INFO', 'message': 'A test log'}
print(re.match(pattern.sample).groupdict())


# this will output \\[(?P<logDate>\\d{4}-\\d{2}-\\d{2}\\s\\d{2}:\\d{2}:\\d{2}.\\d{3})\\]\\[(?P<level>.+)\\]\\s*(?P<message>.+)
# copy-paste this string to the configuration file
print(pattern.replace("\\", "\\\\"))
```
