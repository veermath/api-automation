import pytest

from builder.config_builder import GetConfigTestCaseBuilder

@pytest.mark.smoke
def test_get_config_api(baseurl, web_headers):
    test_case = GetConfigTestCaseBuilder(baseurl, web_headers).build()
    test_case.make_api_call()
    test_case.validate()