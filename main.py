"""Task API — a small CRUD API for a to-do list.

Full CRUD: Create, Read, Update, Delete — on an in-memory list of tasks.
Extras: ?done=, ?search= filters, GET /stats, POST /reset.
Run with:  uvicorn main:app --reload
Then open: http://localhost:8000/docs
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    version="1.0",
    description=(
        "A small CRUD API that manages a to-do list of tasks.\n\n"
        "Data lives in memory only — restart the server and it resets to the "
        "3 seed tasks. (Week 3 replaces this with a real database.)\n\n"
        "Try every endpoint live at [/docs](/docs)."
    ),
)


# ---------- Models ----------
class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    """Body for POST /tasks — only the title is needed; id and done are set by the server."""
    title: str | None = None


class TaskUpdate(BaseModel):
    """Body for PUT /tasks/{id} — both fields optional; only sent fields are changed."""
    title: str | None = None
    done: bool | None = None


# ---------- In-memory "database" ----------
# This list lives in the program's memory. Restart the server and it's gone.
# That's deliberate — Week 3 introduces a real database to fix exactly this.
SEED_TASKS: list[Task] = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Build a CRUD API", done=False),
    Task(id=3, title="Publish to GitHub", done=False),
]
tasks: list[Task] = list(SEED_TASKS)


def reset_tasks() -> None:
    """Restore the in-memory list to the original 3 seed tasks."""
    global tasks
    tasks = list(SEED_TASKS)


def find_task(task_id: int) -> Task | None:
    """Return the task with the given id, or None if it doesn't exist."""
    return next((t for t in tasks if t.id == task_id), None)


def next_id() -> int:
    """Next free id — one bigger than the current max."""
    return max((t.id for t in tasks), default=0) + 1


# ---------- Error format ----------
# FastAPI's default error shape is {"detail": "..."}. The assignment wants
# {"error": "..."}, so we rewrite every HTTPException response here.
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


# ---------- Stage 1: meta endpoints ----------
@app.get("/", tags=["meta"], summary="API description")
def root():
    """Describes the API in a small JSON object so clients know what they've found."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health", tags=["meta"], summary="Health check")
def health():
    """Liveness probe — real companies hit this to check a server is alive."""
    return {"status": "ok"}


# ---------- Stage 2: Read ----------
@app.get("/tasks", tags=["tasks"], summary="List all tasks (with optional filters)")
def list_tasks(
    done: bool | None = None,
    search: str | None = None,
):
    """Returns every task currently in memory.

    Optional query parameters (extras):
    - `?done=true`  — only finished tasks
    - `?done=false` — only open tasks
    - `search=mil`  — only tasks whose title contains "mil" (case-insensitive)
    """
    result = list(tasks)
    if done is not None:
        result = [t for t in result if t.done == done]
    if search:
        needle = search.lower()
        result = [t for t in result if needle in t.title.lower()]
    return result


@app.get("/tasks/{task_id}", tags=["tasks"], summary="Get one task by id")
def get_task(task_id: int):
    """Returns the task with the given id, or 404 if it doesn't exist."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


# ---------- Stage 3: Create ----------
@app.post("/tasks", status_code=201, tags=["tasks"], summary="Create a new task")
def create_task(payload: TaskCreate):
    """Creates a new task. Title is required and must not be empty.

    Returns 201 Created with the new task (including its server-assigned id).
    Returns 400 Bad Request if the title is missing or blank.
    """
    title = (payload.title or "").strip()
    if not title:
        raise HTTPException(
            status_code=400,
            detail="title is required and must not be empty",
        )
    task = Task(id=next_id(), title=title, done=False)
    tasks.append(task)
    return task


# ---------- Stage 4: Update + Delete ----------
@app.put("/tasks/{task_id}", tags=["tasks"], summary="Update an existing task")
def update_task(task_id: int, payload: TaskUpdate):
    """Replaces title and/or done on an existing task.

    Returns 200 with the updated task, 404 if the id doesn't exist,
    or 400 if a title is supplied but blank.
    """
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    # Validate first, mutate second — so a bad request leaves the task untouched.
    if payload.title is not None:
        title = payload.title.strip()
        if not title:
            raise HTTPException(
                status_code=400,
                detail="title must not be empty",
            )
        task.title = title
    if payload.done is not None:
        task.done = payload.done
    return task


@app.delete("/tasks/{task_id}", status_code=204, tags=["tasks"], summary="Delete a task")
def delete_task(task_id: int):
    """Removes the task with the given id. Returns 204 No Content on success, 404 if missing."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    tasks.remove(task)
    # 204 = success with no body. Returning None keeps the response empty.
    return None


# ---------- Extras: stats + reset ----------
@app.get("/stats", tags=["meta"], summary="Task statistics")
def stats():
    """Computes counts from the current task list — the server doing more than just storing."""
    total = len(tasks)
    done_count = sum(1 for t in tasks if t.done)
    return {
        "total": total,
        "done": done_count,
        "open": total - done_count,
    }


@app.post("/reset", status_code=200, tags=["meta"], summary="Reset tasks to seed data")
def reset():
    """Restores the in-memory list to the original 3 seed tasks. Handy for demos."""
    reset_tasks()
    return {"reset": True, "count": len(tasks)}