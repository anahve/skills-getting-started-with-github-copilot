"""Tests for the GET / root endpoint"""
import pytest


def test_root_redirect(client):
    """Test that root path redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_root_follow_redirect(client):
    """Test that following the redirect works"""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
