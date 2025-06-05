import pytest
from modules.legal.app.auth.application.service.jwt import JwtService, DecodeTokenException
from tests.support.token import INVALID_REFRESH_TOKEN, USER_ID_1_TOKEN

@pytest.fixture
def jwt_service():
    return JwtService()

@pytest.mark.asyncio
async def test_verify_token(jwt_service):
    with pytest.raises(DecodeTokenException):
        await jwt_service.verify_token(token="abc")

@pytest.mark.asyncio
async def test_create_refresh_token_invalid_refresh_token(jwt_service):
    token = INVALID_REFRESH_TOKEN
    with pytest.raises(DecodeTokenException):
        await jwt_service.create_refresh_token(token=token, refresh_token=token)

@pytest.mark.asyncio
async def test_create_refresh_token(jwt_service):
    token = USER_ID_1_TOKEN
    sut = await jwt_service.create_refresh_token(token=token, refresh_token=token)
    assert sut.token is not None
    assert sut.refresh_token is not None

