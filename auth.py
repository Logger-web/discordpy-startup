import datetime
import uuid
from enum import Enum

from discord.abc import User
from discord.guild import Guild

class AuthSessionState(Enum):
	NONE = 1,
	NEED_USERNAME = 2,
	NEED_TOKEN = 3

class AuthSession():
	def __init__(self, discord_username: User, discord_guild: Guild, state: AuthSessionState = AuthSessionState.NEED_USERNAME) -> None:
		self.discord_user = discord_username
		self.discord_guild = discord_guild
		self.state = state

	discord_user: User
	discord_guild: Guild
	shack_name: str
	auth_token: str
	expire_time: datetime
	state: AuthSessionState = AuthSessionState.NEED_USERNAME

class AuthService:
	sessions = dict()

	def get_session_state(self, discord_user: User) -> AuthSessionState:
		session = self.sessions.get(discord_user)
		if session:
			return session.state
		return AuthSessionState.NONE

	def set_shack_username_get_token(self, discord_user: User, shack_username: str) -> str:
		session : AuthSession = self.sessions[discord_user]
		if session:
			session.shack_name = shack_username
			session.auth_token = str(uuid.uuid4()).upper()[:6]
			session.state = AuthSessionState.NEED_TOKEN
			self.sessions[discord_user] = session
			return session.auth_token

	def start_session(self, discord_user: User, discord_guild: Guild):
		self.sessions[discord_user] = AuthSession(discord_user, discord_guild)
	
	def match_token(self, discord_user: User, token: str) -> bool:
		if (discord_user in self.sessions == False):
			return False
		
		session : AuthSession = self.sessions.get(discord_user)
		return session.auth_token == token.strip()

	def remove_session(self, discord_user: User):
		self.sessions.pop(discord_user)
