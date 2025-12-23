
from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

api = FastAPI()

class Priority(IntEnum):
    low = 3
    medium = 2
    high = 1

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=502, description="Name of the todo")
    todo_descripstion: str = Field(..., description="Description of the todo")
    priority: Priority = Field(default=Priority.low, description="Priority of the todo")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description="ID of the todo")

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=502, description="Name of the todo")
    todo_descripstion: Optional[str] = Field(None, description="Description of the todo")
    priority: Optional[Priority] = Field(None, description="Priority of the todo")

# all_todos = [
#     {'todo_id':1, 'todo_name': 'Sports', 'todo_descripstion': "go to the gym"},
#     {'todo_id':2, 'todo_name': 'Study', 'todo_descripstion': "read a book"},
#     {'todo_id':3, 'todo_name': 'Shopping', 'todo_descripstion': "buy groceries"},
# ]

all_todos = [
    Todo(todo_id=1, todo_name='Sports', todo_descripstion="go to the gym", priority=Priority.medium),
    Todo(todo_id=2, todo_name='Study', todo_descripstion="read a book", priority=Priority.high),
    Todo(todo_id=3, todo_name='Shopping', todo_descripstion="buy groceries", priority=Priority.low),
]

@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id : int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
        
@api.get('/todos/', response_model=List[Todo])
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
    
@api.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    
    new_todo = Todo(todo_id=new_todo_id, 
                    todo_name=todo.todo_name, 
                    todo_descripstion=todo.todo_descripstion, 
                    priority=todo.priority)

    all_todos.append(new_todo)
    return new_todo

@api.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_descripstion is not None:
                todo.todo_descripstion = updated_todo.todo_descripstion
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
        
    raise HTTPException(status_code=404, detail="Todo not found")

    

@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Todo not found")

## GET, POST, PUT, DELETE
# @api.get('/')
# def index():
#     return {"message": "Hello World!"}

# localhost:9999/todos?first_n=3

# @api.get('/todos/{todo_id}')
# def get_todo(todo_id : int):
#     for todo in all_todos:
#         if todo['todo_id'] == todo_id:
#             return {'result': todo}


# @api.get('/todos/')
# def get_todos(first_n: int = None):
#     if first_n is not None:
#         return all_todos[:first_n]
#     else:
#         return all_todos

# @api.post('/todos')
# def create_todo(todo: dict):
#     new_todo_id = max(todo['todo_id'] for todo in all_todos) + 1
    
#     new_todo = {
#         'todo_id': new_todo_id,
#         'todo_name': todo['todo_name'],
#         'todo_descripstion': todo['todo_descripstion']
#     }
#     all_todos.append(new_todo)
#     return {'result': new_todo}


# @api.put('/todos/{todo_id}')
# def update_todo(todo_id: int, updated_todo: dict):
#     for todo in all_todos:
#         if todo['todo_id'] == todo_id:
#             todo['todo_name'] = updated_todo['todo_name']
#             todo['todo_descripstion'] = updated_todo['todo_descripstion']
#             return todo
#     return "error, not found"


# @api.delete('/todos/{todo_id}')
# def delete_todo(todo_id: int):
#     for index, todo in enumerate(all_todos):
#         if todo['todo_id'] == todo_id:
#             deleted_todo = all_todos.pop(index)
#             return {'result': deleted_todo}
#     return "error, not found"

