def test_create_order(client):
 
    # Create customer
    customer_response = client.post(
        "/api/customers/",
        json={
            "name": "Order Customer",
            "email": "order@example.com",
            "phone": "9876543210"
        }
    )
 
    customer_id = customer_response.json()["id"]
 
    # Create product
    product_response = client.post(
        "/api/products/",
        json={
            "name": "Test Laptop",
            "description": "Laptop for testing",
            "price": 50000,
            "quantity": 10
        }
    )
 
    product_id = product_response.json()["id"]
 
    # Place order
    order_response = client.post(
        "/api/orders/",
        json={
            "customer_id": customer_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2
                }
            ]
        }
    )
 
    assert order_response.status_code == 200
 
    data = order_response.json()
 
    assert data["customer_id"] == customer_id
    assert data["total_amount"] == 100000
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2
 
 
def test_order_reduces_product_stock(client):
 
    customer = client.post(
        "/api/customers/",
        json={
            "name": "Stock Customer",
            "email": "stock@example.com",
            "phone": "9876543210"
        }
    ).json()
 
    product = client.post(
        "/api/products/",
        json={
            "name": "Stock Laptop",
            "description": "Stock test",
            "price": 40000,
            "quantity": 10
        }
    ).json()
 
    client.post(
        "/api/orders/",
        json={
            "customer_id": customer["id"],
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 3
                }
            ]
        }
    )
 
    response = client.get("/api/products/")
 
    remaining_stock = response.json()[0]["quantity"]
 
    assert remaining_stock == 7
 
 
def test_order_with_insufficient_stock(client):
 
    customer = client.post(
        "/api/customers/",
        json={
            "name": "Stock Customer",
            "email": "lowstock@example.com",
            "phone": "9876543210"
        }
    ).json()
 
    product = client.post(
        "/api/products/",
        json={
            "name": "Limited Product",
            "description": "Limited stock",
            "price": 1000,
            "quantity": 2
        }
    ).json()
 
    response = client.post(
        "/api/orders/",
        json={
            "customer_id": customer["id"],
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 5
                }
            ]
        }
    )
 
    assert response.status_code == 400
