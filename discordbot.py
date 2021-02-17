from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='hi!')
token = os.environ['DISCORD_BOT_TOKEN']

@bot.command(pass_context=True)
async def ping(ctx):
    """ Pong! """
    await delete_message(ctx.message)
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def hello(ctx):
    await ctx.send('こんばんは(　＾∀＾)')
    
@bot.command()
async def me(ctx):
    await ctx.send('君、誰だよ！')
                  
@bot.command()
async def lol(ctx):
    await ctx.send('( ・∀・)')
                
                   
bot.run(token)
