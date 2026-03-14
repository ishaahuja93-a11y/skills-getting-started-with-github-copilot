"""Tests for the activities API endpoints using AAA pattern."""


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_success(self, client):
        # Arrange: No special setup needed as activities are predefined

        # Act: Make GET request to /activities
        response = client.get("/activities")

        # Assert: Check response status and structure
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "description" in data["Chess Club"]
        assert "participants" in data["Chess Club"]


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        # Arrange: Choose an activity and a new email
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"

        # Act: Make POST request to signup
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert: Check success response
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert f"Signed up {email} for {activity_name}" == result["message"]

        # Verify the participant was added
        response_get = client.get("/activities")
        assert email in response_get.json()[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        # Arrange: Use a non-existent activity
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"

        # Act: Attempt to signup
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert: Check 404 response
        assert response.status_code == 404
        result = response.json()
        assert result["detail"] == "Activity not found"

    def test_signup_duplicate_participant(self, client):
        # Arrange: Signup a student first
        activity_name = "Gym Class"
        email = "duplicate@mergington.edu"
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Act: Try to signup the same student again
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert: Check 400 response for duplicate
        assert response.status_code == 400
        result = response.json()
        assert result["detail"] == "Student is already signed up for this activity"


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_success(self, client):
        # Arrange: First signup a student
        activity_name = "Chess Club"
        email = "removeme@mergington.edu"
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Act: Unregister the student
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert: Check success response
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert f"Unregistered {email} from {activity_name}" == result["message"]

        # Verify the participant was removed
        response_get = client.get("/activities")
        assert email not in response_get.json()[activity_name]["participants"]

    def test_unregister_activity_not_found(self, client):
        # Arrange: Use a non-existent activity
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"

        # Act: Attempt to unregister
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert: Check 404 response
        assert response.status_code == 404
        result = response.json()
        assert result["detail"] == "Activity not found"

    def test_unregister_not_signed_up(self, client):
        # Arrange: Use an email not signed up
        activity_name = "Programming Class"
        email = "notsigned@mergington.edu"

        # Act: Attempt to unregister
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")

        # Assert: Check 400 response
        assert response.status_code == 400
        result = response.json()
        assert result["detail"] == "Student not signed up for this activity"