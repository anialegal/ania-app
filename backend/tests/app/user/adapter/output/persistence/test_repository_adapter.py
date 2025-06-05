from unittest.mock import AsyncMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from modules.legal.app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from modules.legal.app.user.domain.repository.user import UserRepo
from tests.support.user_fixture import make_user

user_repo_mock = AsyncMock(spec=UserRepo)
repository_adapter = UserRepositoryAdapter(user_repo=user_repo_mock)

@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )

    user_repo_mock.get_users.return_value = [user]

    result = await repository_adapter.get_users(limit=1, prev=1)

    assert len(result) == 1
    assert result[0].id == user.id

    user_repo_mock.get_users.assert_awaited_once_with(limit=1, prev=1)

@pytest.mark.asyncio
async def test_get_user_by_email_or_nickname(session: AsyncSession):
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )

    user_repo_mock.get_user_by_email_or_nickname.return_value = user

    result = await repository_adapter.get_user_by_email_or_nickname(
        email=user.email, nickname=user.nickname
    )

    assert result.id == user.id

    user_repo_mock.get_user_by_email_or_nickname.assert_awaited_once_with(
        email=user.email, nickname=user.nickname
    )

@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )

    user_repo_mock.get_user_by_id.return_value = user

    result = await repository_adapter.get_user_by_id(user_id=user.id)

    assert result.id == user.id

    user_repo_mock.get_user_by_id.assert_awaited_once_with(user_id=user.id)

@pytest.mark.asyncio
async def test_get_user_by_email_and_password(session: AsyncSession):
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )

    user_repo_mock.get_user_by_email_and_password.return_value = user

    result = await repository_adapter.get_user_by_email_and_password(
        email=user.email, password=user.password
    )

    assert result.id == user.id

    user_repo_mock.get_user_by_email_and_password.assert_awaited_once_with(
        email=user.email, password=user.password
    )

@pytest.mark.asyncio
async def test_save_user(session: AsyncSession):
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )

    await repository_adapter.save(user=user)

    user_repo_mock.save.assert_awaited_once_with(user=user)

