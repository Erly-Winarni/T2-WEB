def test_create_item(client):
    res = client.post("/items/", json={
        "name": "Laptop",
        "description": "Gaming"
    })

    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Laptop"
    assert data["description"] == "Gaming"
    assert "id" in data


def test_get_items(client):
    res = client.get("/items/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_single_item(client):
    create = client.post("/items/", json={
        "name": "Mouse",
        "description": "Wireless"
    })

    item_id = create.json()["id"]

    res = client.get(f"/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["name"] == "Mouse"


def test_update_item(client):
    create = client.post("/items/", json={
        "name": "Keyboard",
        "description": "Mechanical"
    })

    item_id = create.json()["id"]

    res = client.put(f"/items/{item_id}", json={
        "name": "Keyboard Updated",
        "description": "RGB"
    })

    assert res.status_code == 200
    assert res.json()["name"] == "Keyboard Updated"


def test_delete_item(client):
    create = client.post("/items/", json={
        "name": "Monitor",
        "description": "24 inch"
    })

    item_id = create.json()["id"]

    res = client.delete(f"/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["message"] == "Item terhapus"