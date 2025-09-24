# Backend - Issue Tracker (FastAPI + MongoDB)

## Prerequisites

-   Python 3.10+
-   MongoDB (local or hosted)

## Environment Variables

-   `MONGODB_URI` (e.g., mongodb://localhost:27017)
-   `MONGODB_DB` (default: issuetracker)
-   `CORS_ORIGIN` (e.g., http://localhost:5173)

## Setup & Run

``` bash
cd backend
python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

-   `GET /health`
-   `GET /issues` (query: search, status, priority, assignee, sortBy,
    sortOrder, page, pageSize)
-   `GET /issues/{id}`
-   `POST /issues`
-   `PUT /issues/{id}`

------------------------------------------------------------------------
