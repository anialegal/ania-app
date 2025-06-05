from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import Request

from modules.legal.app.container import Container
from modules.shared.core.fastapi.dependencies import (
    AllowAll,
    IsAdmin,
    IsAuthenticated,
    PermissionDependency,
)
from modules.shared.core.fastapi.dependencies.permission import UnauthorizedException

container = Container()


@pytest.mark.asyncio
async def test_permission_dependency_is_authenticated():
    dependency = PermissionDependency(permissions=[IsAuthenticated])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)

    with pytest.raises(UnauthorizedException):
        await dependency(request=request)


@pytest.mark.asyncio
async def test_permission_dependency_is_admin_user_is_not_admin():
    dependency = PermissionDependency(permissions=[IsAdmin])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=1)

    user_service_mock = AsyncMock()
    user_service_mock.is_admin.return_value = False

    with container.user_service.override(user_service_mock):
        with pytest.raises(UnauthorizedException):
            await dependency(request=request)


@pytest.mark.asyncio
async def test_permission_dependency_is_admin_user_id_is_none():
    dependency = PermissionDependency(permissions=[IsAdmin])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)

    user_service_mock = AsyncMock()
    user_service_mock.is_admin.return_value = False

    with container.user_service.override(user_service_mock):
        with pytest.raises(UnauthorizedException):
            await dependency(request=request)


@pytest.mark.asyncio
async def test_permission_dependency_allow_all():
    dependency = PermissionDependency(permissions=[AllowAll])
    request = AsyncMock(spec=Request)

    sut = await dependency(request=request)

    assert sut is None
