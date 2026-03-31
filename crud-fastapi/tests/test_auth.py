def test_register_not_available(client):
    res = client.post("/register", json={
        "username": "user",
        "password": "123"
    })

    assert res.status_code == 404


def test_login_not_available(client):
    res = client.post("/login", json={
        "username": "user",
        "password": "123"
    })

    assert res.status_code == 404