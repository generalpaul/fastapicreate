from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Product
from database import SessionLocal
from .auth import get_current_user

#router = APIRouter()

router = APIRouter(
    prefix='/product',
    tags=['product']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class ProductModel(BaseModel):
    product_id: str = Field(min_length=5)
    product_short_name: str = Field(min_length=3, max_length=50)
    product_long_name: str = Field(min_length=10, max_length=100)
   

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Product).all()


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def read_product(user: user_dependency, db: db_dependency, Product_Id: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    product_model = db.query(Product).filter(Product.product_id == Product_Id).first()
    if product_model is not None:
        return product_model
    raise HTTPException(status_code=404, detail='Product not found.')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(user: user_dependency, db: db_dependency,
                      product_request: ProductModel):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    product_model = Product(**product_request.model_dump())

    db.add(product_model)
    db.commit()


@router.put("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_product(user: user_dependency, db: db_dependency,
                      product_request: ProductModel,
                      product_id: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    product_model = db.query(Product).filter(Product.product_id == product_id).first()
    if product_model is None:
        raise HTTPException(status_code=404, detail='product not found.')

    product_model.Product_Long_Name = product_request.Product_Long_Name
    product_model.Product_Short_Name = product_request.Product_Short_Name
    

    db.add(product_model)
    db.commit()


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(user: user_dependency, db: db_dependency, product_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    product_model = db.query(Product).filter(Product.product_id == product_id).first()
    if product_model is None:
        raise HTTPException(status_code=404, detail='product not found.')
    db.query(Product).filter(Product.product_id == product_id).delete()

    db.commit()












