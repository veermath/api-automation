import api_config
from processor.request_processor import APIRequest, APITestCase, APIResponseValidator
from test_data import agents

class GetConfigTestCaseBuilder():
    def __init__(self, base_url, headers):
        self._base_url = base_url
        self._headers = headers

    def build(self):
        payload = {
            "userid": agents.admins [0][0],
            "deviceid": agents.admins [0][1]
        }
        request_obj = APIRequest()
        request_obj.set_endpoint(api_config.ADMIN_CONFIG)
        request_obj.set_headers(self._headers)
        request_obj.set_payload(payload)
        request_obj.set_base_url(self._base_url)
        request_obj.set_method_type("get")
        response_validator = APIResponseValidator("get_admin_config.json")
        test_case = APITestCase()
        test_case.set_response_validator(response_validator)
        test_case.set_request_object(request_obj)
        return test_case

def custom_validator(response_obj):
    pass