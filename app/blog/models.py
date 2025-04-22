from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class BlogModel(Base):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True, index=True)
    blogname = Column(String)
    blogcontent = Column(Text)
    blogdesc = Column(String)
    blogauthor = Column(String)
    cid = Column(Integer, ForeignKey('categories.c_id'))
    status = Column(String(50), default="unpublished")
    soft_delete = Column(Integer, default=0)

    category = relationship("CategoryModel", back_populates="blogs")
    comments = relationship("CommentModel", back_populates="blog")


class CommentModel(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)
    commentedby = Column(String)
    soft_delete = Column(Integer, default=0)
    blog_id = Column(Integer, ForeignKey('blog.id'))

    blog = relationship("BlogModel", back_populates="comments")


# class BlogBase(BaseModel):
#     id: int
#     blogname: str
#     category: Optional[CategoryBase]  # nested category info

#     class Config:
#         orm_mode = True



# class CategoryModel(Base):
#     __tablename__ = 'categories'
#     c_id = Column(Integer, primary_key=True, index=True)
#     cname = Column(String, nullable=False)
#     p_id = Column(Integer, ForeignKey('categories.c_id'))

#     parent = relationship("CategoryModel", remote_side=[c_id], backref="children")
#     blogs = relationship("BlogModel", back_populates="category")






