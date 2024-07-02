from fastapi import FastAPI
from routers import film, auth, user
import models
from database import engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get('/Homepage')
def Home_page():
    return {"status" : "work successfully !"}

app.include_router(film.router)
app.include_router(auth.router)
app.include_router(user.router)


