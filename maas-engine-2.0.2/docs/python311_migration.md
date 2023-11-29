# Moving to Python 3.11

## Introduction

This document presents some evolution appeared between Python 3.9 and 3.11 that are useful to the MAAS project.

This does not mean to be exhaustive at all, and is clearly opinionated.

For all changes between all Python versions, refer to [this document of the official documentation](https://docs.python.org/3.11/whatsnew/index.html)

### Motivation

As MAAS evolves through time, the old Docker Python 3.9 base image becomes obsolete and has an increasing volume of vulnerabilities.

As Python now adopts a per-year release plan, 3.9 version will become obsolete in _not-so-many years_ as this document is written (2023).

Moving to 3.11 version will make MAAS project reliable for at least the next 4 years (up to 2027).

Security concerns will appear in the future, so migration to a newer version may happen if needed.

### Roadmap

Version of maas-engine 1.17 has been developed for Python 3.9, so moving to 3.11 has to include evolution from 3.10.

maas-engine 1.17 has no problem to run out the box with 3.11 (it has been anticipated and fixed _a long ago_), but maas-cds 1.18 depends on Shapely 1.8.2 which has no binary distribution in pip for Py3.11, so it has been upgraded to 2.0.1 that lead to a regression in a test hosting a comparison that became false due to float epsilon (a temporary fix has been done until full investigation).

However, new development have to take advantage of the new features when they provide improvements in performance, modularity or **readiness**.

## Features

### Better stack trace

What fails precisely is now clearly underlined in the stack trace, speeding up problem resolution:

```bash
Traceback (most recent call last):
  File "/home/fgirault/Code/MAAS/maas-collector/src/maas_collector/rawdata/collector/ftpcollector.py", line 265, in ingest_ftp_file
    self.extract_from_file(
  File "/home/fgirault/Code/MAAS/maas-collector/src/maas_collector/rawdata/collector/filecollector.py", line 463, in extract_from_file
    for success, info in parallel_bulk(
  File "/home/fgirault/Code/MAAS/venvX/lib/python3.11/site-packages/elasticsearch/helpers/actions.py", line 472, in parallel_bulk
    for result in pool.imap(
  File "/usr/lib/python3.11/multiprocessing/pool.py", line 873, in next
    raise value
  File "/usr/lib/python3.11/multiprocessing/pool.py", line 125, in worker
    result = (True, func(*args, **kwds))
                    ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/multiprocessing/pool.py", line 144, in _helper_reraises_exception
    raise ex
  File "/usr/lib/python3.11/multiprocessing/pool.py", line 391, in _guarded_task_generation
    for i, x in enumerate(iterable):
  File "/home/fgirault/Code/MAAS/venvX/lib/python3.11/site-packages/elasticsearch/helpers/actions.py", line 155, in _chunk_actions
    for action, data in actions:
  File "/home/fgirault/Code/MAAS/maas-collector/src/maas_collector/rawdata/model.py", line 227, in __iter__
    for data_extract in self.config.extractor.extract(
  File "/home/fgirault/Code/MAAS/maas-collector/src/maas_collector/rawdata/extractor/xml.py", line 131, in extract
    tree = ET.parse(path)
           ^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/xml/etree/ElementTree.py", line 1218, in parse
    tree.parse(source, parser)
  File "/usr/lib/python3.11/xml/etree/ElementTree.py", line 580, in parse
    self._root = parser._parse_whole(source)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 1, column 0
```

### Parenthesized context managers

```python
with (CtxManager() as example):
    ...

with (
    CtxManager1(),
    CtxManager2()
):
    ...

with (CtxManager1() as example,
      CtxManager2()):
    ...

with (CtxManager1(),
      CtxManager2() as example):
    ...

with (
    CtxManager1() as example1,
    CtxManager2() as example2
):
    ...
```

### Exceptions

#### Notes

```python
>>> try:
...     raise TypeError('bad type')
... except Exception as e:
...     e.add_note('Add some information')
...     raise
...
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: bad type
Add some information
```

#### Groups

```python
>>> eg = ExceptionGroup(
...     "one",
...     [
...         TypeError(1),
...         ExceptionGroup(
...             "two",
...              [TypeError(2), ValueError(3)]
...         ),
...         ExceptionGroup(
...              "three",
...               [OSError(4)]
...         )
...     ]
... )
```

Handling with `except*`:

```python
try:

    raise ExceptionGroup("eg",

        [ValueError(1), TypeError(2), OSError(3), OSError(4)])

except* TypeError as e:

    print(f'caught {type(e)} with nested {e.exceptions}')

except* OSError as e:

    print(f'caught {type(e)} with nested {e.exceptions}')


caught <class 'ExceptionGroup'> with nested (TypeError(2),)
caught <class 'ExceptionGroup'> with nested (OSError(3), OSError(4))
  + Exception Group Traceback (most recent call last):
  |   File "<stdin>", line 2, in <module>
  | ExceptionGroup: eg
  +-+---------------- 1 ----------------
    | ValueError: 1
    +------------------------------------
```

### f-strings dump

```python
import dataclasses

@dataclasses.dataclass
class A:
    a: str
    b: int

a = A("plop", 3)

print(f"{a=}")

# output: "a=A(a='plop', b=3)"
```

### match / case

### Walrus operator

(oops it's already in 3.9)

### Typing

```python
def square(number: int | float) -> int | float:
    return number ** 2
```
