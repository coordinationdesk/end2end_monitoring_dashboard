#! /bin/bash

source "./functions.sh"

if [ -z "${omcs_ENV_SETTED}" ]; then
    source env.sh
    info "env sourced"
else
    info "env sourced"
fi

if [ -f "${VENV_PATH}/bin/activate" ]; then
    info "Python virtual environement ${VENV_PATH} exist"
else
    info "create python virtual environement ${VENV_PATH}"
    python"${PYTHON_VERSION}" -m venv "${VENV_PATH}"
fi

if [ -n "${VIRTUAL_ENV}" ] && [ "${VIRTUAL_ENV}" = "${VENV_PATH}" ]; then
    echo "Python virtual environement ${VENV_PATH} sourced!"
else
    source "${VENV_PATH}/bin/activate"
fi

build_module maas-model
build_module maas-engine
build_module maas-collector
build_module maas-cds

