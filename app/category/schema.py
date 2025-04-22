from typing import Optional,List
from pydantic import BaseModel

class CategorySchema(BaseModel):
    c_id:int
    cname:str
    p_id : Optional[int] = 0
    # soft_delete:str

class CategoryResponseSchema(CategorySchema):
    c_id: int
    
    class Config:
        orm_mode = True

class CategoryListResponse(BaseModel):
    status:str
    data : List[CategorySchema]
    count: int
   
class CategoryBase(BaseModel):
    id: int
    cname: str
    p_id: Optional[int]

    class Config:
        orm_mode = True


