"""Unit test for lambdahandler"""


import unittest
from unittest import mock
from unittest.mock import MagicMock
from main import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    """test case for lambdahandler"""

    @mock.patch('main.MessagePublisher')
    @mock.patch('main.IntegrationSignalfx')
    @mock.patch('main.getconnection')
    @mock.patch('main.isuser')
    def test_empty_sources(self, mock_is_user, mock_ldap, mock_source, mock_msg_publisher):
      main.sources = []
      isUser = MagicMock()
      ldap = MagicMock()
      source = MagicMock()
      msg_publisher = MagicMock()
      mock_is_user.return_value = isUser
      mock_ldap.return_value = ldap
      mock_source.return_value = source
      mock_msg_publisher.return_value = msg_publisher
      event = {'dryrun': False}
      lambda_handler(event, None)
      mock_is_user.assert_not_called()
      mock_ldap.assert_called_once()
      mock_source.assert_not_called()
      mock_msg_publisher.assert_not_called()
    
    @mock.patch('main.MessagePublisher')
    @mock.patch('main.IntegrationSignalfx')
    @mock.patch('main.getconnection')
    @mock.patch('main.isuser')
    def test_empty_user_from_sources(self, mock_is_user, mock_ldap, mock_source, mock_msg_publisher):
      isUser = MagicMock()
      ldap = MagicMock()
      source = MagicMock()
      msg_publisher = MagicMock()
      main.sources = [source]
      mock_is_user.return_value = isUser
      mock_ldap.return_value = ldap
      mock_source.return_value = source
      mock_msg_publisher.return_value = msg_publisher
      source.get_users.return_value = []
      event = {'dryrun': False}
      lambda_handler(event, None)
      mock_is_user.assert_not_called()
      mock_ldap.assert_called_once()
      mock_source.assert_not_called()
      mock_msg_publisher.assert_not_called()
      source.get_users.assert_called_once()
 
    @mock.patch('main.MessagePublisher')
    @mock.patch('main.IntegrationSignalfx')
    @mock.patch('main.getconnection')
    @mock.patch('main.isuser')
    def test_user_valid(self, mock_is_user, mock_ldap, mock_source, mock_msg_publisher):
      isUser = MagicMock()
      ldap = MagicMock()
      source = MagicMock()
      msg_publisher = MagicMock()
      main.sources = [source]
      mock_is_user.return_value = isUser
      mock_ldap.return_value = ldap
      mock_source.return_value = source
      mock_msg_publisher.return_value = msg_publisher
      source.get_users.return_value = [{'email': 'abc@xyz.com', 'id': "abj148djh"}]
      isUser.return_value = True
      event = {'dryrun': False}
      lambda_handler(event, None)
      mock_is_user.assert_not_called()
      mock_ldap.assert_called_once()
      mock_source.assert_not_called()
      mock_msg_publisher.assert_not_called()
      source.get_users.assert_called_once()
      msg_publisher.publish_message.assert_not_called()
      source.remove_user.assert_not_called()
      
    @mock.patch('main.MessagePublisher')
    @mock.patch('main.IntegrationSignalfx')
    @mock.patch('main.getconnection')
    @mock.patch('main.isuser')
    def test_user_invalid_with_dryrun_enabled(self, mock_is_user, mock_ldap, mock_source, mock_msg_publisher):
      isUser = MagicMock()
      ldap = MagicMock()
      source = MagicMock()
      msg_publisher = MagicMock()
      main.sources = [source]
      mock_is_user.return_value = isUser
      mock_ldap.return_value = ldap
      mock_source.return_value = source
      mock_msg_publisher.return_value = msg_publisher
      source.get_users.return_value = [{'email': 'abc@xyz.com', 'id': "abj148djh"}]
      isUser.return_value = FALSE
      event = {'dryrun': True}
      lambda_handler(event, None)
      mock_is_user.assert_not_called()
      mock_ldap.assert_called_once()
      mock_source.assert_not_called()
      mock_msg_publisher.assert_not_called()
      source.get_users.assert_called_once()
      msg_publisher.publish_message.assert_not_called()
      source.remove_user.assert_not_called()
        
      @mock.patch('main.MessagePublisher')
    @mock.patch('main.IntegrationSignalfx')
    @mock.patch('main.getconnection')
    @mock.patch('main.isuser')
    def test_user_invalid_with_dryrun_disabled(self, mock_is_user, mock_ldap, mock_source, mock_msg_publisher):
      isUser = MagicMock()
      ldap = MagicMock()
      source = MagicMock()
      msg_publisher = MagicMock()
      main.sources = [source]
      mock_is_user.return_value = isUser
      mock_ldap.return_value = ldap
      mock_source.return_value = source
      mock_msg_publisher.return_value = msg_publisher
      source.get_users.return_value = [{'email': 'abc@xyz.com', 'id': "abj148djh"}]
      isUser.return_value = FALSE
      event = {'dryrun': False}
      lambda_handler(event, None)
      mock_is_user.assert_not_called()
      mock_ldap.assert_called_once()
      mock_source.assert_not_called()
      mock_msg_publisher.assert_not_called()
      source.get_users.assert_called_once()
      msg_publisher.publish_message.assert_called_once()
      source.remove_user.assert_called_once()  
