---
title: Introduction
layout: home
nav_order: 1
description: LabelBridge is a Flask middleware that seamlessly connects Label Studio with NLP models and LLMs, handling data transformations to enable smooth automated annotations.
permalink: /
---

# Introduction

Welcome to **LabelBridge**, an open-source Flask middleware that bridges the gap between [**Label Studio**][label-studio] and your **Natural Language Processing (NLP)** models or **Large Language Models (LLMs)**.

{: .highlight }
Currently, LabelBridge supports text-based tasks only.

## Why LabelBridge?

While Label Studio is a versatile and feature-rich data labeling platform, integrating it with custom NLP or LLM-based annotation pipelines can be challenging. One of the key obstacles is the lack of clear documentation regarding the expected request and response formats for automated model-based annotations.

**LabelBridge** addresses this issue by acting as a smart intermediary. It intercepts and translates requests between Label Studio and your models, automatically reformatting the data so that both systems can communicate without error or manual intervention:

- Incoming requests from Label Studio are transformed into a format your NLP models or LLMs can process.
- Model predictions are then adapted into the specific structure that Label Studio requires for annotations.

This middleware was created after extensive reverse-engineering and debugging of Label Studio’s undocumented API interactions. The goal is to eliminate guesswork, reduce setup time, and enable fast, reliable integration of custom models into your labeling workflow.

LabelBridge empowers data scientists, ML engineers, and annotation teams to automate their labeling processes efficiently. The integration of NLP models works with both local runtime and Hugging Face Spaces, making it a versatile solution for a wide range of annotation scenarios.

Start building intelligent, model-assisted annotation pipelines with confidence and ease.

<!-- links -->
[label-studio]: https://labelstud.io/
