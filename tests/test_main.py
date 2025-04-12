from fastapi import status
from fastapi.testclient import TestClient


def test_read_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to AI Engineer API"}
