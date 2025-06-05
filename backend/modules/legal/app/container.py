from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from modules.legal.app.auth.application.service.jwt import JwtService
from modules.legal.app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from modules.legal.app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from modules.legal.app.user.application.service.user import UserService


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["modules.legal.app"])

    user_repo = Singleton(UserSQLAlchemyRepo)
    user_repo_adapter = Factory(UserRepositoryAdapter, user_repo=user_repo)
    user_service = Factory(UserService, repository=user_repo_adapter)

    jwt_service = Factory(JwtService)

