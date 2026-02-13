"""Tests for the GET /activities endpoint"""
import pytest


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_contains_required_fields(client):
    """Test that activities contain required fields"""
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


def test_get_activities_participants_list(client):
    """Test that participants are returned correctly"""
    response = client.get("/activities")
    data = response.json()
    
    chess_participants = data["Chess Club"]["participants"]
    assert isinstance(chess_participants, list)
    assert "michael@mergington.edu" in chess_participants
    assert "daniel@mergington.edu" in chess_participants


def test_manga_maniacs_activity_exists(client):
    """Test that Manga Maniacs activity is available"""
    response = client.get("/activities")
    data = response.json()
    
    assert "Manga Maniacs" in data
    manga = data["Manga Maniacs"]
    assert manga["description"] == "Explore the fantastic stories of the most interesting characters from Japanese Manga (graphic novels)"
    assert manga["schedule"] == "Tuesdays at 7pm"
    assert manga["max_participants"] == 15
    assert isinstance(manga["participants"], list)
