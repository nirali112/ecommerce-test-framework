import requests
import pytest
import allure

BASE_URL = "https://jsonplaceholder.typicode.com"


@allure.feature("API Testing")
@allure.story("Posts API")
class TestPostsAPI:
    
    @allure.title("Get all posts from API")
    @allure.description("Test retrieving all posts from the JSONPlaceholder API")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_posts(self):
        with allure.step("Send GET request to /posts endpoint"):
            response = requests.get(f"{BASE_URL}/posts")
            
            allure.attach(
                str(response.status_code),
                name="Response Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Verify response status is 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        with allure.step("Verify response contains list of posts"):
            data = response.json()
            assert isinstance(data, list), "Response should be a list"
            assert len(data) > 0, "Response should contain at least one post"
            
            allure.attach(
                f"Total posts: {len(data)}",
                name="Posts Count",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Attach sample of first post
            if data:
                allure.attach(
                    str(data[0]),
                    name="Sample Post",
                    attachment_type=allure.attachment_type.JSON
                )

    @allure.title("Create new post via API")
    @allure.description("Test creating a new post using POST request")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_post(self):
        payload = {
            "title": "nirali's test post",
            "body": "This is a test for SDET API automation",
            "userId": 1
        }
        
        with allure.step("Prepare request payload"):
            allure.attach(
                str(payload),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Send POST request to create new post"):
            response = requests.post(f"{BASE_URL}/posts", json=payload)
            
            allure.attach(
                str(response.status_code),
                name="Response Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Verify response status is 201 (Created)"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        with allure.step("Verify response contains correct data"):
            data = response.json()
            assert data["title"] == payload["title"], "Title mismatch"
            assert data["body"] == payload["body"], "Body mismatch"
            assert data["userId"] == payload["userId"], "UserId mismatch"
            assert "id" in data, "Response should contain post ID"

    @allure.title("Delete post via API")
    @allure.description("Test deleting a post using DELETE request")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_post(self):
        post_id = 1
        
        with allure.step(f"Send DELETE request for post ID: {post_id}"):
            response = requests.delete(f"{BASE_URL}/posts/{post_id}")
            
            allure.attach(
                str(response.status_code),
                name="Response Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Verify response status is 200"):
            # JSONPlaceholder always returns 200 for fake delete
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"