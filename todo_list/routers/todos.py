from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo_list.database import get_session
from todo_list.models import ToDo, ToDoState, User
from todo_list.schemas import Message, ToDoList, ToDoPublic, ToDoSchema, ToDoUpdate
from todo_list.security import get_current_user

router = APIRouter(prefix='/todos', tags=['ToDos'])


T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=ToDoPublic)
def create_todo(todo: ToDoSchema, user: CurrentUser, session: T_Session):
    db_todo = ToDo(title=todo.title, description=todo.description, state=todo.state, user_id=user.id)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.get('/', response_model=ToDoList)
def list_todos(
    session: T_Session,
    user: CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: ToDoState | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    query = select(ToDo).where(ToDo.user_id == user.id)
    if title:
        query = query.filter(ToDo.title.contains(title))
    if description:
        query = query.filter(ToDo.description.contains(description))
    if state:
        query = query.filter(ToDo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()
    return {'todos': todos}


@router.patch('/{todo_id}', response_model=ToDoPublic)
def patch_todo(todo_id: int, session: T_Session, user: CurrentUser, todo: ToDoUpdate):
    db_todo = session.scalar(select(ToDo).where(ToDo.user_id == user.id, ToDo.id == todo_id))

    if not db_todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found.')

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: T_Session, user: CurrentUser):
    todo = session.scalar(select(ToDo).where(ToDo.user_id == user.id, ToDo.id == todo_id))

    if not todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found.')

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}
