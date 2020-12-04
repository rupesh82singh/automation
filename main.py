#!/usr/bin/env python
from src.audit.signalfx import IntegrationSignalfx
from src.audit.validate_aduser import getconnection, isuser
import os
import logging
from src.audit.sendevents import MessagePublisher

def lambda_handler( event, _):
    """Initial entry point for lambda"""

    logger = logging.getLogger()
    data = {"API_URL": os.getenv("SIGNALFX_API"), "TOKEN": os.getenv("SIGNALFX_TOKEN")}
    integrationsfx = IntegrationSignalfx(data)
    messagepub = MessagePublisher("SignalFx")
    users = integrationsfx.get_users()
    ldap = getconnection()
    dryrun = event.get('dryrun', False)

    for user in users:
        if not isuser(user.get("email"), ldap):
            if not dryrun:
                integrationsfx.remove_user(user.get('id'))
                logger.info("Invalid user found...\nEmail: "+user.get('email')+"\nSignalFx ID: "+user.get('id'))
                messagepub.publish_message(user.get('email'), user.get('id'))
            else:
                logger.info("dryrun enabled")
        else:
            logger.info("User validated successfully!...\nEmail: "+user.get('email')+"\nSignalFx ID: "+user.get('id'))

if __name__ == "__main__":
    EVENT = {'dryrun': True}
    lambda_handler(EVENT, None)
