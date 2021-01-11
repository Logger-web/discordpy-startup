from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='s/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def hello(ctx):
    await ctx.send('こんばんは(　＾∀＾)')
    
@bot.command()
async def menu(ctx):
    await ctx.send('s/menu **ヘルプメニューを表示します。\ns/hello **挨拶をします')
                  
@bot.command()
async def lol(ctx):
    await ctx.send('( ・∀・)')
                
                   
bot.run(token)
