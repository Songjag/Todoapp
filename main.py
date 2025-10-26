from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Todo List WebApp")

# Gắn thư mục template
templates = Jinja2Templates(directory="templates")

# Bộ nhớ tạm cho Todo
todos = []

# Model Todo
class Todo(BaseModel):
    id: int
    title: str
    description: str = ""
    completed: bool = False


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/api/todos")
def get_todos():
    return todos


@app.post("/api/todos")
def add_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo added", "todo": todo}


@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: int, updated: Todo):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[i] = updated
            return {"message": "Todo updated", "todo": updated}
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
