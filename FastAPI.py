from sqlalchemy import create_engine, Column, Integer, String, false
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session  #this will help us interact with the datebase
from pydantic import BaseModel  #This validte the data coming comparing to the entry data, as both should match
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from typing import Optional



app = FastAPI()
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()  # The base class act as the manager of the dataset that act as a parent for all tables aka model and calass attribute AKA column


#Define a table inharated from the base (this communiucate on program level that
# it is a table belong to base) better for communication on case we bring more tables
class User(base):
    #Now we created a new table named users
    __tablename__ = "users"
    #Now we define the columns in this table
    #Start with id that is an integer and act as a primary key
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    #now declare creating new table using the metadata engine , as SQLaalchemy is waiting for this command
    #to create the table without needing SQL
    base.metadata.create_all(bind=engine)


#This allow the session to be used in the API end poing once the API is uesed we close it regardless if there was an
#action or not the DB session is closed to ensure no leak
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=(UserResponse))
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


class UserUpdate(BaseModel):
   name: Optional[str] = None
   email: Optional[str] = None

@app.put("/users/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name if user.name is not None else db_user.name
    db_user.email = user.email if user.email is not None else db_user.email
    db.commit()
    db.refresh(db_user)
    return db_user
@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

