from pydantic import BaseModel
from datetime import datetime 
from typing import Optional

class UserModel (BaseModel):
    name : str
    password : str


class UserResponse(BaseModel):
    id : int
    name : str
    created_at : datetime


class FilmModel(BaseModel):
    type: str
    title : str
    description : str
    video_url : str



class FilmResponse(FilmModel):
    id : int
    created_at : datetime



class TokenData(BaseModel):
    id : Optional[str] = None 


class TokenResponse(BaseModel):
    token : str
    token_type : str