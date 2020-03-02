from django.test import Client
from rest_framework.test import APIRequestFactory
import json
from rest_framework.test import force_authenticate

class Client():
    client = Client()
    factory = APIRequestFactory()

    def post(self,url,data): 
        response = self.client.post(url,
                                json.dumps(data),
                                content_type="application/json")
        try:
            out = json.loads(response.content)
        except:
            import pdb; pdb.set_trace()
        out['status_code'] = response.status_code        
        return out
    
    def get(self,url,view,user=None): 
        request = self.factory.get(url)
        if user:
            force_authenticate(request, user=user, token=user.auth_token)

        return view(request).data