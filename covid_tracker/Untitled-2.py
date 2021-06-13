def create_position(db: Session, position_id: int, position = schemas.PositionCreate):
    db_position = models.Person(name = position.name, age = position.age, gender = position.gender, condition = position.condition)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position