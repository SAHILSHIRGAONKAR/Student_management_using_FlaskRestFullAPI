import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

# Test GET /students endpoint
def test_get_students(client):
    response = client.get('/students')
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) > 0

    # Validate the structure of each student object
    for student in data:
        assert isinstance(student, dict)
        assert 'roll_no' in student
        assert 'name' in student
        assert 'class' in student
        assert 'city' in student  # Check for 'city' key in each student's dictionary
        assert 'gender' in student
        assert 'dob' in student
        assert 'subjects' in student
        assert isinstance(student['subjects'], list)
        assert all(isinstance(subject, dict) for subject in student['subjects'])
        assert all('subject_id' in subject for subject in student['subjects'])
        assert all('subject_name' in subject for subject in student['subjects'])
        assert all('marks' in subject for subject in student['subjects'])


def test_get_student_by_id(client):
    response = client.get('/students/2')
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, dict)
    assert len(data) > 0

    # Validate the structure of each student object
    for student in data:
        assert 'roll_no' in data
        assert 'name' in data
        assert 'class' in data
        assert 'city' in data
        assert 'gender' in data
        assert 'dob' in data
        assert 'subjects' in data
        assert isinstance(data['subjects'], list)
        assert all(isinstance(subject, dict) for subject in data['subjects'])
        assert all('subject_id' in subject for subject in data['subjects'])
        assert all('subject_name' in subject for subject in data['subjects'])
        assert all('marks' in subject for subject in data['subjects'])


def test_get_student_by_city(client):
    response = client.get('/students/Mumbai')
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)
    assert len(data) > 0

    # Validate the structure of each student object
    for student in data:
        assert isinstance(student, dict)
        assert 'roll_no' in student
        assert 'name' in student
        assert 'class' in student
        assert 'city' in student  # Check for 'city' key in each student's dictionary
        assert 'gender' in student
        assert 'dob' in student
        assert 'subjects' in student
        assert isinstance(student['subjects'], list)
        assert all(isinstance(subject, dict) for subject in student['subjects'])
        assert all('subject_id' in subject for subject in student['subjects'])
        assert all('subject_name' in subject for subject in student['subjects'])
        assert all('marks' in subject for subject in student['subjects'])

# def test_get_subjects(client):
#     response = client.get('/subjects')
#     assert response.status_code == 400
#     data = response.json
#     assert isinstance(data, list)
#     assert len(data) > 0
#
#     # Validate the structure of each student object
#     for subject in data:
#         assert isinstance(subject, dict)
#         #assert 'id' in subject
#         assert 'message' in subject
#         # assert response.status_code == 400

