def test_create_product(client):
 
    response = client.post(

        "/api/products/",

        json={

            "name": "Laptop",

            "description": "Test laptop",

            "price": 55000,

            "quantity": 10

        }

    )
 
    assert response.status_code == 200
 
    data = response.json()
 
    assert data["name"] == "Laptop"

    assert data["price"] == 55000

    assert data["quantity"] == 10

    assert "id" in data
 
 
def test_get_products(client):
 
    client.post(

        "/api/products/",

        json={

            "name": "Keyboard",

            "description": "Wireless keyboard",

            "price": 1500,

            "quantity": 20

        }

    )
 
    response = client.get("/api/products/")
 
    assert response.status_code == 200
 
    data = response.json()
 
    assert len(data) == 1

    assert data[0]["name"] == "Keyboard"
 
 
def test_invalid_product_price(client):
 
    response = client.post(

        "/api/products/",

        json={

            "name": "Mouse",

            "description": "Test mouse",

            "price": -100,

            "quantity": 10

        }

    )
 
    assert response.status_code == 422
 
 
def test_negative_product_quantity(client):
 
    response = client.post(

        "/api/products/",

        json={

            "name": "Mouse",

            "description": "Test mouse",

            "price": 500,

            "quantity": -5

        }

    )
 
    assert response.status_code == 422
 
