import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # should return list of posts

def test_create_post():
    payload = {
        "title": "nirali's test post",
        "body": "This is a test for SDET API automation",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    print("\nResponse JSON:", response.json()) 
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "nirali's test post"
    assert data["body"] == "This is a test for SDET API automation"

def test_delete_post():
    response = requests.delete(f"{BASE_URL}/posts/1")
    # JSONPlaceholder always returns 200 for fake delete
    assert response.status_code == 200
