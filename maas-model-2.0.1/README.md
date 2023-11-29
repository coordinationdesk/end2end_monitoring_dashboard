# maas-model

This project provides various base classes and DAO code generation from index templates.

## MAASMessage

`MAASMessage` class stores some attributes for exchange between MAAS components through the AMQP bus : `document_class`, `document_ids`, `document_indices`, and `date` (defaults to now).

The `to_dict()` method outputs a dictionary ready for serialization.

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
