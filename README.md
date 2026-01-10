# BotanicalClassifier

Computer vision project built in Python using [Azure AI Custom Vision](https://www.customvision.ai/) for classifying roses, orchids, daisies, carnations and sunflowers.

## Table of Contents

* [Requirements](#requirements)
* [Quick Start](#quick-start)
  * [1. Create a virtual environment](1. Create a virtual environment)
  * [2. Activate the venv](2. Activate the venv)
  * [3. Update pip / setuptools / wheel](3. Update pip / setuptools / wheel)
  * [4. Install the project in development mode](4. Install the project in development mode)
  * [5. Verify installation](5. Verify installation)
  * [6. Update after changes](6. Update after changes)
  * [7. Uninstall (if necessary)](7. Uninstall (if necessary))
  * [Run locally](#run-locally)
* [Contributing](#contributing)
* [License](#license)

## Requirements

* Python 3.11

## Quick Start

### 1. Create a virtual environment

```bash
py -3.11 -m venv .venv
```

### 2. Activate the venv

Windows:

```bash
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Update pip / setuptools / wheel

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 4. Install the project in development mode

```bash
python -m pip install -e ".[dev]"
```

> This installs the local code so changes are immediately available without re-installing:

### 5. Verify installation

```bash
python -m pip show botanical-classifier
```

Check the `Location` field to ensure the package is inside your `.venv` path.

### 6. Update after changes

When you change packaging metadata or dependencies, you can update:

```bash
python -m pip install -e . --upgrade
```

### 7. Uninstall (if necessary)

```bash
python -m pip uninstall botanical-classifier
```

### Run locally

From the repository root, run:

```bash
py ./src/index.py
```

---

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `feature/my-change`.
3. Commit, push, and open a pull request describing the change and reason.

---

## License

This project is available under the **MIT License**.
