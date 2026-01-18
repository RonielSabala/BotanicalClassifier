# BotanicalClassifier

Desktop application that classifies five flower types: **roses**, **orchids**, **daisies**, **carnations**, and **sunflowers**. The app provides a friendly Tkinter GUI to collect survey responses, upload and store images locally, call [Azure AI Custom Vision](https://www.customvision.ai/) for predictions, and manage survey records.

The visual and content design was inspired by the official website of the [Jardín Botánico Nacional](https://www.jbn.gob.do/).

---

## Table of Contents

* [Case study & motivation](#case-study--motivation)
* [Features](#features)
* [Architecture Overview](#architecture-overview)
  * [Repository Structure](#repository-structure)
  * [Module Structure](#module-structure)
  * [Dataset & naming convention](#dataset--naming-convention)
* [Requirements](#requirements)
* [Installation](#installation)
  * [`.env` configuration](#env-configuration)
  * [Create & activate virtual environment](#create--activate-virtual-environment)
  * [Install in development mode](#install-in-development-mode)
  * [Run locally](#run-locally)
  * [Update after changes (Optional)](#update-after-changes-optional)
* [Model evaluation & metrics](#model-evaluation--metrics)
  * [Overall model metrics](#overall-model-metrics)
  * [Performance Per-tag](#performance-per-tag)
* [Scalability & extensibility](#scalability--extensibility)
* [Limitations & risks](#limitations--risks)
* [Contributing](#contributing)
* [Credits](#credits)
* [License](#license)

---

## Case study & motivation

The Jardín Botánico Nacional is conducting a nationwide research project to estimate how many flowers of each type people keep in their homes. For this effort, the botanic garden created an online survey where participants fill a short form and upload a photograph of the plants they keep at home. All submitted photos are stored in a local folder on the botanic garden's research computer. Photo filenames follow the convention `flower_survey_xx.png`.

The garden needs to homologate these photos and assign a flower type to each image. The target classes are: **roses**, **orchids**, **daisies**, **carnations**, and **sunflowers**. Manual labeling at scale is time-consuming and staff resources are limited, so they require an automated solution to speed up classification and reduce human workload.

---

This repository contains the desktop application that implements that automation: image ingestion, local storage conventions, a GUI for survey management, and the Custom Vision integration for predictions.

---

## Features

* Lightweight desktop GUI with Tkinter for:
  * Filling a short survey (name, surname, address) and attaching a flower image.
  * Saving images locally in a structured folder.
  * Sending images to **Azure Custom Vision** and **displaying prediction** tables sorted by confidence.
  * Browsing/searching stored survey records, paginated view, and manual classification trigger.

* **Local-first design**: images and records are stored locally.
* **Internationalization** (i18n) with built-in English and Spanish language support.
* **Modular design** that separates GUI, services, and models for easier maintenance.

---

## Architecture Overview

The application follows a layered architecture that separates concerns between presentation, business logic, and data management. Each module is designed with clear responsibilities to ensure maintainability and scalability.

### Repository Structure

```md
BotanicalClassifier/
├── dataset/
├── src/
│   ├── common/
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── paths.py
│   │   └── utils.py
│   ├── gui/
│   │   ├── assets/
│   │   ├── pages/
│   │   └── styles/
│   ├── models/
│   │   ├── prediction_model.py
│   │   └── record_model.py
│   ├── resources/
│   │   ├── content/
│   │   ├── i18n/
│   │   ├── images/
│   │   └── local/
│   ├── services/
│   │   ├── about_service.py
│   │   ├── form_service.py
│   │   ├── i18n_service.py
│   │   ├── predictor_service.py
│   │   └── records_service.py
│   └── app.py
├── pyproject.toml
└── README.md
```

### Module Structure

#### `src/gui/`

User interface layer built with Tkinter, organized into three main components:

* **assets/**: Image resource management.
* **pages/**: Application screens.
* **styles/**: Style definitions of all UI components.

#### `src/services/`

Business logic layer that handles core application functionality:

* **i18n_service**: Internationalization management for language support.
* **predictor_service**: Integration wrapper for Azure Custom Vision API calls and response processing.
* **records_service**: Persistent storage operations using JSON-based local storage.
* **form_service**: Validation logic for the survey form.
* **about_service**: Dynamic content loader for About sections.

#### `src/models/`

Data models representing core domain entities:

* **prediction_model**: Structured representation of classification results from the Azure API.
* **record_model**: Schema for persisted records with prediction metadata.

#### `src/common/`

Shared utilities and application-wide configuration:

* **config**: Environment variables.
* **constants**: Application-wide constants.
* **paths**: Centralized path resolution for resources and local storage.
* **utils**: Helper functions for common operations across modules.

#### `src/resources/`

Static and dynamic content assets:

* **i18n/**: Translation catalogs in JSON format for supported languages.
* **content/**: About sections content for supported languages.
* **images/**: Application icon, banner, and placeholder image.
* **local/**: Runtime-generated directory for user survey data.

### Dataset & naming convention

The training dataset is organized by flower categories, each one with at least **55 unique images**:

```md
dataset/
  ├── carnations/
  ├── daisies/
  ├── orchids/
  ├── roses/
  └── sunflowers/
```

Images are named using the application convention so that locally saved survey photos follow:

```md
flower_survey_xx.png
```

---

## Requirements

* Python 3.11
* Azure Custom Vision subscription.

---

## Installation

### `.env` configuration

Create a `.env` under `src/common/` containing your Custom Vision credentials:

```env
CUSTOM_VISION_KEY='your-prediction-key'
CUSTOM_VISION_ENDPOINT='your-prediction-endpoint'
CUSTOM_VISION_PROJECT_ID='your-project-id'
CUSTOM_VISION_PUBLISHED_NAME='your-published-iteration-name'
```

#### How to get credentials

1. Sign in to Azure Custom Vision at [https://www.customvision.ai](https://www.customvision.ai)
2. Create a **Custom Vision project**:
   * Click **New Project**.
   * Choose a Name (e.g., `botanical-classifier`).
   * Select **Classification** > **Multiclass**.
   * Select a domain appropriate for the flower images.
   * Choose an appropriate resource (or create one) for training.
3. For each class (`roses`, `orchids`, `daisies`, `carnations`, `sunflowers`), upload representative images from `dataset/` into the corresponding tag.
4. Remove duplicates, low-quality, or incorrectly-tagged photos.
5. To train the model: **Train** > **Quick Training**.
6. Once trained and tested, **publish** the trained iteration and provide a descriptive `Published Name`.
7. In the Custom Vision **Resource Keys / Endpoint** or in the Azure portal, copy the `Prediction Key` and `Endpoint URL`.
8. Go to **Azure portal** > **Settings** and copy the `Project Id`.

### Create & activate virtual environment

From the repository root:

```bash
py -3.11 -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

```

### Install in development mode

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

### Run locally

```bash
py ./src/app.py
```

### Update after changes (Optional)

If you change packaging metadata or dependencies, you can update with:

```bash
python -m pip install -e . --upgrade
```

---

## Model evaluation & metrics

### Overall model metrics

The screenshot below shows the model's overall Precision, Recall, and Average Precision for the published iteration. These metrics summarize the model's capacity to correctly identify the correct flower type on our validation set.

![Overall metrics](docs/metrics/overall_metrics.png)

### Performance Per-tag

The per-tag table indicates which classes are well represented and which require additional training data.

![Performance per-tag](docs/metrics/performance_per_tag.png)

---

## Scalability & extensibility

This application supports several straightforward scalability paths:

* **Add more pages and UI flows**: The `src/gui/pages/` directory uses a page class pattern; adding pages, and registering them with simple navigation is straightforward.
* **More languages**: The `src/resources/i18n/` JSON catalogs and `I18nService` enable new languages by adding additional `xx.json` files and a small enum update.
* **Themes & styles**: Styles are centralized under `src/gui/styles/` and can be extended to add themes (dark/light) without large code changes.
* **Model tags**: Custom Vision supports adding tags. The app's data model and UI are tag-agnostic; adding new tags to the model and dataset is possible without deep changes.
* **Larger datasets / improved models**: As dataset size increases or a different model export options is adopted, the same prediction API remains compatible.
* **Storage backends**: The `RecordsService` and `Paths` module centralize I/O location logic; storage can be refactored to cloud by swapping the storage implementation without changing GUI code.

---

## Limitations & risks

* **High concurrency or multi-client access**: The current design assumes single-user desktop usage.
* **Limited class set**: the current model supports only five flower types.
* **Dependency on internet & Azure**: the application requires network access and an Azure Custom Vision subscription.
* **Image quality sensitivity**: poor resolution, blur, or non-standard formats may cause incorrect classifications.
* **Prediction quotas**: free-tier limitations or constrained subscription limits may restrict the number of monthly predictions.

---

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `feature/my-change`.
3. Commit, push, and open a pull request describing the change and reason.

---

## Credits

* **Design inspiration**: Jardín Botánico Nacional - [https://www.jbn.gob.do/](https://www.jbn.gob.do/).
* **Dataset source**: Pexels - [https://www.pexels.com/](https://www.pexels.com/).
* **Dataset curation & development**: Abel Eduardo Martínez Robles.
* **Model service**: Azure AI Custom Vision.

---

## License

This project is available under the **MIT License**.
