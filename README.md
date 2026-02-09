# BotanicalClassifier

Desktop application that classifies five flower types using an Azure Custom Vision model: **roses**, **orchids**, **daisies**, **carnations**, and **sunflowers**. The app provides a friendly Tkinter GUI to collect survey responses, upload and store images locally, and request real-time predictions from Azure Custom Vision.

---

## Table of Contents

* [Use case & motivation](#use-case--motivation)
* [Features](#features)
* [Architecture overview](#architecture-overview)
* [Installation](#installation)
  * [Requirements](#requirements)
  * [Azure Custom Vision setup](#azure-custom-vision-setup)
  * [`.env` configuration](#env-configuration)
  * [Virtual environment setup](#virtual-environment-setup)
  * [Install dependencies](#install-dependencies)
  * [Run locally](#run-locally)
  * [Update after changes (optional)](#update-after-changes-optional)
* [Model evaluation & metrics](#model-evaluation--metrics)
* [Scalability & extensibility](#scalability--extensibility)
* [Limitations & risks](#limitations--risks)
* [Attribution & credits](#attribution--credits)
* [Contributing](#contributing)
* [License](#license)

---

## Use case & motivation

The Jardín Botánico Nacional is conducting a nationwide research project to estimate how many flowers of each type people keep in their homes. For this effort, the botanic garden created an online survey where participants fill a short form and upload a photograph of the plants they keep at home. All submitted photos are stored in a local folder on the botanic garden's research computer. Photo filenames follow the convention `flower_survey_xx.png`.

The garden needs to homologate these photos and assign a flower type to each image. The target classes are: **roses**, **orchids**, **daisies**, **carnations**, and **sunflowers**. Manual labeling at scale is time-consuming and staff resources are limited, so they require an automated solution to speed up classification and reduce human workload.

This repository implements a desktop application that supports that workflow: image ingestion, local storage, a survey GUI, and an integration with Azure Custom Vision to obtain and display model predictions.

---

## Features

- Lightweight desktop GUI with Tkinter for:
  - Filling a short survey (name, surname, address) and attaching a flower image.
  - Saving images and structured records locally for research and audit.
  - Sending images to **Azure Custom Vision** and showing sorted predictions by confidence.
  - Browsing/searching stored survey records, paginated view, and manual classification trigger.
- **Local-first design**: images and JSON records are stored locally.
- **Internationalization (i18n)**: English and Spanish language support.

---

## Architecture overview

The project follows a layered design that separates concerns between presentation, business logic, models, and common utilities. Each module is designed with clear responsibilities to ensure maintainability and scalability.

### High-level structure

```md
BotanicalClassifier/
├── dataset/
├── src/
│   ├── common/    # Shared utilities and configuration
│   ├── gui/       # Tkinter UI components
│   ├── models/    # Data models
│   ├── resources/ # Static assets and content
│   ├── services/  # Business logic layer
│   └── app.py     # Application entry point
├── pyproject.toml
└── README.md
```

### Layer responsibilities

#### Presentation layer (`gui/`)

User interface built with Tkinter, organized into three main components:

- **assets/**: Image resource management.
- **pages/**: Application screens.
- **styles/**: Style definitions of all UI components.

#### Business logic (`services/`)

Handles core application functionality:

- **i18n_service**: Internationalization management for language support.
- **predictor_service**: Integration wrapper for Azure Custom Vision API calls and response processing.
- **records_service**: Persistent storage operations using JSON-based local storage.
- **form_service**: Validation logic for the survey form.
- **about_service**: Dynamic content loader for About sections.

#### Data layer (`models/`)

Data models representing core domain entities:

- **prediction_model**: Structured representation of classification results from the Azure API.
- **record_model**: Schema for persisted records with prediction metadata.

#### Shared (`common/`)

Shared utilities and application-wide configuration:

- **config**: Environment variables.
- **constants**: Application-wide constants.
- **paths**: Centralized path resolution for resources and local storage.
- **utils**: Helper functions for common operations across modules.

#### Resources (`resources/`)

Static and dynamic content assets:

- **i18n/**: Translation catalogs in JSON format for supported languages.
- **content/**: Static content for supported languages.
- **images/**: Static images.
- **local/**: Local storage directory for user survey data.

### Dataset organization

Training images are organized by class:

```md
dataset/
  ├── carnations/
  ├── daisies/
  ├── orchids/
  ├── roses/
  └── sunflowers/
```

All images follow the `flower_survey_xx.png` naming convention.

---

## Installation

### Requirements

* Python 3.11
* Azure Custom Vision subscription.

### Azure Custom Vision setup

#### Create a Custom Vision Project

1. Sign in to Azure Custom Vision at [https://www.customvision.ai](https://www.customvision.ai)
2. Click **New Project**:
   - Name: `botanical-classifier`
   - Project Type: **Classification**
   - Classification Type: **Multiclass**
   - Domain: Select appropriate for flower images.
   - Resource: Create or select existing.

#### Train the model

1. For each class (`roses`, `orchids`, `daisies`, `carnations`, `sunflowers`) upload representative images from `dataset/` folders to corresponding tags.
2. Remove duplicates, low-quality, or incorrectly-tagged images.
3. Click **Train** > **Quick Training**.
4. Publish the iteration with a descriptive **Published Name**.

#### Get credentials

- Copy `Prediction Key` and `Endpoint URL` from **Settings**.
- Copy `Project ID` from **Azure Portal**.
- Note your `Published Name` from the published iteration.

### `.env` configuration

Create a `.env` under `src/common/` containing your **Custom Vision** credentials:

```env
CUSTOM_VISION_KEY='your-prediction-key'
CUSTOM_VISION_ENDPOINT='your-prediction-endpoint'
CUSTOM_VISION_PROJECT_ID='your-project-id'
CUSTOM_VISION_PUBLISHED_NAME='your-published-iteration-name'
```

### Virtual environment setup

From the repository root:

```bash
# Create virtual environment
py -3.11 -m venv .venv

# Activate (Windows)
.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate

```

### Install dependencies

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

### Run locally

```bash
py ./src/app.py
```

### Update after changes (optional)

If you modify dependencies:

```bash
python -m pip install -e . --upgrade
```

---

## Model evaluation & metrics

### Overall performance

The published iteration demonstrates strong classification performance across the validation set:

![Overall metrics](docs/metrics/overall_metrics.png)

### Per-Class performance

Individual class metrics reveal which categories are well-represented and which may benefit from additional training data:

![Per-Class Performance](docs/metrics/performance_per_tag.png)

---

## Scalability & extensibility

The application is designed for growth:

| Extension point | Detail |
| --------------- | -------------- |
| **Additional pages** | Adding new page classes in `gui/pages/` with simple navigation is straightforward. |
| **More languages** | Adding new languages (`xx.json` catalogs) to `resources/i18n/` just requieres a small enum update. |
| **Themes** | Centralized styles in `gui/styles/` enable dark/light mode support without large code changes. |
| **New flower types** | Adding new tags to the Custom Vision model is straightforward; UI adapts automatically. |
| **Larger datasets / Improved Models** | As dataset size increases or a different model is adopted, the prediction API remains compatible. |
| **Cloud storage** | The `RecordsService` and `Paths` encapsulates storage logic, enabling straightforward migration to cloud-based solutions. |

---

## Limitations & risks

- Single-user desktop design, not intended for concurrent multi-user usage.
- Local storage grows with survey submissions.
- Requires network connectivity and Azure Custom Vision subscription.
- Free-tier limitations or constrained subscription limits may restrict the number of monthly predictions.
- Classification accuracy may be affected by poor image resolution, blur, or non-standard formats.

---

## Attribution & credits

### Visual design & content

The application's visual identity and informational content are inspired by and adapted from the **Jardín Botánico Nacional** (National Botanical Garden of the Dominican Republic):

- **UI design**: Layout and color scheme inspired by [jbn.gob.do](https://www.jbn.gob.do/).
- **Branding assets**: Logo, banner images, and iconography sourced from official website.
- **About content**: Terms, policies, and informational sections translated and adapted from official documentation.

This is an educational project demonstrating Azure Custom Vision integration. All content from JBN is used respectfully for demonstration purposes.

### Dataset

- **Image source**: [Pexels](https://www.pexels.com/)
- **Curation**: Abel Eduardo Martínez Robles

### Technology

- **Prediction service**: Azure Custom Vision
- **Application Development**: Roniel Antonio Sabala Germán

---

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository.
2. Create a feature branch: `feature/my-change`.
3. Commit, push, and open a pull request describing the change and reason.

> Please, ensure your code follows the existing style and includes appropriate documentation.

---

## License

This project is available under the **MIT License**.
