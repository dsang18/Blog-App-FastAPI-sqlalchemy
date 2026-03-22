from fastapi import Depends, HTTPException, APIRouter
import models
import traceback
from database_models import Vote, Post
from typing import List, Optional
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import get_current_user

router = APIRouter(prefix="/vote",tags=['Vote'])

@router.post("/", status_code=201)
async def vote(vote:models.Vote, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    print("Inside Vote Update")
    try:
        post = db.query(Post).filter(Post.id == vote.post_id).first()
        if post is None:
            raise HTTPException(404, "Post not found")

        if vote.dir==1:
            found_vote = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
            if found_vote.first() is not None:
                raise HTTPException(409, "Vote already exists")
            new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
        else:
            vote_to_delete = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
            if vote_to_delete.first() is None:
                raise HTTPException(404, "Vote does not exist")
            vote_to_delete.delete(synchronize_session=False)
            db.commit()
        return {"status":"Vote Updated"}
    except Exception as e:
        return HTTPException(404, str(e))


