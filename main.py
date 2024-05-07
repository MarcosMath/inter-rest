from typing import Annotated, Union

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db ={
    "johndoe" :{
        "username" : "johndoe",
        "fullname" : "John Doe",
        "email" : "johndoe@example.com",
        "hashed_password" : "fakehashedsecret",
        "disable" : True,
    },
    "mrosas" :{
        "username" : "mrosas",
        "fullname" : "Marcos Rosas",
        "email" : "mrosas74@gmail.com",
        "hashed_password" : "fakehashedsecret2",
        "disable" : False,
    },
    "mariajose" :{
        "username" : "mariajose",
        "fullname" : "Maria Jose",
        "email" : "majo@example.com",
        "hashed_password" : "fakehashedsecret3",
        "disable" : False,
    }
}



app = FastAPI()

def fake_hash_password(passsword : str):
    return "fakehashed"+passsword

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Usuario(BaseModel):
    username : str
    email : Union[str, None] = None
    full_name : Union[str, None] = None
    disabledd : Union[bool, None] = None

class UsuarioEnDB(Usuario):
    hashed_passowrd: str

def get_user(db, username : str):
    if username in db:
        user_dict = db[username]
        return UsuarioEnDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token : Annotated[str, Depends(oauth2_scheme)]):
    usuario = fake_decode_token(token)
    if not usuario:
        raise HTTPException(
            
        )

@app.get("/users/me")
async def read_users_me(current_user : Annotated[Usuario, Depends(get_current_user)]):
    return current_user
                        

@app.get("/items/")
def read_items(token : Annotated[str, Depends(oauth2_scheme)]):
    return token