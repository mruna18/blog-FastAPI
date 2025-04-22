from sqlalchemy.orm import Session
from . import models,schemas
from sqlalchemy import or_, desc, asc

def create_user(db:Session,user:schemas.UserCreate):
    db_user =models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db:Session,user_id : int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db:Session,skip:int=0,limit:int=10):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db:Session,user_id:int,user:schemas.UserUpdate):
    db_user=db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    
    for var,value in vars(user).items():
        # print(var)
        print(value)
        setattr(db_user,var,value)
        if not value is not None:
            setattr(db_user,var,value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session,user_id:int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user:
        db.delete(user)
        db.commit()
    return user

def search_users(db:Session,name:str):
    return db.query(models.User).filter(models.User.name.ilike(f"%{name}")).all()

def get_paginated_users(db:Session,page:int=1,size:int=10):
    return db.query(models.User).offser((page-1)* size).limit(size).all()

def get_all_users_advanced(db:Session,filters:schemas.UserFilters):
    query=db.query(models.User)
    if filters.search:
        search_term=f"%{filters.search}%"
        query=query.filter(or_(models.User.name.ilike(search_term),models.User.email.ilike(search_term)))
      

    if filters.min_age is not None:
        query=query.filter(models.User.age >= filters.min_age)

    if filters.max_age is not None:
        query =query.filter(models.User.age <= filters.max_age)

    sort_column = getattr(models.User,filters.sort_by,None)
    if sort_column is not None:
        sort_func = desc if filters.sort_order == "desc" else asc
        query = query.order_by (sort_func(sort_column))

    total =query.count()
    offset=(filters.page -1)* filters.limit
    users = query.offset(offset).limit(filters.limit).all()

    return {
        "total":total,
        "page":filters.page,
        "limit":filters.limit,
        "data": users
    }


        