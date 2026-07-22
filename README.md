Task API — W2 · A1 (Python / FastAPI lane)
A small CRUD API that manages a to-do list of tasks. Built for the FlyRank W2 A1assignment ("Build your first CRUD API"), Python lane.

Data lives in memory only — restart the server and it resets to the 3 seedtasks. That's deliberate: Week 3 swaps this for a real database, and losingyour data on restart is the lesson that motivates it.

How to install & run
You need Python 3.10+.

# 1. (optional but recommended) create a virtual environmentpython -m venv .venvsource .venv/bin/activate          # Windows: .venv\Scripts\activate# 2. install the two dependenciespip install -r requirements.txt# 3. run the server  — one documented commanduvicorn main:app --reload
Then open:

http://localhost:8000/ — API description (JSON)
http://localhost:8000/health — {"status":"ok"}
http://localhost:8000/tasks — the task list
http://localhost:8000/docs — Swagger UI (interactive)
Endpoints
Method
Path
Purpose
Success
Errors
GET	/	Describe the API	200	—
GET	/health	Liveness probe	200	—
GET	/tasks	List all tasks	200	—
GET	/tasks/{id}	Get one task by id	200	404
POST	/tasks	Create a new task (body: title)	201	400
PUT	/tasks/{id}	Update title and/or done	200	400, 404
DELETE	/tasks/{id}	Delete a task	204	404

Status codes used
200 OK — successful read or update
201 Created — POST /tasks succeeded
204 No Content — DELETE /tasks/{id} succeeded
400 Bad Request — missing/empty title on POST or PUT
404 Not Found — no task with that id
All errors return JSON: {"error": "..."}