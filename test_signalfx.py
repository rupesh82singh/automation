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
    
    @mock.patch('sendevents.requests.get', side_effect={'count':0})
    def test_get_count_zero(self):
      count_result = self.signalfxsource.get_count('https://signalfx.com', [])
      self.assertEqual(0, count_result)  
      
    @mock.patch('sendevents.requests.get', side_effect={'count':1})
    def test_get_count_postive_value(self):
      count_result = self.signalfxsource.get_count('https://signalfx.com', [])
      self.assertEqual(1, count_result)   
      
    @mock.patch('sendevents.requests.delete', side_effect=MockResponse(204))
    def test_remove_user_success(self):
      delete_result = self.signalfxsource.remove_user('abc')
      self.assertEqual(True, delete_result)
    
    @mock.patch('sendevents.requests.delete', side_effect=MockResponse(500))
    def test_remove_user_fail(self):
      delete_result = self.signalfxsource.remove_user('abc')
      self.assertEqual(False, delete_result) 
      
    def test_integration_name(self):
      integration_name = self.signalfxsource.name()
      self.assertEqual('SignalFx', integration_name)
