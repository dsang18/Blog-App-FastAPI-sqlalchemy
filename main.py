import sys
sys.dont_write_bytecode = True

from fastapi import FastAPI
from models import Post
from database import SessionLocale,engine
import database_models
from routers import post, user, auth, vote

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

database_models.BaseModel.metadata.create_all(bind=engine)

all_posts = [
    Post(user_id=1,title="Post 1", content="Dummy Content for Post 1"),
    Post(user_id=1,title="Post 2", content="Dummy Content for Post 2"),
    Post(user_id=1,title="Post 3", content="Dummy Content for Post 3")
    ]



def init_db():
    db = SessionLocale()
    count = db.query(database_models.Post).count()
    if count==0:
        for post in all_posts:
            db.add(database_models.Post(**post.model_dump()))
    db.commit()
    db.close()

init_db()