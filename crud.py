import random
import string
from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_userName(db: Session, userName: str):
    return db.query(models.User).filter(models.User.userName == userName).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()



def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    password = user.password
    db_user = models.User(email=user.email, userName=user.userName, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def verify_user(db: Session, userName: str, password: str) -> bool:
    count = db.query(models.User).filter(models.User.userName == userName ,models.User.password == password).count()
    return (count > 0)

def generate_token(db: Session, userName: str) -> str:
    db_user = get_user_by_userName(db, userName=userName)
    db_user.loginToken = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    db.commit()
    return db_user.loginToken
