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
        page = 1
        total_pages = 9999999999
        if params is None:
            params = {}
        
        params.setdefault('per_page', '5000')
        results = []

        while page <= total_pages:
            params['page'] = page
            res = requests.get(url,
                            params=params,
                            headers={'ACCESS_TOKEN': self.token})
            try:
                res_json = res.json()
                total_pages = res_json['meta']['total_pages']
                results.extend(res_json[endpoint])
                page += 1
            except:# JSONDecodeError:
                print(res.text)
                return results

        return results
       
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
