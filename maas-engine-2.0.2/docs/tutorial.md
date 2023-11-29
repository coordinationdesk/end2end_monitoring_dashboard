# Tutorial

This section will explain steps to set up a basic project.

## Requirements

- Python >= 3.9

## Project initialization

Let's create a `maas-tutorial` project.

### Workspace

Create a workspace root directory that will contain:

- Python virtual environment
- `maas-tutorial` code repository clone
- `maas-deploy-tutorial` settings repository clone

For instance:

```bash
mkdir ~/maas-workspace
cd ~/maas-workspace
```

Create a virtual environment and activate it:

```bash
python -m venv venv
source ./venv/bin/activate
```

### Scaffolding

Initializing a Python project from scratch can be time-consuming, so using a scaffolding tool is highly recommended.

[PyScaffold](https://pyscaffold.org/en/stable/) has a lot of advantages when integrated to continuous integration system as it provides common [`tox`](https://tox.wiki/) tasks for the development process: package building and publication, documentation generation, running tests in a separated environment ...

Install `tox`, `pyscaffold` and `pyscaffoldext-markdown` (Markdown is the official MAAS documentation format) with `pip`:

```bash
pip install tox pyscaffold pyscaffoldext-markdown
```

Then, in the workspace directory, call `putup` with the following options:

```bash
putup -l Apache-2.0 --markdown -d "MAAS tutorial project" --no-skeleton --gitlab maas-tutorial
```

Will output:

```

A pre-commit hook was installed in your repo.
It is a good idea to update the hooks to the latest version:

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

done! 🐍 🌟 ✨

```

The `maas-tutorial` directory have then the following structure:

```bash
maas-tutorial/
├── AUTHORS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── docs
│   ├── authors.md
│   ├── changelog.md
│   ├── conf.py
│   ├── contributing.md
│   ├── index.md
│   ├── license.md
│   ├── Makefile
│   ├── readme.md
│   ├── requirements.txt
│   └── _static
├── LICENSE.txt
├── pyproject.toml
├── README.md
├── setup.cfg
├── setup.py
├── src
│   └── maas_tutorial
│       └── __init__.py
├── tests
│   └── conftest.py
└── tox.ini
```

There are many generated Markdown files that needs to be filled so the project documentation is consistent.

### Additional directories

MAAS project have a common package tree scheme:

- `cli` package for command-line console script
- `engines` package that contains engine implementation, grouped by responsibilities:
  - `engines/compute` for data computing
  - `engines/reports` for data consolidation
- `lib` for shared functions
- `model` contains all DAO classes
- `resources` to store static data
- `update` for data migration tools at deployment time

Create the directories in the `maas_tutorial` module source tree:

```bash
cd maas-tutorial/src/maas_tutorial
mkdir -p cli engines/reports engines/compute lib model resources update
```

`src` subdirectory will have the following structure:

```bash
❯ tree src/
src/
└── maas_tutorial
    ├── cli
    ├── engines
    │   ├── compute
    │   └── reports
    ├── __init__.py
    ├── lib
    ├── model
    ├── resources
    └── update
```

### git repository setup

As PyScaffold initializes the git repository, remote origin has to be specified (replace url with the correct settings)

```bash
git remote add origin git@github.com:User/maas-tutorial.git
```

Or

```bash
git remote set-url origin git@github.com:User/maas-tutorial.git
```

Initialize `git flow`:

```bash
cd maas-tutorial
git flow init
```

This will ask for many settings: default values are ok and do not need customization.
After this, the current checkout will refer to the develop branch.
