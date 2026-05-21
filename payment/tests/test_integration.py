import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
import sys

# Uveri se da je database mockovan
from main import app

client = TestClient(app)

def test_get_order_not_found():
    """Integracioni test: API poziv za nepostojeći order"""
    # Direktno testiramo API, bez Order.get
    response = client.get("/orders/99999")
    assert response.status_code == 404

@patch('main.httpx.AsyncClient.get')
def test_create_order_product_not_found(mock_http_get):
    """Integracioni test: Kreiranje order-a za nepostojeći proizvod"""
    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_http_get.return_value = mock_response
    
    response = client.post("/orders", json={"id": "invalid", "quantity": 1})
    assert response.status_code == 400
    assert "Product not found" in response.json()["detail"]

@patch('main.httpx.AsyncClient.get')
def test_create_order_success(mock_http_get):
    """Integracioni test: Uspešno kreiranje order-a"""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value={
        "id": "prod123",
        "name": "Test Product",
        "price": 100.0,
        "quantity": 10
    })
    mock_http_get.return_value = mock_response
    
    response = client.post("/orders", json={"id": "prod123", "quantity": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == "prod123"
    assert data["price"] == 100.0
    assert data["quantity"] == 2
    assert "pk" in data