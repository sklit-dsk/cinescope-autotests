import pytest
import requests
def test_register_timeout(api_manager, test_user):
    with pytest.raises(requests.exceptions.ConnectTimeout):
        api_manager.auth_api.register_user(test_user, timeout=0.001)