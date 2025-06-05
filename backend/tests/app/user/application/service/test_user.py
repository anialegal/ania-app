from unittest.mock import AsyncMock

import pytest

from modules.legal.app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from modules.legal.app.user.application.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from modules.legal.app.user.application.service.user import UserService
from modules.legal.app.user.application.command import CreateUserCommand
from modules.legal.app.user.domain.entity.user import UserRead
from modules.shared.core.helpers.token import TokenHelper
from tests.support.user_fixture import make_user


repository_mock = AsyncMock(spec=UserRepositoryAdapter)
user_service = UserService(repository=repository_mock)


@pytest.mark.asyncio
async def test_get_user_list():
    # Given
    user = UserRead(id=1, email="test@example.com", nickname="hide")
    repository_mock.get_users.return_value = [user]

    # When
    result = await user_service.get_user_list(limit=10, prev=0)

    # Then
    assert len(result) == 1
    assert result[0].id == user.id
    assert result[0].email == user.email
    assert result[0].nickname == user.nickname


@pytest.mark.asyncio
async def test_create_user_password_does_not_match():
    command = CreateUserCommand(
        email="test@example.com",
        password1="password1",
        password2="password2",
        nickname="nickname",
        lat=37.123,
        lng=-127.123,
    )

    with pytest.raises(PasswordDoesNotMatchException):
        await user_service.create_user(command)


@pytest.mark.asyncio
async def test_create_user_duplicated():
    command = CreateUserCommand(
        email="test@example.com",
        password1="password",
        password2="password",
        nickname="nickname",
        lat=37.123,
        lng=-127.123,
    )

    existing_user = make_user(
        password="password",
        email="test@example.com",
        nickname="nickname",
        is_admin=False,
        lat=37.123,
        lng=-127.123,
    )

    repository_mock.get_user_by_email_or_nickname.return_value = existing_user

    with pytest.raises(DuplicateEmailOrNicknameException):
        await user_service.create_user(command)


@pytest.mark.asyncio
async def test_create_user():
    command = CreateUserCommand(
        email="newuser@example.com",
        password1="password",
        password2="password",
        nickname="newuser",
        lat=37.123,
        lng=-127.123,
    )

    repository_mock.get_user_by_email_or_nickname.return_value = None

    await user_service.create_user(command)

    repository_mock.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_is_admin_user_not_exist():
    repository_mock.get_user_by_id.return_value = None

    result = await user_service.is_admin(user_id=1)

    assert result is False


@pytest.mark.asyncio
async def test_is_admin_user_is_not_admin():
    user = make_user(
        id=1,
        password="password",
        email="test@example.com",
        nickname="nickname",
        is_admin=False,
        lat=37.123,
        lng=-127.123,
    )

    repository_mock.get_user_by_id.return_value = user

    result = await user_service.is_admin(user_id=user.id)

    assert result is False


@pytest.mark.asyncio
async def test_is_admin():
    user = make_user(
        id=1,
        password="password",
        email="admin@example.com",
        nickname="admin",
        is_admin=True,
        lat=37.123,
        lng=-127.123,
    )

    repository_mock.get_user_by_id.return_value = user

    result = await user_service.is_admin(user_id=user.id)

    assert result is True


@pytest.mark.asyncio
async def test_login_user_not_found():
    repository_mock.get_user_by_email_and_password.return_value = None

    with pytest.raises(UserNotFoundException):
        await user_service.login(email="email", password="password")


@pytest.mark.asyncio
async def test_login():
    user = make_user(
        id=1,
        password="password",
        email="test@example.com",
        nickname="user",
        is_admin=False,
        lat=37.123,
        lng=-127.123,
    )

    repository_mock.get_user_by_email_and_password.return_value = user
    token = TokenHelper.encode(payload={"user_id": user.id})
    refresh_token = TokenHelper.encode(payload={"sub": "refresh"})

    result = await user_service.login(email="email", password="password")

    assert result.token == token
    assert result.refresh_token == refresh_token

