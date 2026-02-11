"""Tests for the POST /activities/{activity_name}/signup endpoint"""
import pytest


def test_signup_new_participant(client):
    """Test signing up a new participant for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=newemail@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newemail@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_updates_participants_list(client):
    """Test that signup updates the participants list"""
    email = "test@mergington.edu"
    activity = "Programming Class"
    
    # Get initial count
    response = client.get("/activities")
    initial_count = len(response.json()[activity]["participants"])
    
    # Sign up
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    
    # Verify count increased
    response = client.get("/activities")
    new_count = len(response.json()[activity]["participants"])
    assert new_count == initial_count + 1
    assert email in response.json()[activity]["participants"]


def test_signup_duplicate_participant(client):
    """Test that duplicate signups are rejected"""
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/Nonexistent Club/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_activity_full(client):
    """Test signing up for a full activity"""
    activity = "Tennis Team"
    
    # Get current participants and max
    response = client.get("/activities")
    tennis_activity = response.json()[activity]
    current_participants = len(tennis_activity["participants"])
    max_participants = tennis_activity["max_participants"]
    
    # If already full, add more dummy participants to fill it
    if current_participants < max_participants:
        for i in range(current_participants, max_participants):
            email = f"filler{i}@mergington.edu"
            client.post(f"/activities/{activity}/signup?email={email}")
    
    # Try to sign up to a full activity
    response = client.post(f"/activities/{activity}/signup?email=overcapacity@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "full" in data["detail"].lower()
