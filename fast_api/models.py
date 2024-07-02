from database import Base
from sqlalchemy import Column, String , Integer,ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_character = Column(String, nullable = False)
    coins = Column(Integer, nullable = False, server_default = "0")
    shown_films = Column(ARRAY(Integer),nullable = False, server_default = '[]')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    


class BloodyFilm(Base):
    __tablename__ = 'bloodyfilms'
    id = Column(Integer, primary_key=True)
    type = Column(String, server_default = 'blood video')
    title = Column(String, server_default=f'film number {id}')
    description = Column(String, nullable=False)
    video_url = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))

