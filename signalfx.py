#!/usr/bin/env python

import requests

from src.audit.integration_base import IntegrationBase

def singalfx_data():
    return {"API_URL": os.getenv("SIGNALFX_API"), "TOKEN": os.getenv("SIGNALFX_TOKEN")}

class IntegrationSignalfx(IntegrationBase):
    def __init__(self):
        super().__init__(data)
        self.api_url = data.get("API_URL")
        self.headers = {'X-SF-Token': data.get('TOKEN')}

    def get_users(self):
        limit = self.get_count(self.api_url, self.headers)
        data = requests.get(self.api_url+"/?limit="+str(limit), headers=self.headers).json()
        return [{"email": x.get("email"), "id": x.get("id")}for x in data.get("results")]

    def get_count(self, api_url, headers):
        return requests.get(api_url, headers=headers).json()['count']

    def remove_user(self, user):
        deleted = requests.delete(self.api_url+"/"+user, headers=self.headers)
        if deleted.status_code == 204:
            return True
        else:
            return False
    
    def name(slef):
        return "SignalFx"
