from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List,Union
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter(prefix="/products", tags=["products"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Union[schemas.Product, List[schemas.Product]], status_code=201)
def create_product(
    products: Union[schemas.ProductCreate, List[schemas.ProductCreate]],
    db: Session = Depends(get_db) ):
    # Convert single product to list
    if isinstance(products, schemas.ProductCreate):
        products = [products]

    # Validate and create each product
    created_products = []
    for product in products:
        if product.price < 0 or product.amount < 0:
            raise HTTPException(status_code=400, detail="Negative values not allowed")
        created = crud.create_product(db, product)
        created_products.append(created)

    # Return single object if only one product was posted
    return created_products[0] if len(created_products) == 1 else created_products

@router.get("/", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
