from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Product, Product_Sub
from database import SessionLocal
from .auth import get_current_user

#router = APIRouter()

router = APIRouter(
    prefix='/product_sub',
    tags=['product_sub']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class Product_SubModel(BaseModel):
    product_sub_id: int 
    product_id: str = Field(min_length=5)
    product_sub_code: str = Field(min_length=5)
    barcode: str = Field(min_length=5)
    amount: float = Field(gt=0)
   

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Product_Sub).all()


@router.get("/{product_sub_id}", status_code=status.HTTP_200_OK)
async def read_product_sub(user: user_dependency, db: db_dependency, Product_Sub_Id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    product_sub_model = db.query(Product_Sub).filter(Product_Sub.Product_Sub_Id == Product_Sub_Id).first()
    if product_sub_model is not None:
        return product_sub_model
    raise HTTPException(status_code=404, detail='Product_Sub not found.')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product_sub(db: db_dependency, user: user_dependency,
                      product_sub_request: Product_SubModel):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    product_model = db.query(Product).filter(Product.product_id == product_sub_request.product_id).first()
    if product_model is None:
        raise HTTPException(status_code=404, detail='Product not found.')
    
    product_sub_model = Product_Sub(**product_sub_request.model_dump())

    db.add(product_sub_model)
    db.commit()


@router.put("/{product_sub_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_product_sub(user: user_dependency, db: db_dependency,
                      product_sub_request: Product_SubModel,
                      product_sub_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    product_sub_model = db.query(Product_Sub).filter(Product_Sub.Product_Sub_Id == product_sub_id).first()
    if product_sub_model is None:
        raise HTTPException(status_code=404, detail='product_sub not found.')

    product_sub_model.Product_Sub_Long_Name = product_sub_request.Product_Sub_Long_Name
    product_sub_model.Product_Sub_Short_Name = product_sub_request.Product_Sub_Short_Name
    

    db.add(product_sub_model)
    db.commit()


@router.delete("/{product_sub_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_sub(user: user_dependency, db: db_dependency, product_sub_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    product_sub_model = db.query(Product_Sub).filter(Product_Sub.Product_Sub_Id == product_sub_id).first()
    if product_sub_model is None:
        raise HTTPException(status_code=404, detail='product_sub not found.')
    db.query(Product_Sub).filter(Product_Sub.Product_Sub_Id == product_sub_id).delete()

    db.commit()












