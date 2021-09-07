import requests
from os.path import join
from jsonschema import validate, RefResolver
import json
import pathlib


class APIRequest:
    def __init__(self):
        self._payload = None
        self._headers = None
        self._method_type = None
        self._endpoint = None
        self._base_url = None

    def set_payload(self, payload):
        self._payload = payload

    def set_headers(self, headers):
        self._headers = headers

    def set_endpoint(self, endpoint):
        self._endpoint = endpoint

    def set_base_url(self, base_url):
        self._base_url = base_url

    def set_method_type(self, method_type):
        self._method_type = method_type

    def execute_request(self):
        response = ""
        if self._method_type.casefold() == 'get':
            response = requests.get(self._base_url + self._endpoint, params=self._payload, headers=self._headers)

        elif self._method_type.casefold() == 'post':
            response = requests.post(self._base_url + self._endpoint, params=self._payload, headers=self._headers)

        elif self._method_type.casefold() == 'put':
            response = requests.put(self._base_url + self._endpoint, params=self._payload, headers=self._headers)

        return response


class APITestCase:
    def __init__(self):
        self._request_obj = None
        self._response_validator = None
        self._response_obj = None

    def set_request_object(self, request_obj):
        self._request_obj = request_obj

    def set_response_validator(self, response_validator):
        self._response_validator = response_validator

    def make_api_call(self):
        self._response_obj = self._request_obj.execute_request()
        return self._response_obj

    def validate(self):
        return self._response_validator.validate(self._response_obj)

class APIResponseValidator:
    def __init__(self, schema_file_name, custom_validator=None, expected_response_code=200):
        self._schema_file_name = schema_file_name
        self._custom_validator = custom_validator
        self._expected_response_code = expected_response_code

    def validate(self, response_obj):
        assert response_obj.status_code == self._expected_response_code, "GET call failed. Status Code {}".format(response_obj.status_code)
        schema_file = self._load_json_schema()
        resolver = RefResolver("file://{0}".format(join(pathlib.Path(__file__).parent.parent, 'schemas/')), None)
        validate(response_obj.json(), schema_file, resolver=resolver)
        if self._custom_validator is not None:
            self._custom_validator(response_obj)

    def _load_json_schema(self):
        relative_path_file = join('schemas', self._schema_file_name)
        absolute_path_file = join(pathlib.Path(__file__).parent.parent, relative_path_file)

        with open(absolute_path_file) as schema_file:
            return json.loads(schema_file.read())

