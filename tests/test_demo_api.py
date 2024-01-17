from main import app

def test_get_api_endpoint():
    with app.test_client() as c:
        response = c.get('api/DemoApiEndpoint')
        assert response.status_code == 200
        json_response = response.get_json()
        assert json_response == {'message': 'This is a response from a GET request.'}
print()