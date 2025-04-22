from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.users import schemas,crud
from app.users.dependencies import get_db

user_router=APIRouter(prefix="/users",tags=["Users"])

@user_router.post('/',response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session= Depends(get_db)):
    return crud.create_user(db,user)

@user_router.get('/',response_model=list[schemas.UserOut])
def read_users(skip:int=0,limit:int=10,db:Session=Depends(get_db)):
    return crud.get_users(db,skip,limit)
    

@user_router.get('/{user_id}',response_model=schemas.UserOut)
def read_user(user_id:int,db:Session=Depends(get_db)):
    user=crud.get_user(db,user_id)
    if not user:
        raise HTTPException(status_code=404,details='User not found')
    return user

@user_router.put('/{user_id}',response_model=schemas.UserOut)
def update_user(user_id:int,user:schemas.UserUpdate,db:Session=Depends(get_db)):
    return crud.update_user(db,user_id,user)

@user_router.delete("/{user_id}",response_model=schemas.UserOut)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    return crud.delete_user(db,user_id)


@user_router.get("all")
def get_all_users(search:str=None,min_age:int=None,max_age:int=None,sort_by:str="id",sort_order:str="asc",page:int=1,limit:int=10,db:Session=Depends(get_db),):
    filters =schemas.UserFilters(
        search = search,min_age=min_age,max_age=max_age,sort_by =sort_by,sort_order=sort_order,page=page,limit=limit
    )
    return crud.get_all_users_advanced(db,filters)



