"""Unit test for Iam Key Publisher"""

import unittest
from unittest import mock
import requests
from sendevents import MessagePublisher

def mocked_request_post(_, __):
    """mocking the request post"""
    class MockResponse:
        """mock the response"""
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            """mock the json"""
            return self.json_data

        def raise_for_status(self):
            """raise for status returns none"""
            return None

    return MockResponse({'status': 'OK'}, 200)

class TestMessagePublisher(unittest.TestCase):
    """this is a test case for messagepublisher"""

    def setUp(self):
        self.message_publisher = MessagePublisher('signalfx')

    def test_generate_payload(self):
        """test the generate payload function"""
        payload = self.message_publisher.generate_payload('abc@def.com', 'US123', 'signalfx')
        self.assertEqual('security-audit', payload['type'])
        self.assertEqual('signalfx', payload['integration'])
        self.assertEqual('abc@def.com', payload['email'])
        self.assertEqual('US123', payload['id'])
        
    @mock.patch('sendevents.requests.post', side_effect=requests.exceptions.ConnectionError())
    def test_publish_message_fails(self, _):
        """test the publish message fail fucntion"""
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.message_publisher.publish_message('abc@def.com', 'US123', 'signalfx')


    @mock.patch('sendevents.requests.post', side_effect=mocked_request_post)
    def test_publish_message_success(self, _):
        """testing the publish message is success"""
        self.message_publisher.publish_message('abc@def.com', 'US123', 'signalfx')


if __name__ == '__main__':
    unittest.main()
