"""Tests for the DELETE /activities/{activity_name}/unregister endpoint"""
import pytest


def test_unregister_existing_participant(client):
    """Test unregistering an existing participant"""
    activity = "Chess Club"
    email = "michael@mergington.edu"
    
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister removes participant from list"""
    activity = "Programming Class"
    email = "emma@mergington.edu"
    
    # Get initial count
    response = client.get("/activities")
    initial_count = len(response.json()[activity]["participants"])
    assert email in response.json()[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_response.status_code == 200
    
    # Verify count decreased and email is gone
    response = client.get("/activities")
    new_count = len(response.json()[activity]["participants"])
    assert new_count == initial_count - 1
    assert email not in response.json()[activity]["participants"]


def test_unregister_not_registered(client):
    """Test unregistering someone not registered"""
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_nonexistent_activity(client):
    """Test unregistering from a non-existent activity"""
    response = client.delete("/activities/Fake Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_then_unregister(client):
    """Test the flow of signing up and then unregistering"""
    activity = "Gym Class"
    email = "newstudent@mergington.edu"
    
    # Sign up
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    
    # Verify signed up
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    
    # Unregister
    unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_response.status_code == 200
    
    # Verify unregistered
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]
