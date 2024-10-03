import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=",", intents=discord.Intents.all())
bot.remove_command("help")

with open("Bot/token.json") as f:
    BOT_TOKEN = json.load(f)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('YOUR SERVER NAME'))
    print(f"Logged in as: {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} has been kicked. Reason: {reason}")
    except:
        await ctx.send(f"❌ Failed to kick {member.mention}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member.mention} has been banned. Reason: {reason}")
    except:
        await ctx.send(f"❌ Failed to ban {member.mention}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, duration: int, *, reason=None):
    try:
        await member.timeout_for(duration=discord.utils.timedelta(minutes=duration), reason=reason)
        await ctx.send(f"✅ {member.mention} has been muted for {duration} minutes. Reason: {reason}")
    except:
        await ctx.send(f"❌ Failed to mute {member.mention}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    try:
        embed = discord.Embed(title="Warning", description=f"You have been warned on **{ctx.guild.name}**", color=discord.Color.orange())
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
        await member.send(embed=embed)
        await ctx.send(f"✅ {member.mention} has been warned. Reason: {reason}")
    except:
        await ctx.send(f"❌ Failed to warn {member.mention}")

@kick.error
@ban.error
@mute.error
@warn.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You do not have permission to use this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Member not found.")
    else:
        await ctx.send("❌ An error occurred while trying to execute the command.")

bot.run(BOT_TOKEN)
