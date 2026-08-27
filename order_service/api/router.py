from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

from order_service.infrastructure.database import SessionFactory
from order_service.infrastructure.sql_repository import SQLAlchemyOrderRepository
from order_service.use_cases.create_order import CreateOrderUseCase

router = APIRouter()


class ItemSchema(BaseModel):
    product_name: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)


class CreateOrderSchema(BaseModel):
    customer_email: EmailStr
    items: list[ItemSchema]


class OrderResponse(BaseModel):
    status: str
    order_id: int
    total: float


def get_repository() -> SQLAlchemyOrderRepository:
    return SQLAlchemyOrderRepository(session_factory=SessionFactory)


@router.post("/orders/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: CreateOrderSchema,
    repo: Annotated[SQLAlchemyOrderRepository, Depends(get_repository)],
):
    use_case = CreateOrderUseCase(repo=repo)
    try:
        result = await use_case.execute(
            email=payload.customer_email,
            items_data=[item.model_dump() for item in payload.items],
        )
        return {
            "status": "success",
            "order_id": result.id,
            "total": result.total_price,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))