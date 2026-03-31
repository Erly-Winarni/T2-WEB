def test_access_without_auth(client):
    res = client.get("/items/")
    assert res.status_code == 200 


def test_delete_without_role_control(client):
    create = client.post("/items/", json={
        "name": "RBAC Test",
        "description": "Testing"
    })

    item_id = create.json()["id"]

    res = client.delete(f"/items/{item_id}")

    assert res.status_code == 200