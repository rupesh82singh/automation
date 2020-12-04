"""Primary class for Security Audit"""

import logging
import requests


class MessagePublisher:
    """Contains logic for creating MessageBus payload for security-audit alerts"""

    def __init__(self, source):
        """Creates necessary configuration"""
        self.source = source
        self.message_bus_url = 'https://message-bus.sre.malwarebytes.com/message-bus'
        self.type = 'security-audit'
        self.logger = logging.getLogger('security_audit')

    def publish_message(self, email, id):
        """Publishes message to the Message Bus"""
        post_url = '%s?source=security-audit' % self.message_bus_url

        payload = self.generate_payload(email, id)
        resp = requests.post(url=post_url, json=payload)
        resp.raise_for_status()
        self.logger.info('Message successfully published to the Message Bus')

    def generate_payload(self, email, id):
        """Generates payload data for the Message Bus"""

        message_payload = {
            "type": self.type,
            "integration": self.source,
            "email": email,
            "id": id
        }

        return message_payload
