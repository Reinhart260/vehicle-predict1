# test_main.py
import unittest
from unittest.mock import patch
from main import app, predict  # Assuming your Flask app and predict function are in the same module
from numpy import array

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    @patch("main.predict")
    def test_index_endpoint_with_file(self, mock_predict):
        # Replace 'test_image.jpg' with the path to your test image
        with open('airplane76.jpg', 'rb') as test_image:
            # Mock the prediction function to return a known result
            mock_predict.return_value = array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99])

            # Assuming your endpoint is '/'
            response = self.app.post('/', data={'file': (test_image, 'airplane76.jpg')})

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the 'prediction' key
        self.assertIn(b'prediction', response.data)

        # Check if the 'predict' function is called with the expected argument
        mock_predict.assert_called_once()

    def test_index_endpoint_no_file(self):
        # Test when no file is provided
        response = self.app.post('/')
        self.assertEqual(response.status_code, 200)  # You can customize this based on your application logic
        self.assertIn(b'error', response.data)  # Check if the response contains the 'error' key

    def test_index_endpoint_invalid_file(self):
        # Test when an invalid file is provided
        response = self.app.post('/', data={'file': 'invalid_file'})
        self.assertEqual(response.status_code, 200)  # You can customize this based on your application logic
        self.assertIn(b'error', response.data)  # Check if the response contains the 'error' key

if __name__ == '__main__':
    unittest.main()
