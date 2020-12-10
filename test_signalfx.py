import unittest
from unittest import mock
import requests
from signalfx import IntegrationSignalfx

class MockResponse:
  """mock the response"""
  def __init__(self, status_code):
    self.status_code = status_code


class TestIntegrationSignalfx(unittest.TestCase):
    """this is a test case for integrationsignalfx"""

    def setUp(self):
      self.signalfxsource = IntegrationSignalfx({"API_URL": "https://signalfx.com", "TOKEN": "abcdef"})
    
    @mock.patch('sendevents.requests.delete', side_effect=MockResponse(204))
    def test_remove_user_success(self):
      delete_result = self.signalfxsource.remove_user('abc')
      self.assertEqual(204, delete_result)
    
    @mock.patch('sendevents.requests.delete', side_effect=MockResponse(500))
    def test_remove_user_Fail(self):
      delete_result = self.signalfxsource.remove_user('abc')
      self.assertEqual(500, delete_result) 
      
    def test_integration_name(self):
      integration_name = self.signalfxsource.name()
      self.assertEqual('SignalFx', integration_name)
