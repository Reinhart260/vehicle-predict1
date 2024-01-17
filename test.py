import unittest
import requests

from main import app

class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000"

    data = {
        "name": "Testing",
        "description": "Testing post functionality"
        }

    expected_result = '<Response [200]>'

    update_data = {
        "name": "Updated",
        "description": "Updated post functionality",
        "completed": True
    }

    def test_1_get_all_todos(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.__str__()), 16)
        print("Test 1 completed")

    def test_2_post_todo(self):
        resp = requests.post(self.URL, json=self.data)
        self.assertEqual(resp.status_code, 200)
        print("Test 2 completed")

    def test_3_get_specific_todo(self):
        resp = requests.get(self.URL + '/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.__str__(), self.expected_result)
        print("Test 3 completed")

    def test_4_delete(self):
        resp = requests.delete(self.URL)
        self.assertEqual(resp.status_code, 200)
        print("Test 4 completed")

    def test_5_update(self):
        resp = requests.put(self.URL, json=self.update_data)
        self.assertEqual(resp.__str__(),'name', self.update_data)
        self.assertEqual(resp.__str__()['description'], self.update_data['description'])
        self.assertEqual(resp.__str__()['completed'], self.update_data['completed'])
        print("Test 5 completed")

if __name__ == "__main__":
    tester = TestAPI()

    tester.test_1_get_all_todos()
    tester.test_2_post_todo()
    tester.test_3_get_specific_todo()
    # tester.test_4_delete()
    # tester.test_5_update()