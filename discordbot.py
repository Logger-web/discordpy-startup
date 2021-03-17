import discord
import logging
from discord.ext import commands
import os
import asyncio
import traceback
from discord import Message
from discord.enums import ChannelType
from auth import AuthService, AuthSessionState

client = commands.Bot(command_prefix='=')
token = os.environ['DISCORD_BOT_TOKEN']

@client.event
async def on_ready():
    print('------')
    print('起動しました。')
    print('------')
    print('名前')
    print(client.user.name)
    print('------')
    print('ID')
    print(client.user.id)
    print('------')

class DiscordBot(discord.Client):
	def __init__(self, auth_svc: AuthService):
		self.auth_svc = auth_svc
		super().__init__()
	#discordLogger = logging.getLogger('discord')
	#discordLogger.setLevel(logging.DEBUG)
	async def on_ready(self):
		logging.info("Logged in as {0}".format(self.user))
	async def on_message(self, message: Message):
		if message.author == self.user: return
		logging.info(message)

		if message.channel.type == ChannelType.text:
			if message.content == 'auth':
				self.auth_svc.start_session(message.author, message.guild.name)
				await message.author.send('What is your shacknews username?')
				logging.info(f'Starting auth session for {message.author}')

		elif message.channel.type == ChannelType.private:
			if self.auth_svc.get_session_state(message.author) == AuthSessionState.NEED_USERNAME:
				token = self.auth_svc.set_shack_username_get_token(message.author, message.content)
				if token:
					await message.author.send('Check your shackmessages and reply with the token.')
					logging.info(f'Generated token {token} for {message.author} with shackname {message.content}')

			elif self.auth_svc.get_session_state(message.author) == AuthSessionState.NEED_TOKEN:
				if self.auth_svc.match_token(message.author, message.content):
					await message.author.send('Successfully authenticated!')
					self.auth_svc.remove_session(message.author)
					logging.info(f'Successfully authenticated {message.author}')
				else:
					await message.author.send('Token didn\'t match please try again.')
			else:
				await message.author.send('Not sure what to do here. You don\'t have an active authentication session. Type !auth in the server you want to authenticate against.') 
@client.command()
async def rect(ctx, about = "募集", cnt = 4, settime = 10.0):
    cnt, settime = int(cnt), float(settime)
    reaction_member = [">>>"]
    test = discord.Embed(title=about,colour=0x1e90ff)
    test.add_field(name=f"あと{cnt}人 募集中\n", value=None, inline=True)
    msg = await ctx.send(embed=test)
    #投票の欄
    await msg.add_reaction('⬆️')
    await msg.add_reaction('↩️')

    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '⬆️' or emoji == '↩️'

    while len(reaction_member)-1 <= cnt:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=settime, check=check)
        except asyncio.TimeoutError:
            await ctx.send('残念、人が集まらなかったようだ...')
            break
        else:
            print(str(reaction.emoji))
            if str(reaction.emoji) == '⬆️':
                reaction_member.append(user.name)
                cnt -= 1
                test = discord.Embed(title=about,colour=0x1e90ff)
                test.add_field(name=f"あと__**{cnt}**__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                await msg.edit(embed=test)

                if cnt == 0:
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__**{cnt}**__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                    finish = discord.Embed(title=about,colour=0x1e90ff)
                    finish.add_field(name="おっと、メンバーが決まったようだな",value='\n'.join(reaction_member), inline=True)
                    await ctx.send(embed=finish)

            elif str(reaction.emoji) == '↩️':
                if user.name in reaction_member:
                    reaction_member.remove(user.name)
                    cnt += 1
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__**{cnt}**__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                else:
                    pass
                
            elif str(reaction.emoji) == '🔚':
                    test = discord.Embed(title=about,color=0x1e90ff)
                    test.add_field(name=f"募集終了")
                    await msg.edit(embed=test)
                    
        # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
        await msg.remove_reaction(str(reaction.emoji), user)
        
@client.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@client.command()
async def menu(ctx):
    await ctx.send('prefix:=\nmenu **これです。**\nhello **挨拶(?)します。**\nme **???(実行してみよう)**\nlol **???(実行してみよう)**\nrect <項目>　<人数> <時間(秒)> **募集を呼び掛けます(※開発中)**') 
    
@client.command()
async def hello(ctx):
    await ctx.send('こんばんは(　＾∀＾)')
   
@client.command()
async def baka(ctx):
    await ctx.send('自己紹介ありがとうございます(^.^)(-.-)(__)')
    
@client.command()
async def me(ctx):
    await ctx.send('君、誰だよ！')
                  
@client.command()
async def lol(ctx):
    await ctx.send('**( ・∀・)**')
                
                   
client.run(token)
