def test_home_endpoint(client):
 
    response = client.get("/")
 
    assert response.status_code == 200
 
    data = response.json()
 
    assert data["message"] == "Welcome to ShopSphere!"
    assert data["status"] == "Application is running"
 
 
def test_health_endpoint(client):
 
    response = client.get("/health")
 
    assert response.status_code == 200
 
    assert response.json() == {
        "status": "healthy"
    }
 
 
def test_about_endpoint(client):
 
    response = client.get("/about")
 
    assert response.status_code == 200
 
    assert response.json()["application"] == "ShopSphere"
