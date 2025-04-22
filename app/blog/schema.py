from typing import Optional,List
from pydantic import BaseModel
from app.category.schema import CategorySchema,CategoryBase



class BlogSchema(BaseModel):
    id : int
    blogname: str
    blogcontent: str
    blogdesc: str
    blogauthor: str
    status: Optional[str] = "unpublished"
    cid: int
    

    class Config:
        from_attributes = True


class BlogResponseSchema(BlogSchema):
    id: int

    class Config:
        orm_mode = True


class BlogListResponse(BaseModel):
    status: str
    data: List[BlogSchema]
    count: int
    # category: List[CategorySchema]
    # subCategory: List[CategorySchema]

    class Config:
        orm_mode = True

class CommentSchema(BaseModel):
    comment: str
    commentedby: str
    blog_id: int
    
class CommentResponseSchema(CommentSchema):
    comment_id: int

    class Config:
        orm_mode = True

class CommentListResponse(BaseModel):
    status:str
    data : List[CommentSchema]

class BlogBase(BaseModel):
    id: int
    blogname: str
    category: Optional[CategoryBase] 

    class Config:
        orm_mode = True



# class CategorySchema(BaseModel):
#     cname:str
#     p_id : Optional[int] = 0

# class CategoryResponseSchema(CategorySchema):
#     c_id: int
    
#     class Config:
#         orm_mode = True

# class CategoryListResponse(BaseModel):
#     status:str
#     data : List[CategorySchema]
#     count: int




# Base.metadata.create_all(bind=engine)