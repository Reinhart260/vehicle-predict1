from main import app


def test_home_route():
    response = app.test_client().get('/')
    print()
    assert response.status_code == 200
    assert b'OK' in response.data


test_home_route()
