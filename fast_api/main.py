from fastapi import FastAPI
from .routers import film, auth, user
from . import models
from . import database


# models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()


@app.get('/Homepage')
def Home_page():
    return {"status" : "work successfully !"}

app.include_router(film.router)
app.include_router(auth.router)
app.include_router(user.router)


