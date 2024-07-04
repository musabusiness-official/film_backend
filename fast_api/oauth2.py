from sqlalchemy.orm import Session
from . import database
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from . import schemas
from . import models
from . import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp' : expire})

    encodeed_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encodeed_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : int = payload.get('user_id')
        
        if id is None:
            raise credential_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credential_exception
    
    return token_data



def get_current_user(token:str= Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail='invalid credentials', headers={"WWW-Authenticate" : "Bearer"}
    )

    token_data = verify_access_token(token=token, credential_exception=credential_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user