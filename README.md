# Gradebook API

[![Tests](https://github.com/anilaasher/gradebook-api/actions/workflows/tests.yml/badge.svg)](https://github.com/anilaasher/gradebook-api/actions/workflows/tests.yml)

A web API for managing students and their grades, built with Python, FastAPI and SQLite, with a React front end.


![Gradebook screenshot](docs/screenshot.png)


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

## Endpoints

| Method | Path | What it does |
|--------|------|--------------|
| POST | /students | Add a student (JSON body with `name`) |
| GET | /students | List all student names |
| GET | /students/{name} | Get one student's grades and average |
| POST | /students/{name}/grades | Add a grade (JSON body with `score`) |
| DELETE | /students/{name} | Delete a student and their grades |

With the API running, interactive documentation is at http://127.0.0.1:8000/docs