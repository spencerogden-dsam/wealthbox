from json import JSONDecodeError
import requests

__version__ = '0.3.2'

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
                # The WB API usually (always?) returns a list of results under a key with the same name as the endpoint
                results.extend(res_json[endpoint.split('/')[-1]]) 
                page += 1
            except JSONDecodeError:
                return f"Error Decoding: {res.text}"

        return results
    
    def api_post(self, endpoint, data):
        url = self.base_url + endpoint
        res = requests.post(url,
                            json=data,
                            headers={'ACCESS_TOKEN': self.token})
        try:
            res_json = res.json()
        except JSONDecodeError:
            return f"Error Decoding: {res.text}"
        return res.json()
       
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

    def get_custom_fields(self,document_type=None):
        if document_type:
            params = {'document_type':document_type}
        else:
            params = None
        return self.api_request('categories/custom_fields',params=params)
    
    def update_contact(self,contact_id,updates_dict,custom_field=None):
        # Update a contact in WealthBox with a given ID and field data
        res = requests.put(self.base_url + f'contacts/{contact_id}',
                            json=updates_dict,
                            headers={'ACCESS_TOKEN': self.token})
        #TODO: Add custom field update
        return res.json()

