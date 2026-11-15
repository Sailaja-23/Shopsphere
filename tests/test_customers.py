def test_create_customer(client):
 
    response = client.post(

        "/api/customers/",

        json={

            "name": "Test Customer",

            "email": "test@example.com",

            "phone": "9876543210"

        }

    )
 
    assert response.status_code == 200
 
    data = response.json()
 
    assert data["name"] == "Test Customer"

    assert data["email"] == "test@example.com"

    assert "id" in data
 
 
def test_invalid_customer_email(client):
 
    response = client.post(

        "/api/customers/",

        json={

            "name": "Test Customer",

            "email": "invalid-email",

            "phone": "9876543210"

        }

    )
 
    assert response.status_code == 422
 
 
def test_duplicate_customer_email(client):
 
    customer = {

        "name": "Test Customer",

        "email": "duplicate@example.com",

        "phone": "9876543210"

    }
 
    first_response = client.post(

        "/api/customers/",

        json=customer

    )
 
    second_response = client.post(

        "/api/customers/",

        json=customer

    )
 
    assert first_response.status_code == 200
 
    assert second_response.status_code == 409
 
