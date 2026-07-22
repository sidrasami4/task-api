# Task API — W2 · A1 (Python / FastAPI)

A small CRUD API that manages a to-do list of tasks, built for the **FlyRank W2 A1 – "Build Your First CRUD API"** (Python/FastAPI lane).

This project stores data **in memory only**. Whenever the server restarts, the data resets to the three default seed tasks. This behavior is intentional and will be replaced with a database in the next assignment.

---

## Features

- CRUD operations for tasks
- In-memory data storage
- Automatic API documentation with Swagger UI
- Request validation
- JSON error responses
- Health check endpoint

---

## Requirements

- Python 3.10 or later

---

## Installation

### 1. Clone the repository

```bash
 git clone https://github.com/sidrasami4/task-api.git
cd task-api
```

### 2. Create a virtual environment (recommended)

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

---

## API URLs

After starting the server, open:

| URL | Description |
|------|-------------|
| http://localhost:8000/ | API description |
| http://localhost:8000/health | Health check |
| http://localhost:8000/tasks | List all tasks |
| http://localhost:8000/docs | Swagger UI |

---

# Swagger UI

See **`docs/swagger-ui.pdf`**

---

# Endpoints

| Method | Endpoint | Purpose | Success | Errors |
|---------|----------|---------|---------|--------|
| GET | `/` | API description | 200 | — |
| GET | `/health` | Health check | 200 | — |
| GET | `/tasks` | List all tasks | 200 | — |
| GET | `/tasks/{id}` | Get task by ID | 200 | 404 |
| POST | `/tasks` | Create a task | 201 | 400 |
| PUT | `/tasks/{id}` | Update a task | 200 | 400, 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204 | 404 |

---

## Status Codes

| Status Code | Meaning |
|-------------|---------|
| **200 OK** | Successful request |
| **201 Created** | Task created successfully |
| **204 No Content** | Task deleted successfully |
| **400 Bad Request** | Invalid or missing request data |
| **404 Not Found** | Requested task does not exist |

All error responses are returned in JSON format:

```json
{
  "error": "..."
}
```

---

## Example cURL

Create a task:

```bash
curl -i -X POST http://localhost:8000/tasks ^
-H "Content-Type: application/json" ^
-d "{\"title\":\"Complete FlyRank Assignment\"}"
```

Example response:

```http
HTTP/1.1 201 Created

{
  "id": 4,
  "title": "Complete FlyRank Assignment",
  "done": false
}
```

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn



**Sidra Sami Khanzada**

GitHub: git clone https://github.com/sidrasami4
