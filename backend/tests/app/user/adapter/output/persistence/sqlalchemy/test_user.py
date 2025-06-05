import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from modules.legal.app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from modules.legal.app.user.domain.entity.user import User
from tests.support.user_fixture import make_user

user_repo = UserSQLAlchemyRepo()


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    user_1 = make_user(
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )

    user_2 = make_user(
        password="password2",
        email="b@b.c",
        nickname="test",
        is_admin=False,
        lat=37.123,
        lng=127.123,
    )

    session.add_all([user_1, user_2])
    await session.commit()

    # When
    sut = await user_repo.get_users(limit=15, prev=12)

    # Then
    assert len(sut) == 2
    assert sut[0].email == user_1.email
    assert sut[1].email == user_2.email


@pytest.mark.asyncio
async def test_get_user_by_email_or_nickname(session: AsyncSession):
    # Given
    email = "a@b.c"
    nickname = "hide"
    user = make_user(
        password="password2",
        email=email,
        nickname=nickname,
        is_admin=False,
        lat=37.123,
        lng=127.123,
    )

    session.add(user)
    await session.commit()

    # When
    sut = await user_repo.get_user_by_email_or_nickname(email=email, nickname=nickname)

    # Then
    assert sut.email == email
    assert sut.nickname == nickname


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    # Given
    user = make_user(
        password="password",
        email="c@d.e",
        nickname="testuser",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )

    session.add(user)
    await session.commit()

    # When
    sut = await user_repo.get_user_by_id(user_id=user.id)

    # Then
    assert sut.id == user.id


@pytest.mark.asyncio
async def test_get_user_by_email_and_password(session: AsyncSession):
    # Given
    email = "b@c.d"
    password = "hide"
    user = make_user(
        password=password,
        email=email,
        nickname="hide",
        is_admin=False,
        lat=37.123,
        lng=127.123,
    )

    session.add(user)
    await session.commit()

    # When
    sut = await user_repo.get_user_by_email_and_password(email=email, password=password)

    # Then
    assert sut.email == email
    assert sut.password == password


@pytest.mark.asyncio
async def test_save(session: AsyncSession):
    # Given
    user = make_user(
        password="savepassword",
        email="save@user.com",
        nickname="save",
        is_admin=False,
        lat=37.123,
        lng=127.123,
    )

    # When
    await user_repo.save(user=user)

    # Then
    saved_user = await user_repo.get_user_by_email_or_nickname(email=user.email, nickname=user.nickname)
    assert saved_user is not None
    assert saved_user.email == user.email
    assert saved_user.nickname == user.nickname

