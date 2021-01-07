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
async def help(ctx):
embed=discord.Embed(title="へるぷ▪めにゅー", description="s/hello", color=0x260ccf)
embed.add_field(name="BOT運営", value="SUN#0796", inline=True)
embed.set_footer(text="Smart Human ")
await ctx.send(embed=embed)


bot.run(token)
