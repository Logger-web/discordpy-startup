from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='hi!')
token = os.environ['DISCORD_BOT_TOKEN']

@client.command()
async def tempmute(ctx, member: discord.Member, time: int, d, *, reason=None):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)

            embed = discord.Embed(title="muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
            embed.add_field(name="reason:", value=reason, inline=False)
            embed.add_field(name="time left for the mute:", value=f"{time}{d}", inline=False)
            await ctx.send(embed=embed)

            if d == "s":
                await asyncio.sleep(time)

            if d == "m":
                await asyncio.sleep(time*60)

            if d == "h":
                await asyncio.sleep(time*60*60)

            if d == "d":
                await asyncio.sleep(time*60*60*24)

            await member.remove_roles(role)

            embed = discord.Embed(title="unmute (temp) ", description=f"unmuted -{member.mention} ", colour=discord.Colour.light_gray())
            await ctx.send(embed=embed)

            return



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
