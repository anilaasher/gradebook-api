# Gradebook commands

Before any Python command, check `(myEnvironment)` shows at the start of the prompt. Run the API and React in separate terminals.

## Every day

| Task | Folder | Command |
|------|--------|---------|
| Start the API | folder with app.py | `python -m uvicorn app:app --reload` |
| Start React | frontend-react | `npm run dev` |
| Run the tests | folder with app.py | `python -m pytest -v` |
| Stop a running server | its own terminal | `Ctrl + C` |

## Now and then

| Task | Folder | Command |
|------|--------|---------|
| Tests with coverage | folder with app.py | `python -m pytest --cov=. --cov-report=term-missing` |
| Check React builds | frontend-react | `npm run build` |
| Add a shadcn component | frontend-react | `npx shadcn@latest add button` (change `button` to `input`, `card` and so on) |

## New computer

| Task | Folder | Command |
|------|--------|---------|
| Install Python packages | folder with app.py | `python -m pip install -r requirements-dev.txt` |
| Install React packages | frontend-react | `npm install` |

## Docker

| Task | Folder | Command |
|------|--------|---------|
| Build the API image | folder with app.py | `docker build -t gradebook-api .` |
| Run the API in a container | folder with app.py | `docker run -p 8000:8000 -v gradebook-data:/data -e DATABASE_URL=sqlite:////data/gradebook.db gradebook-api` |
| Stop the container | its own terminal | `Ctrl + C` |

Docs page when the container runs: http://localhost:8000/docs
Stop your normal API first, because both use port 8000.

## Saving work

Use the Source Control panel (`Ctrl + Shift + G`): stage the files, write a message, click Commit, then click Sync Changes.