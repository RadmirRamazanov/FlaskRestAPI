import pytest
from tests.conftest import USER_DATA


def create_user(client, data=None):
    return client.post("/api/v2/users", json=data or USER_DATA)


class TestGetUsers:
    def test_список_пуст_при_отсутствии_пользователей(self, client):
        res = client.get("/api/v2/users")
        assert res.status_code == 200
        assert res.json["users"] == []

    def test_возвращает_всех_пользователей(self, client):
        create_user(client)
        create_user(client, {**USER_DATA, "email": "other@example.com"})

        res = client.get("/api/v2/users")
        assert res.status_code == 200
        assert len(res.json["users"]) == 2

    def test_ответ_содержит_нужные_поля(self, client):
        create_user(client)
        res = client.get("/api/v2/users")
        user = res.json["users"][0]
        assert "surname" in user
        assert "email" in user
        assert "id" not in user


class TestGetUserById:
    def test_возвращает_пользователя_по_id(self, client):
        user_id = create_user(client).json["id"]
        res = client.get(f"/api/v2/users/{user_id}")
        assert res.status_code == 200
        assert res.json["users"]["email"] == USER_DATA["email"]

    def test_404_если_пользователь_не_найден(self, client):
        res = client.get("/api/v2/users/9999")
        assert res.status_code == 404
        assert "not found" in res.json["message"]


class TestPostUser:
    def test_создаёт_пользователя_и_возвращает_id(self, client):
        res = create_user(client)
        assert res.status_code == 200
        assert "id" in res.json
        assert isinstance(res.json["id"], int)

    def test_400_при_отсутствии_обязательного_поля(self, client):
        data = {k: v for k, v in USER_DATA.items() if k != "surname"}
        res = client.post("/api/v2/users", json=data)
        assert res.status_code == 400

    def test_400_при_пустом_теле_запроса(self, client):
        res = client.post("/api/v2/users", json={})
        assert res.status_code == 400

    def test_сообщение_об_ошибке_содержит_имя_поля(self, client):
        res = client.post("/api/v2/users", json={})
        assert "message" in res.json


class TestDeleteUser:
    def test_удаляет_существующего_пользователя(self, client):
        user_id = create_user(client).json["id"]
        res = client.delete(f"/api/v2/users/{user_id}")
        assert res.status_code == 200
        assert res.json["success"] == "OK"

    def test_после_удаления_пользователь_не_найден(self, client):
        user_id = create_user(client).json["id"]
        client.delete(f"/api/v2/users/{user_id}")
        res = client.get(f"/api/v2/users/{user_id}")
        assert res.status_code == 404

    def test_404_при_удалении_несуществующего_пользователя(self, client):
        res = client.delete("/api/v2/users/9999")
        assert res.status_code == 404
        assert "not found" in res.json["message"]
