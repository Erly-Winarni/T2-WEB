def test_register_and_login(client):
    # register
    res = client.post("/register", json={
        "username": "user1",
        "password": "123",
        "role": "user"
    })
    assert res.status_code == 200

    # login
    res = client.post("/login", json={
        "username": "user1",
        "password": "123"
    })
    assert res.status_code == 200

    data = res.json()
    assert "access_token" in data

def test_user_cannot_delete(client):
    # register user
    client.post("/register", json={
        "username": "user2",
        "password": "123",
        "role": "user"
    })

    # login
    login = client.post("/login", json={
        "username": "user2",
        "password": "123"
    })
    token = login.json()["access_token"]

    # buat item
    create = client.post("/items/", json={
        "name": "Test",
        "description": "RBAC"
    })
    item_id = create.json()["id"]

    # delete pakai token user
    res = client.delete(
        f"/items/{item_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 403

def test_delete_item(client):
    # register admin
    client.post("/register", json={
        "username": "admin_test",
        "password": "123",
        "role": "admin"
    })

    # login admin
    login = client.post("/login", json={
        "username": "admin_test",
        "password": "123"
    })
    token = login.json()["access_token"]

    # create item
    create = client.post("/items/", json={
        "name": "Monitor",
        "description": "24 inch"
    })
    item_id = create.json()["id"]

    # delete pakai token
    res = client.delete(
        f"/items/{item_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200