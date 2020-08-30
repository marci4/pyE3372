import pytest

from modem_wrapper import ModemConnector


@pytest.fixture(scope="module")
def mc():
    return ModemConnector()


def test_set_session_vars(mc):
    mc.set_session_vars()
    assert type(mc._session) == str
    assert type(mc._token) == str


def test_sms_list(mc):
    assert type(mc.get_sms_list(5)) == list

