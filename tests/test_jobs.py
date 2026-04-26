import pytest
from tests.conftest import USER_DATA, JOB_DATA


def create_user(client):
    return client.post("/api/v2/users", json=USER_DATA)


def create_job(client, data=None):
    return client.post("/api/v2/jobs", json=data or JOB_DATA)


class TestGetJobs:
    def test_список_пуст_при_отсутствии_работ(self, client):
        res = client.get("/api/v2/jobs")
        assert res.status_code == 200
        assert res.json["users"] == []

    def test_возвращает_все_работы(self, client):
        create_user(client)
        create_job(client)
        create_job(client, {**JOB_DATA, "job": "Вторая задача"})

        res = client.get("/api/v2/jobs")
        assert res.status_code == 200
        assert len(res.json["users"]) == 2

    def test_ответ_содержит_нужные_поля(self, client):
        create_user(client)
        create_job(client)
        res = client.get("/api/v2/jobs")
        job = res.json["users"][0]
        assert "job" in job
        assert "team_leader" in job
        assert "is_finished" in job
        assert "id" not in job


class TestGetJobById:
    def test_возвращает_работу_по_id(self, client):
        create_user(client)
        job_id = create_job(client).json["id"]
        res = client.get(f"/api/v2/jobs/{job_id}")
        assert res.status_code == 200
        assert res.json["users"]["job"] == JOB_DATA["job"]

    def test_404_если_работа_не_найдена(self, client):
        res = client.get("/api/v2/jobs/9999")
        assert res.status_code == 404
        assert "not found" in res.json["message"]


class TestPostJob:
    def test_создаёт_работу_и_возвращает_id(self, client):
        create_user(client)
        res = create_job(client)
        assert res.status_code == 200
        assert "id" in res.json
        assert isinstance(res.json["id"], int)

    def test_400_при_отсутствии_обязательного_поля(self, client):
        data = {k: v for k, v in JOB_DATA.items() if k != "team_leader"}
        res = client.post("/api/v2/jobs", json=data)
        assert res.status_code == 400

    def test_400_при_пустом_теле_запроса(self, client):
        res = client.post("/api/v2/jobs", json={})
        assert res.status_code == 400

    def test_сообщение_об_ошибке_содержит_имя_поля(self, client):
        res = client.post("/api/v2/jobs", json={})
        assert "message" in res.json


class TestDeleteJob:
    def test_удаляет_существующую_работу(self, client):
        create_user(client)
        job_id = create_job(client).json["id"]
        res = client.delete(f"/api/v2/jobs/{job_id}")
        assert res.status_code == 200
        assert res.json["success"] == "OK"

    def test_после_удаления_работа_не_найдена(self, client):
        create_user(client)
        job_id = create_job(client).json["id"]
        client.delete(f"/api/v2/jobs/{job_id}")
        res = client.get(f"/api/v2/jobs/{job_id}")
        assert res.status_code == 404

    def test_404_при_удалении_несуществующей_работы(self, client):
        res = client.delete("/api/v2/jobs/9999")
        assert res.status_code == 404
        assert "not found" in res.json["message"]
