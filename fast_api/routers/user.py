from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserModel, UserResponse
import models
from utils import hash
from oauth2 import create_access_token, get_current_user
from config import settings


router = APIRouter(
    prefix= '/Homepage/user',
    tags= ['user']
)

@router.post('/create_user',) # response_model= UserResponse
def create_user(user : UserModel ,db: Session = Depends(get_db)):
    
    disagree_name = db.query(models.User).filter(models.User.name == user.name).first()

    if disagree_name != None:
        raise HTTPException(
            status_code= status.HTTP_226_IM_USED,
            detail= 'this name already token'
        ) 

    # user.password = hash(user.password)

    new_user = models.User(**user.dict())
    new_user.name = new_user.name  # split()
    new_user.user_character = new_user.name[0]

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    token = create_access_token(data= {"user_id" : new_user.id})

    return {
        "token" : token,
        "user_data" : new_user
    }



# @router.delete('/delete_user/{id}')
# def delete_user(
#         db : Session = Depends(get_db),
#         # current_user : 
# )
    

@router.get('/all_users')
def all_users(owner_pass : str = None, db: Session = Depends(get_db)):

    if owner_pass == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= 'you have to provide the owner password'
        )
    
    if owner_pass != settings.owner_password :
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'the owner password is not correct'
        )
    
    users = db.query(models.User).all()

    return users


@router.delete('/delete_user_by_id/{id}')
def delete_user( id : int, owner_pass : str = None , db : Session = Depends(get_db)):

    if owner_pass == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= 'you have to provide the owner password'
        )
    
    if owner_pass != settings.owner_password :
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'the owner password is not correct'
        )

    query = db.query(models.User).filter(models.User.id == id)
    user = query.first()

    if user == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f'this user with id of {id} does not exsist'
        )

    query.delete(synchronize_session=False)
    db.commit()

    return {"status" : "done successfully."}



@router.delete('/delete_current_user')
def delete_current_user(db : Session = Depends(get_db), current_user : int = Depends(get_current_user)):
    query = db.query(models.User).filter(models.User.id == current_user.id)

    query.delete(synchronize_session=False)
    db.commit()

    return {"status" : "done successfully."}