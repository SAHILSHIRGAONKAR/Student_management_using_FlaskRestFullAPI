import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app
@pytest.fixture
def client(app):
    return app.test_client()

def test_get_students_bad_request(client):
    response = client.get('/student')
    assert response.status_code == 404

def test_get_subjects(client):
    response = client.get('/subject')
    assert response.status_code == 404  # Check if the response status code is 404 (Not Found)



def test_get_students_by_id_bad_request(client):
    response = client.get('/students/invalid_id')
    assert response.status_code == 400
    # Ensure that the response contains an error message indicating bad request
    # assert b"Bad request" in response.data
    # # Ensure that the response data does not contain any valid student data
    # assert b"name" not in response.data
    # assert b"roll_no" not in response.data
    # assert b"gender" not in response.data
    # assert b"dob" not in response.data

def test_get_students_by_city_bad_request(client):
    response = client.get('/students/invalid_city')
    assert response.status_code == 400
    # Ensure that the response contains an error message indicating bad request
    # assert b"Bad request" in response.data
    # Ensure that the response data does not contain any valid student data
    # assert b"name" not in response.data
    # assert b"roll_no" not in response.data
    # assert b"gender" not in response.data
    # assert b"dob" not in response.data



