from models import User, UserResponse
from fastapi import Depends, HTTPException, APIRouter
import database_models
from sqlalchemy.orm import Session
from database import get_db
import utils

router = APIRouter(prefix="/users",tags=['Users'])

@router.post("", status_code=201)
async def create_user(user: User, db:Session = Depends(get_db)):
    try:
        # Hash the password
        hashed_password = utils.has_password(user.password)
        user.password = hashed_password
        db.add(database_models.User(**user.model_dump()))
        db.commit()
        return f"New User Created!"
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id}", status_code=201, response_model=UserResponse)
async def get_user(id:int, db:Session = Depends(get_db)):
    try:
        user = db.query(database_models.User).filter(database_models.User.id == id).first()
        if user is not None:
            return user
        return HTTPException(400, detail=f"No User Found with id {id}")
    except Exception as e:
        return HTTPException(400, detail=str(e))
