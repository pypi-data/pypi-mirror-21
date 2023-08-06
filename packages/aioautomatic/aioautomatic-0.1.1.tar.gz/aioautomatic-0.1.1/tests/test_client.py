"""Tests for automatic client."""
from aioautomatic.client import Client

from tests.common import AsyncMock


def test_create_client(aiohttp_session):
    """Create a client object."""
    client_id = 'mock_id'
    client_secret = 'mock_secret'
    client = Client(client_id, client_secret, aiohttp_session)
    assert client.client_id == client_id
    assert client.client_secret == client_secret


def test_create_session_from_password(client):
    """Test opening a session from the users password."""
    resp = AsyncMock()
    resp.status = 200
    resp.json.return_value = {
        "access_token": "mock_access",
        "expires_in": 123456,
        "scope": ("scope:location scope:vehicle:profile "
                  "scope:user:profile scope:trip"),
        "refresh_token": "mock_refresh",
        "token_type": "Bearer",
    }
    client._client_session.request.return_value = resp

    client.loop.run_until_complete(
        client.create_session_from_password("mock_user", "mock_pass"))
    assert client._client_session.request.called
    assert len(client._client_session.request.mock_calls) == 2
    assert client._client_session.request.mock_calls[0][1][0] == "POST"
    assert client._client_session.request.mock_calls[0][1][1] == \
        "https://accounts.automatic.com/oauth/access_token"
    assert client._client_session.request.mock_calls[0][2]['data'] == {
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "grant_type": "password",
        "username": "mock_user",
        "password": "mock_pass",
        "scope": ("scope:location scope:vehicle:profile "
                  "scope:user:profile scope:trip scope:current_location"),
    }


def test_scope_forbidden(client):
    """Test opening a session from the users password."""
    resp = AsyncMock()
    resp.status = 200
    resp.json.return_value = {
        "access_token": "mock_access",
        "expires_in": 123456,
        "scope": ("scope:location scope:vehicle:profile "
                  "scope:user:profile scope:trip"),
        "refresh_token": "mock_refresh",
        "token_type": "Bearer",
    }

    def get_resp(method, url, data, **kwargs):
        if "scope:current_location" in data["scope"]:
            resp.status = 403
        else:
            resp.status = 200
        return resp

    client._client_session.request.side_effect = get_resp

    client.loop.run_until_complete(
        client.create_session_from_password("mock_user", "mock_pass"))
    assert client._client_session.request.called
    assert len(client._client_session.request.mock_calls) == 2
    assert client._client_session.request.mock_calls[0][1][0] == "POST"
    assert client._client_session.request.mock_calls[0][1][1] == \
        "https://accounts.automatic.com/oauth/access_token"
    assert client._client_session.request.mock_calls[0][2]['data'] == {
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "grant_type": "password",
        "username": "mock_user",
        "password": "mock_pass",
        "scope": ("scope:location scope:vehicle:profile "
                  "scope:user:profile scope:trip"),
    }
