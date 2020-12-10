import unittest
from unittest import mock
import requests
from signalfx import IntegrationSignalfx, singalfx_data

 @mock.patch('signalfx.os.getenv', side_effect=['http://signalfx.com', 'abc'])
    def test_signalfxdata(self):
      data = singalfx_data()
      self.assertEqual('http://signalfx.com', data.get("API_URL"))
      self.assertEqual('abc', data.get("TOKEN"))
      
class MockResponse:
  """mock the response"""
  def __init__(self, status_code):
    self.status_code = status_code


class TestIntegrationSignalfx(unittest.TestCase):
    """this is a test case for integrationsignalfx"""

    def setUp(self):
      self.signalfxsource = IntegrationSignalfx({"API_URL": "https://signalfx.com", "TOKEN": "abcdef"})
    
    @mock.patch('sendevents.requests.get', side_effect=[{'count':0}, {'results' : []])
    def test_get_users_not_empty(self):
      users = self.signalfxsource.get_users('https://signalfx.com', [])
      self.assertEqual(0, length(users))
                                                                      
    @mock.patch('sendevents.requests.get', side_effect=[{'count':0}, {'results' : [{"email": "abc@def", "id": 'abc'}]])
    def test_get_users_not_empty(self):
      users = self.signalfxsource.get_users('https://signalfx.com', [])
      self.assertEqual(1, length(users))
      self.assertEqual('abc@def', users[0].get("email"))
      self.assertEqual('abc', users[0].get("id")) 
    
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
