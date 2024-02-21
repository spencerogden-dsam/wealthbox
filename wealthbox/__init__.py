from json import JSONDecodeError
import requests

__version__ = '0.1.0'

class WealthBox(object):
    def __init__(self, token=None):
        self.token = token
        self.user_id = None
        self.base_url = f"https://api.crmworkspace.com/v1/"
    
    def api_request(self, endpoint, params=None):
        url = self.base_url + endpoint
        if params is None: params = {}

        params.setdefault('per_page','5000')

        res = requests.get(url,
            params = params,
            headers={'ACCESS_TOKEN':self.token})
        
        try:
            return res.json()
        except JSONDecodeError:
            return res.text

    def get_contacts(self, filters=None):
        return self.api_request('contacts',params=filters)

    def get_tasks(self, filters=None):
        return self.api_request('tasks',params=filters)

    def get_my_user_id(self):
        self.user_id = self.api_request('me')['current_user']['id']
        return self.user_id

    def get_my_tasks(self):
        if self.user_id is None:
            self.get_my_user_id()
        return self.get_tasks({'assigned_to':self.user_id})
