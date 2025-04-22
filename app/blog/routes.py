from fastapi import FastAPI, Depends, HTTPException,APIRouter,status,Query
from sqlalchemy.orm import Session    
from typing import List
from app.blog.schema import *
from app.database import *
from app.blog.models import *
from app.category.models import *
from app.category.schema import *



# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
router = APIRouter(
    prefix="/blog",
    tags=["Blog"],
   

)

@router.get("/")
def index():
    return {"message": "Hello, World!"}



@router.post("/add", response_model=BlogResponseSchema,status_code=200)
def add_blog(blog: BlogSchema, db: Session = Depends(get_db)):
    new_blog = BlogModel(
        blogname=blog.blogname,
        blogcontent=blog.blogcontent,
        blogdesc=blog.blogdesc,
        blogauthor=blog.blogauthor,
        status=blog.status,
        cid=blog.cid,
      

    )
    # new_blog=BlogModel(**blog.dict())

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    # return  {"status": "sucess","data":new_blog}
    return  new_blog


#!!!!!!!get all the blogs!!!!!!!!!
@router.get("/all_blogs")
def get_all_blogs(
    category_id: int = Query(..., description="Main or sub category ID"),search: str = Query(None, description="Optional search search"),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
   
    category = db.query(CategoryModel).filter(CategoryModel.c_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")


    category_ids = [category.c_id]
    if category.p_id is None:
        sub_cats = db.query(CategoryModel.c_id).filter(CategoryModel.p_id == category.c_id).all()
        category_ids += [c[0] for c in sub_cats]


    blog_query = db.query(BlogModel).filter(BlogModel.cid.in_(category_ids))

    # if search is None:
    #     categories = db.query(BlogModel).all()
    #     c = len(categories)
    #     return {
    #     "status":"success",
    #     "data":categories,
    #     "count":c
    # }
  
    if search:
        blog_query = blog_query.filter(BlogModel.blogname.like(f"%{search}%"))
        # blog_query = db.query(BlogModel).filter(BlogModel.blogname.like(f"%{search}%%")).all()
        # c=len(blog_query)
        # return {
        #     "status":"success",
        #     "data":blog_query,
        #     "count":c
        # }

    blogs = blog_query.offset(offset).limit(limit).all()

    blog_data = []
    for blog in blogs:
        sub_cat = db.query(CategoryModel).filter(CategoryModel.c_id == blog.cid).first()
        main_cat = db.query(CategoryModel).filter(CategoryModel.c_id == sub_cat.p_id).first() if sub_cat and sub_cat.p_id else None

        blog_data.append({
            "blog": blog,
            "subcategory": sub_cat.cname if sub_cat else None,
            "main_category": main_cat.cname if main_cat else None
        })

    return {
        "status": "success",
        "category_id": category_id,
        "search": search,
        "total_results": len(blog_data),
        "blogs": blog_data
    }    
                                           

#! by id all blog
# 
@router.get("/all_blog/{blog_id}")
def get_blog_by_id(blog_id: int,search : str = Query(None),limit : int= Query(10,ge=1), offset: int= Query(10,ge=0), db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    # category = db.query(CategoryModel).filter(CategoryModel.cname == category_name).first()
    if not blog:

        raise HTTPException(status_code=404, detail="blog not found")
    
    # cat_filter = db.query(CategoryModel).filter(CategoryModel.c_id == blog.cid).first()
    # cat_main_filter = db.query(CategoryModel).filter(CategoryModel.c_id == cat_filter.p_id).first()
    # category_ids = [category.c_id]
    # if category.p_id is None:
    #     sub_cats = db.query(CategoryModel.c_id).filter(CategoryModel.p_id == category.c_id).all()
    #     category_ids += [c[0] for c in sub_cats]
    

    # blog_query =db.query(BlogModel).filter(BlogModel.cid.in_(category_ids))
    # if search :
    #     blog_query = blog_query.filter(
    #         BlogModel.blogname.ilike(f"%{search}%"),
    #         BlogModel.blogdesc.ilike(f"%{search}%")
    #     )

    # blogs = blog_query.offset(offset).limit(limit).all()


    # blog_data=[]

    # for blog in blogs:
    #     sub_cat = db.query(CategoryModel).filter(CategoryModel.c_id== blog.cid).first()  
    #     main_cat = db.query(CategoryModel).filter(CategoryModel.c_id == sub_cat.p_id).first() if sub_cat and sub_cat.p_id else None
            
    #     blog_data.append({
    #         "blog":blog,
    #         "subCategory":sub_cat.cname if sub_cat else None,
    #         "mainCategory":main_cat.cname if main_cat else None
    #     })

    return {

        "status": "success",
        # "searched_category": category.cname,
        # "searched": search,
        "data":blog
       
    }


# @router.get("/all_blog", response_model=BlogListResponse)
# def get_all_blog(search:Optional[str] = None,skip: Optional[int] = None,limit: Optional[int] = None,db: Session = Depends(get_db)):

#     cat = db.query(CategoryModel).filter(CategoryModel.soft_delete == False).all()
#     sub = db.query(CategoryModel).filter(CategoryModel.p_id != None, CategoryModel.soft_delete == False).all()

#     if search:
#         blogs = db.query(BlogModel).filter(BlogModel.blogname.like(f"%{search}%")).offset(skip).limit(limit).all()
#     else:
#         blogs = db.query(BlogModel).all()

#     return {
#         "status": "success",
#         "count": len(blogs),
#         "data": blogs,
#         "category": cat,
#         "subCategory": sub
#     }


@router.put("/update_blog/{blog_id}", response_model=BlogSchema)
def update_blog(blog_id: int, b: BlogSchema, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.blogname = b.blogname
    blog.blogcontent = b.blogcontent
    blog.blogdesc = b.blogdesc
    blog.blogauthor = b.blogauthor
    blog.status = b.status

    db.commit()
    db.refresh(blog)

    return blog

@router.post("/{blog_id}")
def published_my_blog(blog_id:int,db:Session=Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    if blog.status == "unpublished":
        blog.status = "published"
        db.commit()
        db.refresh(blog)
        return {
            "status": "sucess",
            "message": "Blog published successfully",
            "data":blog
        }
    else:
        return {"status": "info",
        "message": "Blog is already published",
        "data": blog 
        }


@router.get("/unpublished_blog/", response_model=BlogListResponse,description=
            'INACTIVE BLOGS')
def get_unpublished_blog(db: Session = Depends(get_db) ):
    blogs = db.query(BlogModel).filter(BlogModel.status == "unpublished").all()
    c= len(blogs)
    return {
        "status": "success",
        "data": blogs,
        "count":c
    }

@router.get("/published_blog/", response_model=BlogListResponse,description=
            'ACTIVE BLOGS')
def get_published_blog(db: Session = Depends(get_db)):
    blogs = db.query(BlogModel).filter(BlogModel.status == "published").all()
    c= len(blogs)

    return {
        "status": "success",
        "data": blogs,
        "count":c
    }
    


# @router.post("/search/")
# def search_blog(query:str,db: Session = Depends(get_db)):
#     query:str
#     blogs = db.query(BlogModel).filter(BlogModel.blogname.like(f"%{query}%%")).all()
#     return {"status": "success", "data": blogs}

# @router.get("/blog/",response_model = BlogListResponse)
# def get_all_blog(search:Optional[str] = None,skip: Optional[int] = None,limit: Optional[int] = None,db:Session = Depends(get_db)):
#     if search is None:
#         b = db.query(BlogModel).all()
#         c = len(b)
#         return {
#         "status":"success",
#         "data":b,
#         "count":c
#     }
#     else:

#         b = db.query(BlogModel).filter(BlogModel.blogname.like(f"%{search}%%")).all()    
#         Note.query.filter(Note.message.match("%somestr%")).all()  
#         return {
#             "status":"success",
#             "data":b,
#             "count":c
#         }



# @router.post("/search/")
# def search_blog(query: str,db: Session = Depends(get_db)):
    
#     blogs = db.query(BlogModel).filter(BlogModel.blogname.like(f"%{query}%%")).all()
#     return {"status": "success", "data": blogs}


# @router.delete("/{blog_id}")
# def delete_blog(blog_id: int, db: Session = Depends(get_db)):
#     blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()

#     if not blog:
#         raise HTTPException(status_code=404, detail="Blog not found")

#     comments = db.query(CommentModel).filter(CommentModel.blog_id == blog_id).all()
#     for comment in comments:
#         db.delete(comment)

#     db.commit()

#     db.delete(blog)
#     db.commit()

#     return {
#         "status": "success",
#         "message": f"Blog with ID {blog_id} has been deleted."
#     }

@router.delete("/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id, BlogModel.soft_delete == False).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.soft_delete = True
    comments = db.query(CommentModel).filter(CommentModel.blog_id == blog_id, CommentModel.soft_delete == False).all()
    for comment in comments:
        comment.soft_delete = True


    db.commit()

    return {
        "status": "success",
        "message": f"Blog with ID {blog_id} has been soft deleted."
    }



#! COMMETS: 

#* Comments published!!
@router.post("/comment/", response_model=CommentResponseSchema, status_code=status.HTTP_201_CREATED)
def add_comment(comment: CommentSchema, db: Session = Depends(get_db)):

    blog = db.query(BlogModel).filter(BlogModel.id == comment.blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    if blog.status == 'published':
        new_comment = CommentModel(
            
            comment=comment.comment,
            commentedby=comment.commentedby,
            blog_id=comment.blog_id,
          
        )
        # new_comment=CommentModel(**comment.dict())
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    else:
        raise HTTPException(status_code=400, detail="Blog is not published")



# @router.post("/comment/")
# def add_comment_new(comment: CommentSchema, db: Session = Depends(get_db)):
 
#     new_comment = CommentModel(
#         comment=comment.comment,
#         commentedby=comment.commentedby,
#         blog_id=comment.blog_id
#         )
#     db.add(new_comment)
#     db.commit()
#     db.refresh(new_comment)
#     return new_comment


    



@router.get("/all_comment", response_model=CommentListResponse)
def get_all_comment(skip: Optional[int] = None,limit: Optional[int] = None,db:Session = Depends(get_db)):
    comments = db.query(CommentModel).offset(skip).limit(limit).all()
    c=len(comments)
    return {
        "status":"success",
        "data": comments,
        "count":c
    }



@router.delete("/comment/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment =db.query(CommentModel).filter(CommentModel.comment_id == comment_id,CommentModel.soft_delete==False).all()


    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment.soft_delete = True

    # db.delete(comment)
    db.commit()
    return {
        "status": "success",
        "message": f"Comment with ID {comment_id} has been deleted."}
    



















