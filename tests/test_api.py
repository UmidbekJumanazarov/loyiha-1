import httpx
import pytest

from main import app


@pytest.fixture
def client():
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    )


@pytest.mark.asyncio
async def test_api_create_order_success(client):
    async with client:
        resp = await client.post(
            "/api/orders/",
            json={
                "customer_email": "x@example.com",
                "items": [{"product_name": "Kitob", "price": 8.0, "quantity": 2}],
            },
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "success"
    assert data["total"] == 16.0
    assert data["order_id"] > 0


@pytest.mark.asyncio
async def test_api_create_order_below_minimum(client):
    async with client:
        resp = await client.post(
            "/api/orders/",
            json={
                "customer_email": "x@example.com",
                "items": [{"product_name": "Stiker", "price": 3.0, "quantity": 1}],
            },
        )
    assert resp.status_code == 400
    assert "10" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_api_create_order_invalid_email(client):
    async with client:
        resp = await client.post(
            "/api/orders/",
            json={
                "customer_email": "not-an-email",
                "items": [{"product_name": "Kitob", "price": 8.0, "quantity": 2}],
            },
        )
    assert resp.status_code == 422