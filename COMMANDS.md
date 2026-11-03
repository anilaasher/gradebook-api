# Gradebook commands

Run each in its own terminal. Check `(myEnvironment)` shows at the start of the prompt.

## Start the API (folder with app.py)
```
python -m uvicorn app:app --reload
```

## Start React (folder frontend-react)
```
npm run dev
```

## Run the tests (folder with app.py)
```
python -m pytest -v
```

## Run the tests with coverage (folder with app.py)
```
python -m pytest --cov=. --cov-report=term-missing
```