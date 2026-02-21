def test_create_user_route(client):
    response = client.post(
        "/contacts/", json={"name": "API", "lastname": "Test", "email": "api@test.com"}
    )

    assert response.status_code == 201
    assert response.get_json()["email"] == "api@test.com"


def test_get_user_404(client):
    response = client.get("/contacts/999")
    assert response.status_code == 404


def test_pagination_validation(client):
    response = client.get("/contacts/?page=1")
    assert response.status_code == 400
