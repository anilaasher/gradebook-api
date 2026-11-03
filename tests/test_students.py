# "client" is the fixture from conftest.py; pytest finds it by name and passes it in
def test_list_students_empty(client):
    # The test database starts empty, so we send a GET request to /students
    response = client.get("/students")
    # 200 means the request succeeded
    assert response.status_code == 200
    # No students have been added to the test database, so the list must be empty
    assert response.json() == {"students": []}

def test_add_student(client):
    # Send a POST request to /students with the new student's name as JSON
    response = client.post("/students", json={"name": "Alice"})
    # 201 means "created", which is what your add_student endpoint returns
    assert response.status_code == 201
    # Your endpoint replies with this exact message
    assert response.json() == {"message": "Added Alice"}

    # Now ask for the list of students and check Alice is in it
    list_response = client.get("/students")
    assert list_response.json() == {"students": ["Alice"]}

def test_add_duplicate_student(client):
    # Add Alice once, which should succeed
    client.post("/students", json={"name": "Alice"})
    # Add Alice a second time, which your endpoint should refuse
    response = client.post("/students", json={"name": "Alice"})
    # 409 means "conflict": the name already exists
    assert response.status_code == 409
    # Your endpoint explains the problem in the "detail" field
    assert response.json() == {"detail": "Alice already exists"}
def test_add_grade(client):
    # First add the student, because grades belong to a student
    client.post("/students", json={"name": "Alice"})
    # Add a grade of 80 for Alice
    response = client.post("/students/Alice/grades", json={"score": 80})
    # 201 means "created", which your add_grade endpoint returns
    assert response.status_code == 201

    # Fetch Alice's record and check the grade was saved
    student_response = client.get("/students/Alice")
    assert student_response.json() == {"name": "Alice", "grades": [80], "average": 80}
def test_delete_student(client):
    # Add Alice so there is someone to delete
    client.post("/students", json={"name": "Alice"})
    # Send a DELETE request to Alice's address
    response = client.delete("/students/Alice")
    # Your delete_student endpoint returns the default status, 200 (OK)
    assert response.status_code == 200
    # Your endpoint confirms with this exact message
    assert response.json() == {"message": "Deleted Alice"}

    # Ask for Alice again: she should no longer exist
    check = client.get("/students/Alice")
    # 404 means "not found", raised by your get_student_or_404 helper
    assert check.status_code == 404