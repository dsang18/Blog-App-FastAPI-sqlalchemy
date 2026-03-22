from fastapi import Depends, HTTPException, APIRouter
import models
import traceback
from database_models import Post, Vote
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from database import get_db
from oauth2 import get_current_user

router = APIRouter(prefix="/posts",tags=['Posts'])

# http://127.0.0.1:8000/posts?limit=3&skip=2
# http://127.0.0.1:8000/posts?search=2
# http://127.0.0.1:8000/posts?search=Post%202
# @router.get("/", status_code=200, response_model=List[models.PostResponse])
@router.get("/", status_code=200, response_model=List[models.PostVoteResponse])
async def get_posts(db:Session = Depends(get_db), limit:int=10, skip:int=0, search:Optional[str]=""):
    try:
        # posts =  db.query(Post).filter(Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
        results = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id==Post.id, isouter=True).group_by(Post.id).filter(or_(Post.title.contains(search), Post.content.contains(search))).limit(limit=limit).offset(offset=skip).all()
        return results
    except Exception as e:
        return HTTPException(404, str(e))


# Create New Post
@router.post("/", status_code=201)
async def create_posts(post: models.Post, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        print("Inside Create Post")
        post.user_id = current_user.id
        db.add(Post(**post.model_dump()))
        db.commit()
        return f"New Post Created!"
    except Exception as e:
        print(f"Exception in creating post {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))


# Get a single Post by ID
@router.get("/{id}", status_code=200, response_model=models.PostVoteResponse)
async def get_post(id:int, db:Session = Depends(get_db), _:int = Depends(get_current_user)):
    try:
        post = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id==Post.id, isouter=True).group_by(Post.id).filter(Post.id == id).first()
        if post is not None:
            return post
        return HTTPException(400, detail=f"No Post Found with id {id}")
    except Exception as e:
        return HTTPException(400, detail=str(e))
    

# Delete a Post by ID
@router.delete("/{id}", status_code=201)
async def delete_post(id:str, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        post_to_delete = db.query(Post).filter(Post.id == id)
        if post_to_delete.first() is None:
            return HTTPException(400, detail=f"No Post Found with id {id}")
        
        if post_to_delete.first().user_id != current_user.id:
            return HTTPException(403, detail=f"You are not allowed to delete someone else's post")
        else:
            post_to_delete.delete(synchronize_session=False)
        db.commit()
        return f"Post with id {id} deleted"
    except Exception as e:
        return HTTPException(400, detail=str(e))
    

# Updated a Post by ID
@router.put("/{id}")
async def update_post(id:str, updated_post:models.Post, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    print("Inside Update Post")
    try:
        # print(**updated_post.model_dump())
        post_to_update = db.query(Post).filter(Post.id == id)
        if post_to_update.first() is None:
            return HTTPException(400, detail=f"No Post Found with id {id}")
        
        if post_to_update.first().user_id != current_user.id:
            return HTTPException(403, detail=f"You are not allowed to update someone else's post")
        else:
            post_to_update.update(**updated_post.model_dump(), synchronize_session=False)

        db.commit()
        return f"Post with id {id} updated"
    except Exception as e:
        print(str(e))
        return HTTPException(400, detail=f"No Post Found with id {id} - {traceback.format_exc()}")
    
   