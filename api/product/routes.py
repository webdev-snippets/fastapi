from fastapi import Depends, Security, status, HTTPException, APIRouter
from typing import Annotated
from sqlmodel import Session, select
from pydantic import ValidationError

from .. import get_session, get_settings, Settings, logger
from ..user.models import User
from ..auth.utils import verify_token
from .models import *
from .utils import *


router = APIRouter(
    tags=["product"],
    prefix="/product"
)


@router.post("", response_model=PublicProduct, description="Create a product", status_code=status.HTTP_201_CREATED)
async def post_booking(*, new_product: CreateProduct, s: Annotated[Session, Depends(get_session)], settings: Annotated[Settings, Depends(get_settings)], user: Annotated[User, Security(verify_token, scopes=["product", "product:write"])]):
    try:
        new_product = Product.model_validate(new_product)
        s.add(new_product)
        s.commit()
        s.refresh(new_product)
        return new_product
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch("/{product_id}", response_model=PublicProduct, description="Update a product", status_code=status.HTTP_200_OK)
async def update_booking(*, product_id: UUID4, update_product: UpdateProduct, s: Annotated[Session, Depends(get_session)], settings: Annotated[Settings, Depends(get_settings)], user: Annotated[User, Security(verify_token, scopes=["product", "product:write"])]):
    try:
        db_product: Product = s.get(Product, product_id)
        db_product = db_product.sqlmodel_update(update_product)
        s.add(db_product)
        s.commit()
        s.refresh(db_product)
        return db_product
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("", response_model=list[PublicProduct], description="get products", status_code=status.HTTP_200_OK)
async def get_products(*, s: Annotated[Session, Depends(get_session)], settings: Annotated[Settings, Depends(get_settings)]):
    try:
        logger.critical(s.exec(select(Product)).all())
        return s.exec(select(Product)).all()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{product_id}", description="delete booking", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(*, product_id: UUID4, s: Annotated[Session, Depends(get_session)], user: Annotated[User, Security(verify_token, scopes=["product", "product:write", "product:delete"])]):
    try:
        p = s.get(Product, product_id)
        s.delete(p)
        s.commit()
        return
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exists")
