# maas-model

This project provides various base classes and DAO code generation from index templates.

## Message Model

### MAASBaseMessage

`MAASBaseMessage` class stores some extra attributes for exchange between MAAS components through the AMQP bus : `ancestor_ids` (list of previous message ids), `message_id` (id of the message), `date`, `pipeline` (List of all engine id crossed by the message since the first ancestor_ids), `force`

### MAASMessage

MAASMessage are based on MAASBaseMessage.
`MAASMessage` class stores some extra attributes for exchange between MAAS components through the AMQP bus : `document_class`, `document_ids`, `document_indices`

The `to_dict()` method outputs a dictionary ready for serialization.

### Custom Message

It is possible to extend MAASBaseMessage, to provide extra information for a custom engine.

```python
@dataclasses.dataclass
class MAASCustomMessage(MAASBaseMessage):

    custom_field: str = "default_value"
```

Next you have to provide the custom class for your custom engine that consume `MAASCustomMessage`
It will allow the engine to deserialize correctly the message (by default `PAYLOAD_MODEL = MAASMessage`)

```python
from maas_model import MAASCustomMessage
from maas_engine.engine.base import Engine

class CustomEngine(Engine):

    PAYLOAD_MODEL = MAASCustomMessage
```

## DAO Code generation

`maas-model` generators output to the standard output, so it is recommended to redirect the output to a file.

### DAO classes

```bash
python -m maas_model.generator.pygen maas-project/resources/*_template.json > maas-project/src/maas_project/model/generated.py
```

Template files starting with `raw-data` will generate classes that inherit `MaasRawDocument` while others will inherit `MaasDocument`

### maas-collector model description

Note it is better to provide only files with `raw-data-` prefix as others may not be useful for the collector.

```bash
python -m maas_model.generator.jsongen maas-project/resources/raw-data-*_template.json > maas-project/charts/collector/conf/maas-project-model.json
```

## Inheritance

To override generated classes with inheritance follow this example :

Put `generated.py` file in `maas_cds.model`

Create `__init__.py` file in `maas_cds.model`

```python
"""contains all the model classes"""

# import generated DAO classes
from maas_cds.model.generated import *

# import custom DAO implementations
from maas_cds.model.custom import *
```

The `custom` module contains classes that inherit generated classes

order matter in order to use custom class if any when importing the module

Sample of generated class inheritance :

Create `custom.py` file in `maas_cds.model`

```python
import maas_cds.model.generated as generated

__all__ = ["PripProduct"]


class PripProduct(generated.PripProduct):
    pass

class CdsProduct(generated.CdsProduct):

    def add_data_provider(self, service_type, publication_date):
        if not self.data_providers:
            self.data_providers = []
        data_provider = generated.CdsProductDataProviders()

        data_provider.service_type = service_type
        data_provider.publication_date = publication_date
        #TODO fill other attrs

        self.data_providers.append(data_provider)

```
