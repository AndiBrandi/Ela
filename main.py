from discord import *
from discord.ui import *
from discord import app_commands, Client
from config import LostAdventurersID as server_id, LostAdvVerifyID as verifyID

from config import TOKEN

intents = Intents.all()
client = Client(intents=intents)
client.tree = app_commands.CommandTree(client)

client.activity = Activity(type=ActivityType.watching, name="Next level Moderation")


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
async def verify(origin_interaction: Interaction, known_user: Member, games: str):
    # await interaction.response.send_message(f"**{interaction.user}** - {known_user} \n" + games)

    if origin_interaction.user == known_user:
        await origin_interaction.response.send_message("❌You can't verify yourself")
        return
    elif not known_user.roles.__contains__(origin_interaction.guild.get_role(verifyID)):
        await origin_interaction.response.send_message("❌Only verified users can verify others")
        return

    await origin_interaction.response.send_message(f"{origin_interaction.user} - {known_user} \n{games} \nWaiting for confirmation...")

    button_yes = Button(label="Yes", style=ButtonStyle.success, emoji="👍")
    button_no = Button(label="No", style=ButtonStyle.danger, emoji="👎")
    user_info_embed = Embed(colour=Colour.dark_magenta(), title="Verification request")

    async def button_yes_callback(interaction: Interaction):
        await origin_interaction.user.add_roles(origin_interaction.guild.get_role(verifyID))
        await origin_interaction.edit_original_response(content=f"{origin_interaction.user} - {known_user} \n{games} \n✅Your request was accepted, you are now verified.")
        await interaction.response.edit_message(content=f"✅Accepted User {origin_interaction.user}", view=None)

        return

    async def button_no_callback(interaction: Interaction):
        await origin_interaction.edit_original_response(content="❌The user has declined your request")
        await interaction.response.send_message(content=f"❌Declined User {origin_interaction.user}", view=None)
        return

    button_yes.callback = button_yes_callback
    button_no.callback = button_no_callback
    view = View()
    view.add_item(button_yes)
    view.add_item(button_no)

    user_info_embed.set_thumbnail(url=origin_interaction.user.display_avatar)
    user_info_embed.add_field(name=f"{origin_interaction.user} ", value="claims to know you on:")
    user_info_embed.add_field(name=f"{origin_interaction.guild} ", value="Verify the claim?", inline=False)
    await known_user.send(embed=user_info_embed, view=view)

    # await known_user.send(f"User {origin_interaction.user} claims to know you on {origin_interaction.guild} \n Verify the claim?", view=view)


client.run(TOKEN)
