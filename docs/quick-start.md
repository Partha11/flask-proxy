---
title: Quick Start
layout: home
nav_order: 3
description: LabelBridge is a Flask middleware that seamlessly connects Label Studio with NLP models and LLMs, handling data transformations to enable smooth automated annotations.
---

# Quick Start Guide

This guide will help you get LabelBridge up and running quickly to automate your Named Entity Recognition (NER) data annotation process. We'll cover the essential configuration steps and how to connect Label Studio to your LabelBridge instance.

## Key Features for Quick Start

LabelBridge is primarily engineered to streamline NER data annotation. It intelligently processes outputs from your models, supporting both word-level and subword-level tokenization to generate precise annotations in Label Studio.

## Initial Configuration

Before running LabelBridge, you'll need to set up or verify a few configuration files.

### Label Studio Configuration Samples

LabelBridge includes sample configuration files for Label Studio to get you started. These are located under the `storage/label_studio/` directory:

- **config.xml:** This file contains the Label Studio project configuration, defining the labeling interface (e.g., text, labels, regions).
- **labels.json:** This file defines the specific labels (e.g., PERSON, ORG, LOC) that your NER models will predict and Label Studio will display.

{: .note-title }
> Action Required
>
> These samples provide a basic setup. You should replace or modify these files with your own Label Studio project's config.xml and the labels.json tailored to your specific NER schema. Ensure these files accurately reflect the annotation task you intend to perform.

### LLM System Prompts (Currently Disabled)

For future Large Language Model (LLM) integration, system prompts can be configured in the `storage/llm/prompts.json` file. This file will allow you to define how LabelBridge interacts with LLMs for generating annotations or insights.

{: .note}
In the current version, LLM functionality has been temporarily disabled due to an identified bug. This feature will be re-enabled in a future release. You do not need to configure `prompts.json` for immediate use.

## Running LabelBridge

Once your configuration files are in place, you can start the LabelBridge server. Start the Flask application by running:

```bash
python src/main.py
```

LabelBridge `host` and `port` can be configured via the `APP_URL` and `APP_PORT` environment variables. By default, LabelBridge will listen on `localhost:8001`.

## Connecting Label Studio

Now, configure your Label Studio project to use LabelBridge as its machine learning backend.

- Open your Label Studio project.
- Navigate to the Settings for your project.
- Go to the `Model` section. Here you can configure your existing ML model or create a new one. Upon clicking `Connect` you will see a form. Fill it up with the following information:
  - Put your model name in the `name` field.
  - Put the URL to your running LabelBridge instance in the `url` field.
  - In `Authentication` section, select `No Authentication`.
  - No extra parameters are required
  - Click validate and save.

{: .note-title }
> Tips
>
> You can check the `Interactive Preannotation` checkbox, which will enable real-time annotation in Label Studio.

After validating, you will be able to see the responses from LabelBridge in the `Response` section. You can then proceed to annotate your data.

{: .highlight}
Please note that your LabelBridge host must be set to `0.0.0.0`. Otherwise it will not regsister requests from Label Studio.

## Testing Your Setup

To verify LabelBridge is working correctly:

- Ensure LabelBridge is running.
- In your Label Studio project, import some unannotated data (e.g., raw text for NER).
- Go to the data annotation interface. As you load tasks, Label Studio should send requests to LabelBridge, and if a connected NLP model is active (after future configuration, beyond this quick start), you should start seeing automated pre-annotations appearing based on your model's predictions.

You are now ready to leverage LabelBridge for efficient, automated NER data annotation! The next sections will delve into specific data formats and advanced configurations.