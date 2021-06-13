from sqlalchemy import Enum, Boolean, Column, ForeignKey, Integer, Float, DateTime, String
from sqlalchemy.orm import relationship
import enum

from .database import Base

class KondisiEnum(enum.Enum):
    sehat = 1
    sakit = 2

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key = True, index = True)
    username = Column(String, index = True)
    password = Column(String(60))
    level = Column(Integer)

class Person(Base):
    __tablename__ = "person"

    person_id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    gender = Column(String(60), index = True)
    age = Column(Integer, index = True)
    condition = Column(Enum(KondisiEnum), index = True)

    positions = relationship("Position", back_populates = "person", lazy='dynamic')

class Position(Base):
    __tablename__ = "position"

    position_id = Column(Integer, primary_key = True, index = True)
    person_id = Column(Integer, ForeignKey('person.person_id'))
    person = relationship("Person", back_populates = "positions")
    long = Column(Float)
    lat = Column(Float)
    date = Column(DateTime)

    def __str__(self) -> str:
        ret  = f"position_id = {self.position_id}\n"
        ret += f"person_id = {self.person_id}\n"
        ret += f"long = {self.long}\n"
        ret += f"lat = {self.lat}\n"
        ret += f"date = {self.date}\n"
        ret += f"person.condition = {self.person.condition}"
        return ret