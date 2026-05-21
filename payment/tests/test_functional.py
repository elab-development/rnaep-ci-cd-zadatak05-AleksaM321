import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@patch('main.httpx.AsyncClient.get')
def test_complete_order_workflow(mock_http_get):
    """Funkcionalni test: Ceo workflow kreiranja order-a"""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value={
        "id": "prod123",
        "name": "Test Product",
        "price": 50.0,
        "quantity": 5
    })
    mock_http_get.return_value = mock_response
    
    # 1. Kreiraj order
    response = client.post("/orders", json={"id": "prod123", "quantity": 1})
    assert response.status_code == 200
    order_data = response.json()
    
    # 2. Proveri podatke
    assert order_data["status"] == "pending"
    assert order_data["product_id"] == "prod123"
    assert order_data["price"] == 50.0
    assert order_data["fee"] == 10.0  # 20% of 50
    assert order_data["total"] == 60.0  # 1.2 * 50 * 1

@patch('main.httpx.AsyncClient.get')
def test_multiple_orders_different_quantities(mock_http_get):
    """Funkcionalni test: Kreiranje više order-a sa različitim količinama"""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value={
        "id": "prod123",
        "name": "Test Product",
        "price": 100.0,
        "quantity": 10
    })
    mock_http_get.return_value = mock_response
    
    quantities = [1, 2, 3]
    orders = []
    
    for qty in quantities:
        response = client.post("/orders", json={"id": "prod123", "quantity": qty})
        assert response.status_code == 200
        orders.append(response.json())
    
    # Proveri da cena zavisi od količine
    assert orders[0]["total"] == 120.0  # 1 komad
    assert orders[1]["total"] == 240.0  # 2 komada
    assert orders[2]["total"] == 360.0  # 3 komada

@patch('main.httpx.AsyncClient.get')
def test_order_price_calculation(mock_http_get):
    """Funkcionalni test: Provera ispravnosti računanja cena"""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value={
        "id": "prod123",
        "name": "Test Product",
        "price": 75.50,
        "quantity": 10
    })
    mock_http_get.return_value = mock_response
    
    response = client.post("/orders", json={"id": "prod123", "quantity": 3})
    assert response.status_code == 200
    data = response.json()
    
    expected_fee = 75.50 * 0.2  # 15.10
    expected_total = 75.50 * 1.2 * 3  # 271.80
    
    assert data["fee"] == expected_fee
    assert data["total"] == expected_total