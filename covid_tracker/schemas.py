from datetime import datetime
import enum
from typing import List, Optional

from pydantic import BaseModel

from .models import KondisiEnum

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    level: int
    password: str


class User(UserBase):
    user_id: int
    level: int
    password: str

    class Config:
        orm_mode = True


class PersonBase(BaseModel):
    name: str

class PersonCreate(PersonBase):
    gender: str
    age: int
    condition: KondisiEnum

class Person(PersonBase):
    person_id: int
    gender: str
    age: int
    condition: KondisiEnum

    class Config:
        orm_mode = True

class PersonBase(BaseModel):
    name: str

class PersonCreate(PersonBase):
    gender: str
    age: int
    condition: KondisiEnum

class Person(PersonBase):
    person_id: int
    gender: str
    age: int
    condition: KondisiEnum

    class Config:
        orm_mode = True


class PositionBase(BaseModel):
    date: datetime

class PositionCreate(PositionBase):
    long: float
    lat: float

class Position(PositionBase):
    position_id: int
    long: float
    lat: float

    class Config:
        orm_mode = True

class PositionTraced(PositionBase):
    position_id: int
    long: float
    lat: float
    contacted_position_id: int
    contacted_long: float
    contacted_lat: float
    contacted_person_id: int
    contact: bool