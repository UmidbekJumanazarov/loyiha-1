from order_service.domain.models import Order, OrderItem
from order_service.domain.repository_interface import OrderRepositoryInterface


class CreateOrderUseCase:
    """Buyurtma yaratish uchun biznes mantiq (Application Rule)."""

    MIN_TOTAL_PRICE = 10.0

    def __init__(self, repo: OrderRepositoryInterface):
        self.repo = repo

    async def execute(self, email: str, items_data: list[dict]) -> Order:
        if not items_data:
            raise ValueError("Buyurtmada kamida bitta mahsulot bo'lishi shart!")

        items = [OrderItem(**item) for item in items_data]
        order = Order(id=None, customer_email=email, items=items)

        # Biznes sharti: Minimum buyurtma summasi 10.0$ bo'lishi kerak
        if order.total_price < self.MIN_TOTAL_PRICE:
            raise ValueError(f"Eng kam buyurtma summasi {self.MIN_TOTAL_PRICE:g}$ bo'lishi kerak!")

        return await self.repo.save(order)