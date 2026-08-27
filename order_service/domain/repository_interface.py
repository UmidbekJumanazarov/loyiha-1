from abc import ABC, abstractmethod
from typing import Optional

from order_service.domain.models import Order


class OrderRepositoryInterface(ABC):
    """Buyurtmalar uchun saqlash interfeysi (dependent inversion)."""

    @abstractmethod
    async def save(self, order: Order) -> Order:
        """Buyurtmani saqlaydi va id berilgan Order obyektini qaytaradi."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """Buyurtmani id bo'yicha qidiradi."""
        raise NotImplementedError