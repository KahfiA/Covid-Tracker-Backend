from datetime import date, datetime
from sqlalchemy import sql
from sqlalchemy.orm import Session
import math
from geopy import distance

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username = user.username, password = user.password, level = user.level)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def edit_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db_user.username = user.username
    db_user.password = user.password
    db_user.level = user.level
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

####################

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.person_id == person_id).first()

def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(name = person.name, age = person.age, gender = person.gender, condition = person.condition)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def edit_person(db: Session, person_id: int, person: schemas.PersonCreate):
    db_person = db.query(models.Person).filter(models.Person.person_id == person_id).first()
    db_person.name = person.name
    db_person.age = person.age
    db_person.gender = person.gender
    db_person.condition = person.condition
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int):
    db_person = db.query(models.Person).filter(models.Person.person_id == person_id).first()
    db.delete(db_person)
    db.commit()
    return db_person


####################

def create_position(db: Session, person_id: int, position = schemas.PositionCreate):
    db_position = models.Position(person_id = person_id, long = position.long, lat = position.lat, date = position.date)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

def get_positions(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.person_id == person_id).first().positions.all()

def get_position(db: Session, person_id: int, position_id: int):
    return db.query(models.Person).filter(models.Person.person_id == person_id).first().positions.filter(models.Position.position_id == position_id).first()

def delete_position(db: Session, person_id: int, position_id: int):
    db_position = db.query(models.Person).filter(models.Person.person_id == person_id).first().positions.filter(models.Position.position_id == position_id).first()
    db.delete(db_position)
    db.commit()
    return db_position

####################

def check(pos: models.Position, pos_other: models.Position):
    # print("#"*40)
    # print(f"Person: {pos}")
    # print(f"Person other: {pos_other}")

    # Less than 5 minutes
    ret = (pos.date-pos_other.date).total_seconds() <= (60*5)
    # Distance lesser than 100
    # ret = ret & (math.sqrt(pow(pos.long-pos_other.long, 2) + pow(pos.lat-pos_other.lat, 2)) <= 100)
    ret = ret & (distance.distance((pos.lat, pos.long), (pos_other.lat, pos_other.long)).m <= 100)
    # Only sick person
    ret = ret & ( (pos_other.person.condition == models.KondisiEnum.sakit) | (pos.person.condition == models.KondisiEnum.sakit) )

    return ret

def get_traces(db: Session, person_id: int):
    positions = db.query(models.Person).filter(models.Person.person_id == person_id).first().positions.all()
    person_others = db.query(models.Person).filter(models.Person.person_id != person_id).all()
    positions_others = []

    for person in person_others:
        positions_others.extend(person.positions.all())
    
    ret = []

    for pos in positions:
        for pos_other in positions_others:
            if(check(pos, pos_other)):
                ret.append(schemas.PositionTraced(
                    date = pos.date,
                    position_id = pos.position_id,
                    long = pos.long,
                    lat = pos.lat,
                    contacted_position_id = pos_other.position_id,
                    contacted_long = pos_other.long,
                    contacted_lat = pos_other.lat,
                    contacted_person_id = pos_other.person_id,
                    contact = True
                ))  
    return ret