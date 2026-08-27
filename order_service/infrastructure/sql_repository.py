from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from order_service.domain.models import Order, OrderItem
from order_service.domain.repository_interface import OrderRepositoryInterface
from order_service.infrastructure.db_models import OrderItemModel, OrderModel


class SQLAlchemyOrderRepository(OrderRepositoryInterface):
    """SQLAlchemy ORM yordamidagi repository implementatsiyasi."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def save(self, order: Order) -> Order:
        order_row = OrderModel(customer_email=order.customer_email)
        order_row.items = [
            OrderItemModel(
                product_name=item.product_name,
                price=item.price,
                quantity=item.quantity,
            )
            for item in order.items
        ]

        async with self.session_factory() as session:
            session.add(order_row)
            await session.commit()
            await session.refresh(order_row)

            order.id = order_row.id
            return order

    async def get_by_id(self, order_id: int) -> Order | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(OrderModel)
                .where(OrderModel.id == order_id)
                .options(selectinload(OrderModel.items))
            )
            row = result.scalar_one_or_none()
            if row is None:
                return None

            return Order(
                id=row.id,
                customer_email=row.customer_email,
                items=[
                    OrderItem(
                        product_name=item.product_name,
                        price=item.price,
                        quantity=item.quantity,
                    )
                    for item in row.items
                ],
            )