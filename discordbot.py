import discord
from discord.ext import commands
import os
import asyncio
import traceback
import logging

token = os.environ['DISCORD_BOT_TOKEN']
prefix = '?.'

class Main(commands.Cog, name='メインコマンド'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot


class JapaneseHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"
        
    def get_ending_note(self):
        return (f"各コマンドの説明: {prefix}help <コマンド名>\n"
                f"各カテゴリの説明: {prefix}help <カテゴリ名>\n")
        
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
async def on_command_error(ctx, error):
    ch = 829611061284044830
    embed = discord.Embed(title="エラー情報", description="", color=0xf00)
    embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
    embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
    embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
    embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
    embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
    embed.add_field(name="発生エラー", value=error, inline=False)
    m = await bot.get_channel(ch).send(embed=embed)
    await ctx.send(f"エラーが発生しました。\nこのエラーについて問い合わせるときはこのコードも一緒にお知らせください\nID：{m.id}")
 
@bot.event
async def on_voice_channel_join(member, channel):
    await discord.utils.get(member.guild.text_channels, name="vc-log").send(f"{member.mention} が {channel.name}　に接続しました。")


@bot.event
async def on_voice_channel_leave(member, channel):
    await discord.utils.get(member.guild.text_channels, name="vc-log").send(f"{member.mention} が {channel.name}　から切断しました。")

@bot.event
async def on_voice_channel_move(member, before, after):
    await discord.utils.get(member.guild.text_channels, name="vc-log").send(f"{member.mention} が {after.name} から　{before.name}　に移動しました。")
                                                                           
@bot.command()
async def rect(ctx, about = "募集", cnt = 4, settime = 10.0):
    """募集を呼び掛ける"""
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
async def hello(ctx):
    """挨拶をする"""
    await ctx.send('こんばんは(　＾∀＾)')
   
@bot.command()
async def baka(ctx):
    """**実行してみよう**"""
    await ctx.reply('自己紹介ありがとうございます(^.^)(-.-)(__)')
    
@bot.command()
async def me(ctx):
    """**あなたが誰かを当てる笑！**"""
    await ctx.send('君、誰だよ！')
                  
@bot.command()
async def lol(ctx):
    """顔文字"""
    await ctx.send('**( ・∀・)**')
    
@bot.command()
@commands.is_owner()
async def offline(ctx):
    """**__ボットのオーナー専用__**"""
    await bot.change_presence(status=discord.Status.offline,activity=discord.Game('開発中(エラー起きてるんゴーw)'))
    await ctx.reply('ステータスを[OFFLINE]に変更しました。')
    await bot.logout()
   
bot = commands.Bot(command_prefix='?.', help_command=JapaneseHelpCommand()) 
bot.add_cog(Main(bot=bot))                   
bot.run(token)
