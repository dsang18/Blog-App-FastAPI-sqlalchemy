from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from datetime import datetime

class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Post(BaseModel):
    user_id: Optional[int]=None
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    published: bool
    owner: UserResponse

class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]