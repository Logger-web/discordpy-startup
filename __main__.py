import discord_bot
import logging, sys
from dependency_injector.wiring import inject, Provide
from dependency_injector import providers
from containers import Container

@inject
def main(
	config: providers.Configuration = Provide[Container.config],
	bot: discord_bot.DiscordBot = Provide[Container.discord_bot]
) -> None:
	logging.basicConfig(level=logging.INFO)
	#Supposedly you should be able to access this via dotting:
	# config.discord.api_key
	# https://python-dependency-injector.ets-labs.org/providers/configuration.html
	# but that doesn't seem to be working?
	bot.run(config['discord']['api_key'])

if __name__ == '__main__':
	container = Container()
	container.init_resources()
	container.config.from_yaml('api_key.yml', required=True)
	container.wire(modules=[sys.modules[__name__]])
	main()
