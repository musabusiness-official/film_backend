from fastapi import FastAPI, HTTPException, APIRouter, Depends, status
from schemas import FilmModel, FilmResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import get_db
import models
from random import choice
from oauth2 import get_current_user
from config import settings


router = APIRouter(
    prefix= '/Homepage/film',
    tags= ['film router']
)

@router.post('/create_film',
            # response_model= FilmResponse
            )
def create_film(film : FilmModel, owner_pass : str = None , db : Session = Depends(get_db)):
    
    # if film.secret_key is not SECRET_KEY_FOR_ADD_AND_MODIFY:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail= "you do not have the authority"
    #     )

    if owner_pass == None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'you have to provide the owner password'
        )

    if owner_pass != settings.owner_password :
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'the owner password is not correct'
        )
    
    new_film = models.BloodyFilm(**film.dict())
    # new_film = models.BloodyFilm(
    #     title = film.title,
    #     type = film.type,
    #     description = film.description,
    #     video_url = film.video_url
    # )
    db.add(new_film)
    db.commit()
    db.refresh(new_film)

    return new_film


@router.delete('/delete_film/{id}')
def delete_film(id : int, owner_pass : str = None ,db: Session = Depends(get_db)):

    if owner_pass == None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'you have to provide the owner password'
        )

    if owner_pass != settings.owner_password :
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'the owner password is not correct'
        )


    query = db.query(models.BloodyFilm).filter(models.BloodyFilm.id == id)
    the_film = query.first()


    if the_film == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f'the film with an id of {id} does not exsist.'
        )

    query.delete(synchronize_session=False)
    db.commit()

    return {"message" : f"the film with an id of {id} have deleted."}



@router.put("/update_film/{id}")
def update_film(id : int,  updated_film : dict, owner_pass : str = None,db: Session = Depends(get_db)):

    if owner_pass == None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'you have to provide the owner password'
        )

    if owner_pass != settings.owner_password :
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'the owner password is not correct'
        )


    # querytry = db.query(models.BloodyFilm).filter(models.BloodyFilm.id == id)
    query = db.query(models.BloodyFilm).filter(models.BloodyFilm.id == id)

    film = query.first()

    if film == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f'the film with an id {id} does not exsist'
        )
    
    # if updated_film.secret_key != SECRET_KEY_FOR_ADD_AND_MODIFY:
    #     raise HTTPException(
    #         status_code= status.HTTP_401_UNAUTHORIZED,
    #         detail= 'you do not have the authority to modify on films'
    #     )
    
    query.update(updated_film, synchronize_session=False)

    db.commit()

    return {"message" : "successfully done.", "updated_film" : query.first()}


@router.get('/get_film_by_id/{id}')
def get_film_by_id(id : int , owner_pass : str = None, db: Session = Depends(get_db)):

    if owner_pass == None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'you have to provide the owner password'
        )

    if owner_pass != settings.owner_password :
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'the owner password is not correct'
        )

    film = db.query(models.BloodyFilm).filter(models.BloodyFilm.id == id).first()

    if film == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f'the film with an id of {id} does not exsist'
        )

    return film


@router.get('/get_all_films/')
def get_all_film(owner_pass : str = None,db: Session = Depends(get_db)):

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

    films = db.query(models.BloodyFilm).all()

    if films == None:
        return 'there is no film here yet.'

    return films

@router.get('/get_limited_films/{limits}')
def get_limited_films(owner_pass : str = None ,limits : int = 3, db:Session = Depends(get_db)):
    
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

    films = db.query(models.BloodyFilm).filter(models.BloodyFilm).limit(limits).all()

    return films


@router.get('/get_film_by_search/{search}')
def get_film_by_search(search : str , owner_pass : str = None, db : Session = Depends(get_db)):

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

    films = db.query(models.BloodyFilm).filter(models.BloodyFilm.type.contains(search)).all()

    return films


@router.get('/get_random_film')
def get_random_film(db: Session = Depends(get_db), current_user : int = Depends(get_current_user)):
    
    # print(current_user.id)
    print(current_user.shown_films)
    # print(current_user.user_character)
    # print(current_user.coins)
    # print(current_user.created_at)
    print(current_user.name)
    # print(current_user.password)
    

    films = db.query(models.BloodyFilm).all()

    film_ids = []
    for film in films:
        film_ids.append(film.id)


    shown_films = current_user.shown_films
    available_film_ids = [item for item in film_ids if item not in shown_films]

    if len(available_film_ids) < 1 :
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= 'sorry , you have seen all films we have '
        )


    print(available_film_ids)
    

    film_id = choice(available_film_ids)
    
    user = db.query(models.User).filter(models.User.id == current_user.id)
    user.update(
        {models.User.shown_films : func.array_append(models.User.shown_films, film_id)}
    )

    db.commit()


    film = db.query(models.BloodyFilm).filter(models.BloodyFilm.id == film_id).first()

    return film
    
    # films = db.query(models.BloodyFilm).filter(models.BloodyFilm.is_seen == False).all()
    # films_ids : list = []

    # length =  len(films)

    # if len(films) < 1:
    #     random_index = randint(0, length-1)
    #     print(length)
    #     print(random_index)

    #     selected = films[random_index]

    #     query = db.query(models.BloodyFilm).filter(models.BloodyFilm.id == selected.id)

    #     query.update({"is_seen" : True}, synchronize_session=False)

    #     db.commit()

    #     film = query.first()

    #     if film == None:
    #         raise HTTPException(
    #             status_code=  status.HTTP_404_NOT_FOUND,
    #             detail= 'all films is already seen.'
    #         )

    #     return film
    
    # raise HTTPException(
    #     detail= 'all films is already shown. '
    # )
     