from fastapi import FastAPI, Depends, HTTPException,APIRouter,status
from sqlalchemy.orm import Session    
from typing import List,Optional
from app.category.schema import *
from app.database import *
from app.category.models import *
#! Categories

category_router = APIRouter(
    prefix="/category",
    tags=["Categories"],
   

)

@category_router.post("/addcategory/",status_code=status.HTTP_201_CREATED,response_model=CategoryResponseSchema)
def add_category(category: CategorySchema, db: Session = Depends(get_db)):
    # new_category = CategoryModel(**category.dict())
    new_category = CategoryModel(
        cname=category.cname,
        p_id = category.p_id 
    )
    if category.p_id == 0:
        new_category.p_id = None
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    else:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category



@category_router.get("all_category",response_model = CategoryListResponse)
def get_all_category(search:Optional[str] = None,skip: Optional[int] = None,limit: Optional[int] = None,db:Session = Depends(get_db)):
    if search is None:
        categories = db.query(CategoryModel).all()
        c = len(categories)
        return {
        "status":"success",
        "data":categories,
        "count":c
    }
    else:

        categories = db.query(CategoryModel).filter(CategoryModel.cname.like(f"%{search}%%")).offset(skip).limit(limit).all()
        c=len(categories)
        return {
            "status":"success",
            "data":categories,
            "count":c
        }




@category_router.delete("/categories/{categories_id}")
def delete_categories(categories_id: int, db: Session = Depends(get_db)):
    categories =db.query(CategoryModel).filter(CategoryModel.categories_id == categories_id,CategoryModel.soft_delete==False).all()


    if not categories:
        raise HTTPException(status_code=404, detail="categories not found")
    categories.soft_delete = True


    db.commit()
    return {
        "status": "success",
        "message": f"categories with ID {categories_id} has been deleted."}
    



@category_router.get("/all_main_categories")
def get_all_main_category(search: Optional[str] = None,skip: Optional[int] = None,limit: Optional[int] = None,
db: Session = Depends(get_db)):
    
    query = db.query(CategoryModel).filter(CategoryModel.p_id == None,CategoryModel.soft_delete == False)

    if search:
        query = query.filter(CategoryModel.cname.like(f"%{search}%"))

    total = query.count()
    results = query.offset(skip).limit(limit).all()

    return {
        "status": "success",
        "data": results,
        "count": total
    }




















