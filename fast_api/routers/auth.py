from fastapi import HTTPException, status, Depends, APIRouter
from .. import models
from sqlalchemy.orm import Session
from .. import database 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import utils
from .. import oauth2


router = APIRouter(
    tags= ['Authentication']
)



@router.post("/login")
def login(user_credential : OAuth2PasswordRequestForm = Depends() ,db : Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.name == user_credential.username).first()

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'there is no name like {user_credential.username}'
        )
    
    # hashed_pass = hash(user_credential.password)

    # if not verify_password(
    #     plain_password= hashed_pass,
    #     password= user.password
    # ) : 
    #     raise HTTPException(
    #         status_code= status.HTTP_406_NOT_ACCEPTABLE, 
    #         detail= 'your password is false'
    #     )

    if user_credential.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail= 'your password is false'
        )
    
    access_token = oauth2.create_access_token(data= {"user_id" : user.id})

    return access_token