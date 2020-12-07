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
    @mock.patch('main.isUser')
    def test_empty_sources(self, mock_is_user, mock_ldap, mock_source, mock_msg_publisher):
      main.sources = []
      isUser = MagicMock()
      ldap = MagicMock()
      sources = MagicMock()
      msg_publisher = MagicMock()
      mock_is_user.return_value = isUser
      mock_ldap.return_value = ldap
      mock_source.return_value = sources
      mock_msg_publisher.return_value = msg_publisher
      event = {'dryrun': False}
      lambda_handler(event, None)
      mock_is_user.assert_not_called()
      mock_ldap.assert_not_called()
      mock_source.assert_not_called()
      mock_msg_publisher.assert_not_called()
