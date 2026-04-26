import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app as flask_app, api
from data import db_session, users_resource, jobs_resource
from data.users import User
from data.jobs import Jobs


@pytest.fixture(scope="session", autouse=True)
def setup_app(tmp_path_factory):
    db_path = str(tmp_path_factory.mktemp("db") / "test.db")
    db_session.global_init(db_path)

    api.add_resource(users_resource.UsersListResource, "/api/v2/users")
    api.add_resource(users_resource.UsersResource, "/api/v2/users/<int:users_id>")
    api.add_resource(jobs_resource.JobsListResource, "/api/v2/jobs")
    api.add_resource(jobs_resource.JobsResource, "/api/v2/jobs/<int:jobs_id>")

    flask_app.config["TESTING"] = True


@pytest.fixture
def client():
    return flask_app.test_client()


@pytest.fixture(autouse=True)
def clean_tables():
    yield
    session = db_session.create_session()
    session.query(Jobs).delete()
    session.query(User).delete()
    session.commit()
    session.close()


USER_DATA = {
    "surname": "Иванов",
    "name": "Иван",
    "age": 30,
    "position": "Инженер",
    "speciality": "Python",
    "address": "Москва",
    "email": "ivan@example.com",
    "hashed_password": "secret123",
}

JOB_DATA = {
    "team_leader": 1,
    "job": "Разработка модуля авторизации",
    "work_size": 20,
    "collaborators": "2, 3",
    "start_date": "2024-03-20",
    "end_date": "2024-03-27",
    "is_finished": False,
}
