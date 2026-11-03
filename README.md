# Gradebook API

[![Tests](https://github.com/anilaasher/gradebook-api/actions/workflows/tests.yml/badge.svg)](https://github.com/anilaasher/gradebook-api/actions/workflows/tests.yml)

A web API for managing students and their grades, built with Python, FastAPI and SQLite, with a React front end.


## Run the API

```
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

## Run the tests

```
python -m pip install -r requirements-dev.txt
python -m pytest -v
```