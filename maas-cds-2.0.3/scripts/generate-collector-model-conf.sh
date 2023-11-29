#!/bin/bash

TEMPLATE_FOLDER=${1:-"/app/resources/templates"}
python -m maas_model.generator.jsongen ${TEMPLATE_FOLDER}/raw-data-*_template.json