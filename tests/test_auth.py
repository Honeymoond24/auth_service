# import json
#
# from sqlalchemy import insert, select
#
# from conftest import client, async_session_maker
#
#
# def test_register():
#     response = client.post("/auth/register", data={
#         "username": "string",
#         "password": "string",
#     })
#     print(client.base_url)
#     print(response.url, response.text)
#
#     assert response.status_code == 201
from starlette.testclient import TestClient

from src.main import app

client: TestClient = TestClient(app)


def test_ping():
    response = client.get("/ping")
    print(client.base_url)
    print(response.url, response.text)
    assert response.status_code == 200
    assert response.json() == {"pong": "pong"}


def test_register():
    response = client.post("/auth/register", data={
        "username": "string",
        "password": "string",
    })
    print(client.base_url)
    print(response.url, response.text)
    assert response.status_code == 201
