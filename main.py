from discord import *
from discord.ext import commands
from discord import app_commands, Client
from config import LostAdventurersID as server_id, LostAdvVerifyID as verifyID
from discord import RoleTags

from config import TOKEN

intents = Intents.default()
client = Client(intents=intents)
client.tree = app_commands.CommandTree(client)

client.activity = Activity(type=ActivityType.watching,name="Next level Moderation")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    try:
        await client.tree.sync(guild=Object(id=server_id))
        print("App-commands synced")
    except Exception as e:
        print(e)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@client.tree.command(name="verify", description="Verify yourself", guild=Object(id=server_id))
@app_commands.describe(known_user="The user that brought you to this server", games="Games that are being played")
async def verify(interaction: Interaction, known_user: Member, games: str):
    await interaction.response.send_message(f"**{interaction.user}** - {known_user} \n" + games)
    await interaction.user.add_roles(interaction.guild.get_role(verifyID))


client.run(TOKEN)
