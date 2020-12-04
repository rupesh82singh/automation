"""Base class for jira integrations"""

from abc import ABC, abstractmethod


class IntegrationBase(ABC):
    """Base class for jira integrations"""

    def __init__(self, data):
        self._data = data
        super().__init__()

    @abstractmethod
    def get_users(self):
        """function to get users"""

    @abstractmethod
    def remove_user(self, user):
        """function to remove users"""
