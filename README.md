# BotanicalClassifier

Computer-vision desktop application that classifies five flower types: **roses**, **orchids**, **daisies**, **carnations** and **sunflowers**. The application provides a simple Tkinter GUI to collect survey data, upload images, store images locally and call [Azure AI Custom Vision](https://www.customvision.ai/) for predictions.

---

## Table of Contents

* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
  * [`.env` configuration](env-configuration)
  * [Create a virtual environment](create-venv)
  * [Activate the venv](activate-venv)
  * [Upgrade packaging basics](upgrade-packaging-basics)
  * [Install project in development mode](install-project-in-dev-mode)
  * [Verify installation](verify-installation)
  * [Update after changes (Optional)](update-after-changes)
  * [Run locally](#run-locally)
* [Dataset & data format](#dataset--data-format)
* [Limitations & risks](#limitations--risks)
* [Contributing](#contributing)
* [Credits](#credits)
* [License](#license)

---

## Features

* Desktop GUI built with Tkinter to:
  * Complete a short survey and upload a flower image.
  * Save uploaded images locally.
  * Send images to **Azure Custom Vision** and **display predictions**.
  * View, search and manage stored survey records.

* **Prediction output**: a probability table sorted by confidence, with the top result highlighted.

---

## Requirements

* Python 3.11

---

## Installation

### `.env` configuration

Create a `.env` file at `src/common/.env` with the keys shown below.

```env
CUSTOM_VISION_KEY='your-prediction-key'
CUSTOM_VISION_ENDPOINT='your-prediction-endpoint'
CUSTOM_VISION_PROJECT_ID='your-project-id'
CUSTOM_VISION_PUBLISHED_NAME='your-published-iteration-name'
```

### Create a virtual environment

From the repository root, run:

```bash
py -3.11 -m venv .venv
```

### Activate the venv

**Windows**:

```bash
.venv\Scripts\Activate.ps1
```

**Linux / macOS**:

```bash
source .venv/bin/activate
```

### Upgrade packaging basics

```bash
python -m pip install --upgrade pip setuptools wheel
```

### Install project in development mode

```bash
python -m pip install -e ".[dev]"
```

> This installs the local code so changes are immediately available without re-installing.

### Verify installation

```bash
python -m pip show botanical-classifier
```

Check the `Location` field to ensure the package is inside your `.venv` path.

### Update after changes (Optional)

If you change packaging metadata or dependencies, you can update:

```bash
python -m pip install -e . --upgrade
```

### Run locally

From the repository root with the venv activated, run:

```bash
py ./src/app.py
```

---

## Dataset & data format

Images used to build and validate the model were collected from **Pexels** and curated into a dataset of at least **60 images per flower class**. Images were saved under the naming convention:

```md
flower_survey_xx.png
```

This convention is used by the application to ingest and normalize incoming user images.

---

## Limitations & risks

* **Dependency on internet & Azure**: the application requires network access and Azure Custom Vision availability.
* **Limited class set**: the current model supports only five flower types.
* **Image quality sensitivity**: poor resolution, blur, or non-standard formats may cause incorrect classifications.
* **Prediction quotas**: free-tier limitations or constrained subscription limits may restrict the number of monthly predictions.
* **App bugs**: possible failures in the desktop UI.

---

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `feature/my-change`.
3. Commit, push, and open a pull request describing the change and reason.

---

## Credits

* **Images**: Pexels.
* **Dataset creation**: Abel Eduardo Martínez Robles.
* **Model service**: Azure AI Custom Vision.

---

## License

This project is available under the **MIT License**.
