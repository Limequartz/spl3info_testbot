import discord
import spl3ink

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$X'):
        match_info = spl3ink.get_match_infos().x
        embed = discord.Embed(title=str(match_info.match_type), url='https://splatoon3.ink/', description=str(match_info.start_datetime) + "~" + str(match_info.end_datetime))
        embed.add_field(name=str(match_info.vs_rule), value=str(match_info.maps[0]), inline=True)
        embed.add_field(name="\0", value=str(match_info.maps[1]), inline=True)
        await message.channel.send(embed=embed)
    if message.content.startswith('$C'):
        match_info = spl3ink.get_match_infos().challenge
        embed = discord.Embed(title=str(match_info.match_type), url='https://splatoon3.ink/', description=str(match_info.start_datetime) + "~" + str(match_info.end_datetime))
        embed.add_field(name=str(match_info.vs_rule), value=str(match_info.maps[0]), inline=True)
        embed.add_field(name="\0", value=str(match_info.maps[1]), inline=True)
        await message.channel.send(embed=embed)
    if message.content.startswith('$O'):
        match_info = spl3ink.get_match_infos().open
        embed = discord.Embed(title=str(match_info.match_type), url='https://splatoon3.ink/', description=str(match_info.start_datetime) + "~" + str(match_info.end_datetime))
        embed.add_field(name=str(match_info.vs_rule), value=str(match_info.maps[0]), inline=True)
        embed.add_field(name="\0", value=str(match_info.maps[1]), inline=True)
        await message.channel.send(embed=embed)
    if message.content.startswith('$R'):
        match_info = spl3ink.get_match_infos().regular
        embed = discord.Embed(title=str(match_info.match_type), url='https://splatoon3.ink/', description=str(match_info.start_datetime) + "~" + str(match_info.end_datetime))
        embed.add_field(name=str(match_info.vs_rule), value=str(match_info.maps[0]), inline=True)
        embed.add_field(name="\0", value=str(match_info.maps[1]), inline=True)
        await message.channel.send(embed=embed)

client.run('MTA0ODUxNTMwNDg2NDYzMjg1Mg.GulKmE.iEDonj0bvzWp5yrl4okOcdf5LHU4DcYBh7jfOA')