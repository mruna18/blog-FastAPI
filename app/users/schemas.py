from pydantic import BaseModel,EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    age: int

class UserUpdate(BaseModel):
    name:Optional[str]=None
    age:Optional[int]=None

class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    age:int

    class Config:
        orm_mode=True

class UserFilters(BaseModel):
    search:Optional[str]=None
    min_age:Optional[int]=None
    max_age:Optional[int] =None
    sort_by:Optional[str]="id"
    sort_order:Optional[str]="asc"
    page:Optional[int]=1
    limit:Optional[int]=10

    
