# imports
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import (
    MessageSchema,
    UserConstructorSchema,
    UserDBSchema,
    UserListSchema,
    UserPublicSchema,
    UserToUpdateSchema,
)

# initialize FastAPI app and define routes
app = FastAPI()
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def readingRoot():
    return {'message': 'Welcome to the FastAPI application!'}


@app.get('/status', response_class=HTMLResponse)
def status():
    return """
    <html>
      <head>
        <title>Python FastApi</title>
      </head>
      <body>
        <h1> API Working </h1>
      </body>
    </html>
    """


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserConstructorSchema):
    user_with_id = UserDBSchema(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserListSchema)
def list_users():
    return {'users': database}


@app.put('/user/{id}', status_code=HTTPStatus.OK)
def update_user(id: int, user: UserToUpdateSchema):
    for user_db in database:
        if user_db.id == id:
            if user.username is not None:
                user_db.username = user.username
            if user.email is not None:
                user_db.email = user.email
            if user.password is not None:
                user_db.password = user.password
            return UserPublicSchema(**user_db.dict())

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')


@app.delete('/users/{user_id}', response_model=MessageSchema)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    del database[user_id - 1]

    return {'message': 'User deleted'}


@app.get('/user/{id}', status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def show_user(id: int):
    for user_db in database:
        if user_db.id == id:
            return user_db
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
