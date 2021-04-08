import discord
from discord.ext import commands
import os
import asyncio
import traceback
import logging

bot = commands.Bot(command_prefix='=')
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print('------')
    print('起動しました。')
    print('------')
    print('名前')
    print(bot.user.name)
    print('------')
    print('ID')
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="開発中(エラー起きてるんゴーw)"))
 
@bot.event
async def on_voice_channel_join(member, channel):
    await discord.utils.get(member.guild.text_channels, name="vc-log").send(f"{member.mention} が {channel.name}　に接続しました。")


@bot.event
async def on_voice_channel_leave(member, channel):
    await discord.utils.get(member.guild.text_channels, name="vc-log").send(f"{member.mention} が {channel.name}　から切断しました。")

@bot.event
async def on_voice_channel_move(member, before, after):
    await discord.utils.get(member.guild.text_channels, name="vc-log").send(f"{member.mention} が {after.name} から　{before.name}　に移動しました。"
                                                 
@bot.event
async def on_member_join(member):
    await message.channel.send(f"{message.author.display_name}さん、||ピザは持ってきたかね?||\nようこそ\n楽しんでいってね\n勿論ですが、ピザのは冗談です")
                                                                            
                       
    

@bot.command()
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
            reaction, user = await bot.wait_for('reaction_add', timeout=settime, check=check)
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
        
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def menu(ctx):
    await ctx.send('prefix:=\nmenu **これです。**\nhello **挨拶(?)します。**\nme **???(実行してみよう)**\nlol **???(実行してみよう)**\nrect <項目>　<人数> <時間(秒)> **募集を呼び掛けます(※開発中)**') 
    
@bot.command()
async def hello(ctx):
    await ctx.send('こんばんは(　＾∀＾)')
   
@bot.command()
async def baka(ctx):
    await ctx.reply('自己紹介ありがとうございます(^.^)(-.-)(__)')
    
@bot.command()
async def me(ctx):
    await ctx.send('君、誰だよ！')
                  
@bot.command()
async def lol(ctx):
    await ctx.send('**( ・∀・)**')
    
@bot.command()
@commands.is_owner()
async def offline(ctx):
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game('開発中(エラー起きてるんゴーw)'))
    await ctx.reply('ステータスを[OFFLINE]に変更しました。')
    await bot.logout()
                
                   
bot.run(token)
