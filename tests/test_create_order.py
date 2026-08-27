import pytest

from order_service.domain.models import Order, OrderItem
from order_service.use_cases.create_order import CreateOrderUseCase


class FakeRepo:
    """Testlar uchun xotiradagi repository (interfeysga bog'liq)."""

    def __init__(self):
        self.saved = None

    async def save(self, order):
        order.id = 1
        self.saved = order
        return order


@pytest.mark.asyncio
async def test_create_order_success():
    repo = FakeRepo()
    use_case = CreateOrderUseCase(repo)

    result = await use_case.execute(
        email="x@example.com",
        items_data=[
            {"product_name": "Kitob", "price": 8.0, "quantity": 2},
        ],
    )

    assert result.id == 1
    assert result.total_price == 16.0
    assert repo.saved is not None


@pytest.mark.asyncio
async def test_create_order_empty_items_raises():
    repo = FakeRepo()
    use_case = CreateOrderUseCase(repo)

    with pytest.raises(ValueError, match="kamida bitta mahsulot"):
        await use_case.execute(email="x@example.com", items_data=[])


@pytest.mark.asyncio
async def test_create_order_below_minimum_raises():
    repo = FakeRepo()
    use_case = CreateOrderUseCase(repo)

    with pytest.raises(ValueError, match="10"):
        await use_case.execute(
            email="x@example.com",
            items_data=[{"product_name": "Stiker", "price": 3.0, "quantity": 1}],
        )


@pytest.mark.asyncio
async def test_domain_total_price():
    order = Order(
        id=None,
        customer_email="a@b.com",
        items=[
            OrderItem(product_name="A", price=2.0, quantity=3),
            OrderItem(product_name="B", price=1.5, quantity=2),
        ],
    )
    assert order.total_price == 9.0