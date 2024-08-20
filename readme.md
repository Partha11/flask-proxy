# Flask Proxy for Label Studio

[![Python Version][python-image]][python-url]
[![Python Version][flask-image]][flask-url]
[![Code Size][code-size]][code-size]

This repository contains a Flask-based proxy designed to facilitate integration between Label Studio and Hugging Face Spaces for NER tasks. The proxy acts as a middleware layer, receiving annotation requests from Label Studio, converting them into the format required by Hugging Face, and then forwarding the reformatted data to the designated Space for further processing.

## How It Works
This proxy server works automatically, acting as a bridge between your huggingface space and label studio
- Label Studio sends annotation data to the Flask proxy
- The proxy processes and reformats the data to match Hugging Face’s requirements
- Reformatted data is forwarded to the Hugging Face Space for further action

![](header.png)

## Installation

```sh
git clone https://github.com/Partha11/flask-proxy
cd path/to/flask-proxy
```
Create a virtual environment
```sh
python3 -m venv .venv
```
For Linux & OS X

```sh
source .venv/bin/activate
```
For Windows with CMD

```bash
.\.venv\Scripts\activate.bat
```
For Windows with Powershell

```bash
.\.venv\Scripts\activate.ps1
```

## Configuration

Copy the .env.example file and rename it to .env, I.E:

```sh
mv .env.example .env
```

Add your huggingface space url and huggingface token to the environment file, which will be used by the proxy server.

## Usage example

Start the server by using this command

```python
python -m src.main
```

After the server starts, it will accept request on the `/predict` endpoint

For connecting it with Label Studio, please check [Wiki][wiki].

## To Do
These are the list of tasks that will be done to this project

- [x] Add LLM for prediction
- [ ] Add data for healthcheck endpoint
- [ ] Migrate label studio configuration to a separate file

## Update History

* 0.2.0
    * ADD: Add `format_prediction()` method
* 0.1.1
    * FIX: Updated prediction field `task_id`
* 0.1.0
    * Connected model with prediction
    * CHANGE: Updated endpoint from `/proxy_predict` to `/predict`
* 0.0.1
    * Initialized project

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/badge/3.9-orange?style=flat-square&logo=python&logoColor=white&label=python&labelColor=gray&color=3776AB
[python-url]: https://www.python.org/downloads/release/python-390
[flask-image]: https://img.shields.io/badge/3.0.x-000000?style=flat-square&logo=flask&logoColor=white&label=flask&labelColor=gray&color=29B5E8
[flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[code-size]: https://img.shields.io/github/languages/code-size/Partha11/flask-proxy?style=flat-square&logo=github
[wiki]: https://github.com/Partha11/flask-proxy/wiki
