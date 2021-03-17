from dependency_injector import containers, providers
from auth import AuthService
from discord_bot import DiscordBot

class Container(containers.DeclarativeContainer):
	config = providers.Configuration()

	auth_service = providers.Singleton(AuthService)
	discord_bot = providers.Singleton(
		DiscordBot,
		auth_svc=auth_service
	)
