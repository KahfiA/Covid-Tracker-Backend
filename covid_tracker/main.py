from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


###############


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # db_user = crud.get_user_by_email(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = crud.get_users(db, skip=skip, limit=limit)
    return user


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def edit_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.edit_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


#################


@app.post("/persons/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    # db_person = crud.get_person_by_email(db, email=person.email)
    # if db_person:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_person(db=db, person=person)

@app.get("/persons/", response_model=List[schemas.Person])
def read_person(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    person = crud.get_persons(db, skip=skip, limit=limit)
    return person


@app.get("/persons/{person_id}", response_model=schemas.Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@app.put("/persons/{person_id}", response_model=schemas.Person)
def edit_person(person_id: int, person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.edit_person(db, person_id=person_id, person=person)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@app.delete("/persons/{person_id}", response_model=schemas.Person)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.delete_person(db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


#################

@app.post("/persons/{person_id}/positions", response_model=schemas.Position)
def create_position(person_id: int, position: schemas.PositionCreate, db: Session = Depends(get_db)):
    return crud.create_position(db=db, person_id=person_id, position=position)

@app.get("/persons/{person_id}/positions", response_model=List[schemas.Position])
def read_positions(person_id: int, db: Session = Depends(get_db)):
    return crud.get_positions(db=db, person_id=person_id)

@app.get("/persons/{person_id}/positions/{position_id}", response_model=schemas.Position)
def read_positions(person_id: int, position_id: int, db: Session = Depends(get_db)):
    db_position = crud.get_position(db=db, person_id=person_id, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position

@app.delete("/persons/{person_id}/positions/{position_id}", response_model=schemas.Position)
def read_positions(person_id: int, position_id: int, db: Session = Depends(get_db)):
    return crud.delete_position(db=db, person_id=person_id, position_id=position_id)

#################

@app.get("/traces/{person_id}", response_model=List[schemas.PositionTraced])
def read_traces(person_id: int, db: Session = Depends(get_db)):
    return crud.get_traces(db=db, person_id=person_id)