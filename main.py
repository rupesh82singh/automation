#!/usr/bin/env python
from src.audit.signalfx import IntegrationSignalfx
from src.audit.validate_aduser import getconnection, isuser
import os
import logging
from src.audit.sendevents import MessagePublisher

def lambda_handler( event, _):
    """Initial entry point for lambda"""

    logger = logging.getLogger()
    dryrun = event.get('dryrun', False)
    sources = [IntegrationSignalfx()]
    
    for source in sources:
        messagepub = MessagePublisher(source.name())
        users = source.get_users()
        ldap = getconnection()

        for user in users:
            if not isuser(user.get("email"), ldap):
                if not dryrun:
                    source.remove_user(user.get('id'))
                    logger.info("Invalid user found...\nEmail: "+user.get('email')+"\nSignalFx ID: "+user.get('id'))
                    messagepub.publish_message(user.get('email'), user.get('id'))
                else:
                    logger.info("dryrun enabled")
            else:
                logger.info("User validated successfully!...\nEmail: "+user.get('email')+"\nSignalFx ID: "+user.get('id'))

if __name__ == "__main__":
    EVENT = {'dryrun': True}
    lambda_handler(EVENT, None)
