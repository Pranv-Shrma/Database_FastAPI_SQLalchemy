from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException
from typing import Optional, List

import sqlite3

app = FastAPI()

# create a connection to the database
connection = sqlite3.connect("database.db")
cursor = connection.cursor()



DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# foundation of all database models
# maps to all tables in the database

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    

Base.metadata.create_all(bind=engine)


    
def get_db():
    db = SessionLocal() # create a new session to interact with the database
    try:
        yield db # to yield the session to the caller
    finally:
        db.close() # to close the session after the request is done


from pydantic import BaseModel

        
# create a new user

class UserCreate(BaseModel):
    name: str
    email: str


@app.post("/users/create_user", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# read data from the database

class UserResponse(BaseModel):
    id : int
    name: str
    email: str

class Config:
    orm_mode = True




@app.get("/users/read_users", response_model=List[UserResponse])
def read_users(skip : int, limit : int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/read_user/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user



# update data in the database

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

@app.put("/users/update_user/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


# delete data from the database

@app.delete("/users/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User with id {user_id} has been deleted successfully"}





