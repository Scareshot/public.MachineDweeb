'''
The main running file (/ module) for the bot. Handles discord intents and commands.
'''

#region crucial setup code
import os.path
import json
import asyncio
import discord
from discord import app_commands
# make specific (import class) rather than *, later.

# importing from config files -- DO NOT INCLUDE THESE FILES IN PUBLIC REPO
from bot_settings import VERSION, COMMAND_DELAY, TOKEN
from console_module import Console
from embed_module import createTestEmbed
import access_module
from items.item_generator import ItemGenerator, loadJsonData
import random
from time import sleep

MODULE_NAME = 'main_module.py'
#MY_GUILD = 540103781162156042 #(emoji bank 1 guild id)

print(f'\nPreloading -- start | Version: {VERSION}')
print('Preloading -- after imports')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#endregion

# NOTE: Make all commands silent, so that people aren't spammed by pings
# TODO: needa test commands w/ diff perm levels, and test to see if i can grab channel/user/perms/role/whatever from a command

#region tree commands
#region base commands
@tree.command(
    name="test",
    description="First application command",
    guild=discord.Object(id=540103781162156042) # remove argument when making them for all guilds, rn it's setup for alt 1
)
async def test_command(interaction):
    '''
    first command; to test that slash commands work
    '''
    await Console.Log('record', 'info_dump', "Invoking test command", MODULE_NAME)
    await interaction.response.send_message(content="Hello World!\nBot version: %s" % VERSION, silent=True)
    await Console.logNewLine()

# old command, no need for extra help when users see descriptions and crap already.
''''''
#detailed help command; sends a DM to user with commands and their descriptions/usage
'''
@tree.command(
    name="machine-dweeb-help",
    description="Sends a DM containing a detailed list of commands for MachineDweeb.",
    guild=discord.Object(id=540103781162156042) # remove argument when making them for all guilds, rn it's setup for alt 1
)
async def detailed_help(interaction):
    await interaction.response.send_message(content="test uwu", ephemeral=True, silent=True)
    #await interaction.response.send_message("Hello!")'''


@tree.command(
    name="test-embed",
    description="Testing the bot's ability to send an embed.",
    guild=discord.Object(id=540103781162156042) # remove argument when making them for all guilds, rn it's setup for alt 1
)
async def test_embed(interaction):
    '''
    tests sending embeds
    '''
    sleep(COMMAND_DELAY) # to slightly prevent spamming from breaking smth (idk if it will, it's just in case)
    testEmbed = await createTestEmbed()
    await interaction.response.send_message(content="contentText", embed=testEmbed, silent=True)
    await Console.logNewLine()
#endregion


#region sql commands
@tree.command(
    name="test-sql",
    description="Testing the bot's ability to connect to the database.",
    guild=discord.Object(id=540103781162156042) # remove argument when making them for all guilds, rn it's setup for alt 1
)
@app_commands.checks.cooldown(1, 1.0, key=lambda i: (i.guild_id, i.user.id)) # setting a cooldown of 1 seconds per member on the command
async def test_sql(interaction):
    '''
    tests SQL connection
    '''
    await Console.Log('record', 'info_dump', "Invoking testSQLCommand()", MODULE_NAME)
    await interaction.response.send_message(content="Grabbing data...", silent=True)
    
    data = await access_module.testSQLCommand() # not sure if separating is necessary, but i'll do it here just in case.
    await editMsgAfterSQLResponse(interaction, data)

    await Console.logNewLine()


@tree.command(
    name="test-insert-guild-id",
    description="Testing the bot's ability to insert guildID if needed.",
    guild=discord.Object(id=540103781162156042) # remove argument when making them for all guilds, rn it's setup for alt 1
)
@app_commands.checks.cooldown(1, 1.0, key=lambda i: (i.guild_id, i.user.id)) # setting a cooldown of 1 seconds per member on the command
async def test_insert_guild_id(interaction):
    '''
    tests SQL connection
    '''
    await Console.Log('record', 'info_dump', "Invoking insertGuildIDIfNeeded()", MODULE_NAME)
    await interaction.response.send_message(content="Checking database...", silent=True)

    await access_module.insertGuildIDIfNeeded(interaction.guild_id) # not sure if separating is necessary, but i'll do it here just in case.
    #await editMsgAfterSQLResponse(interaction, data)

    await Console.logNewLine()


@tree.command(
    name="test-ids",
    description="Passes in your discord ID and the guild's ID.",
    guild=discord.Object(id=540103781162156042) # remove argument when making them for all guilds, rn it's setup for alt 1
)
@app_commands.checks.cooldown(1, 1.0, key=lambda i: (i.guild_id, i.user.id)) # setting a cooldown of 1 seconds per member on the command
async def test_ids(interaction):
    '''
    tests SQL connection
    '''
    guildID = interaction.guild_id
    discordUserID = interaction.user.id
    await Console.Log('record', 'info_dump', f"guildID: {guildID} | discordUserID: {discordUserID}", MODULE_NAME)
    await interaction.response.send_message(content=f"guildID: {guildID} | discordUserID: {discordUserID}", silent=True)
    
    #data = await access_module.testSQLCommand() # not sure if separating is necessary, but i'll do it here just in case.
    #await editMsgAfterSQLResponse(interaction, data)

    await Console.logNewLine()
#endregion


#region item commands
@tree.command(
    name="test-set-item",
    description="Attempts to initialise an item of a set itemID (1).",
    guild=discord.Object(id=540103781162156042) # remove argument when making them for all guilds, rn it's setup for alt 1
)
async def test_command(interaction):
    '''
    Generates an object based on item data corresponding to itemID 1.
    '''
    #await interaction.response.send_message(content="dataaaa : %s" % itemGenerator.data, silent=True)
    itemObj = await itemGenerator.returnItemWithID(1)
    #print(f"can i do *anything* with this? {itemObj}")
    await interaction.response.send_message(content="itemObj : %s" % itemObj, silent=True)
    '''
    attributesToString = itemObj.attributesToString()
    
    #await Console.Log('record', 'info_dump', "Invoking test command", MODULE_NAME)
    await interaction.response.send_message(content="attributesToString : %s" % attributesToString, silent=True)
    #await Console.logNewLine()
    '''

@tree.command(
    name="test-item",
    description="Attempts to initialise an item of a given itemID.",
    guild=discord.Object(id=540103781162156042) # remove argument when making them for all guilds, rn it's setup for alt 1
)
async def test_command(interaction, id: int):
    '''
    Generates an item based on the given itemID integer.
    '''
    itemObj = await itemGenerator.returnItemWithID(id)
    #attributesToString = await itemObj.__str__()

    #await Console.Log('record', 'info_dump', "Invoking test command", MODULE_NAME)
    await interaction.response.send_message(content="itemObj : %s" % itemObj, silent=True)
    #await Console.logNewLine()
#endregion


#region tree errors
# handles command tree errors
@tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        await Console.Log('record', 'info_dump', f"CommandOnCooldown caught | {str(error)}", MODULE_NAME)
        await interaction.response.send_message(content=f"Command is on cooldown; {str(error)}", silent=True, ephemeral=True)
        
    elif isinstance(error, discord.app_commands.MissingPermissions):
        await Console.Log('record', 'info_dump', f"MissingPermissions caught | {str(error)}", MODULE_NAME)
        await interaction.response.send_message(content="User has insufficient permissions", silent=True, ephemeral=True)

    elif isinstance(error, discord.app_commands.BotMissingPermissions):
        await Console.Log('record', 'info_dump', f"BotMissingPermissions caught | {str(error)}", MODULE_NAME)
        #await interaction.response.send_message(content="Bot has insufficient permissions to run that command", silent=True, ephemeral=True)

    elif isinstance(error, discord.app_commands.CheckFailure):
        await Console.Log('error', 'info_dump', f"CheckFailure caught | {str(error)}", MODULE_NAME)
        #await interaction.response.send_message(content="Error; Check failure occured", silent=True, ephemeral=True)

    elif isinstance(error, discord.app_commands.CommandSyncFailure):
        await Console.Log('catastrophic_error', 'info_dump', f"CommandSyncFailure caught | {str(error)}", MODULE_NAME)
        #await interaction.response.send_message(content="Error; Failed to sync commands", silent=True, ephemeral=True)

    else:
        await Console.Log('catastrophic_error', 'info_dump', f"tree.error caught | {str(error)}", MODULE_NAME)
        #await interaction.response.send_message(content="Error; Unchecked exception caught", silent=True, ephemeral=True)
#endregion

#endregion

'''# handles general bot errors
@client.event
async def on_error(ctx, error):
    await Console.Log('catastrophic_error', 'info_dump', f"client.error caught | {str(error)}", MODULE_NAME)'''


#region async methods
@client.event
async def on_ready():
    '''
    Contains code that is to be run immediately following successful start up of the bot.
    '''
    #MY_GUILD = discord.Object(id=540103781162156042)
    #await tree.sync(guild=MY_GUILD)
    await tree.sync(guild=discord.Object(id=540103781162156042))

    data = await loadJsonData()

    global itemGenerator
    itemGenerator = ItemGenerator(data)
    #itemGenerator.loadJsonData()
    print("Ready!")
    #await client.change_presence(status=discord.Status, activity=discord.CustomActivity(name='ÔwÔ'))
    await client.change_presence(status=discord.Status, activity=discord.CustomActivity(name='Being Redesigned :) | %s' % VERSION))

    print(f"itemGenerator : {itemGenerator}")


async def editMsgAfterSQLResponse(interaction, data):
    '''
    will edit whatever response was sent after we grab the SQL data (or when we fail)
    '''
    msg = await interaction.original_response()

    try:
        await msg.edit(content=str(data))
    except:
        await Console.Log('error', 'info_dump', "Failed to grab data", MODULE_NAME)
        await msg.edit(content="Failed to grab data.")


async def editMsg(interaction, newContent):
    '''
    will edit whatever response was sent previously
    '''
    msg = await interaction.original_response()

    try:
        await msg.edit(content=newContent)
    except:
        await Console.Log('error', 'info_dump', "Failed to edit content of message", MODULE_NAME)
#endregion


#region crucial EOF bot setup
# has to be here at the end of the file
print('Preloading -- before loading bot token')
client.run(TOKEN)
print('Preloading -- after loading bot token')
sleep(COMMAND_DELAY)
#endregion




#region deprecated setup
'''
import os.path
import discord
import asyncio
from discord.ext import commands

#from userCmdModule import * #as RunCommand # handles commands from user on discord. has an admin subclass to handle those cmds

from database_settings import HOST, PORT, USER, PASSWORD, DATABASE
from bot_settings import VERSION, BOT_TOKEN, COMMAND_DELAY
from console_module import Console, CURRENT_EVENT

import random
from time import sleep



import mysql.connector
global mydb 
mydb = mysql.connector.connect(
   host=HOST,
   port=PORT,
   user=USER,
   password=PASSWORD,
   database=DATABASE
)
cursor = mydb.cursor()

MODULE_NAME = 'main_module'

TIMED_REWARD_COOLDOWN_TEXT = '1h' # in seconds; 3600 = 1h = 60min
#region wacky code for converting above constant
# Calculator that reads time as a string. Holdover from old code, but it works perfectly so who cares
if TIMED_REWARD_COOLDOWN_TEXT != None:

    if TIMED_REWARD_COOLDOWN_TEXT.endswith('h'):
        hours = int(TIMED_REWARD_COOLDOWN_TEXT.replace('h', ''))
        minutes = hours * 60
        seconds = minutes * 60
        print(f'TIMED_REWARD_COOLDOWN: {seconds}s')
        TIMED_REWARD_COOLDOWN = seconds

    elif TIMED_REWARD_COOLDOWN_TEXT.endswith('m'):
        minutes = int(TIMED_REWARD_COOLDOWN_TEXT.replace('m', ''))
        seconds = minutes * 60
        print(f'TIMED_REWARD_COOLDOWN: {seconds}s')
        TIMED_REWARD_COOLDOWN = seconds

    elif TIMED_REWARD_COOLDOWN_TEXT.endswith('s'):
        seconds = int(TIMED_REWARD_COOLDOWN_TEXT.replace('s', ''))
        print(f'TIMED_REWARD_COOLDOWN: {seconds}s')
        TIMED_REWARD_COOLDOWN = seconds
#endregion

HELP_DESC_TEXT = f'The list of commands MachineDweeb is programmed to respond to.'



print(f'\nPreloading -- start | Version: {VERSION}  test')
print('Preloading -- after imports')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# brought over from old versions; do not touch, there's no reason to
global bot 
bot = commands.Bot(command_prefix='$', intents=intents)
global LIST_OF_COMMANDS
LIST_OF_COMMANDS = bot.commands
NEW_HELP_CMD_REF = bot.help_command
global HELP_COMMAND_OBJ_REF
HELP_COMMAND_OBJ_REF = commands.HelpCommand

# -------------
print('Preloading -- after bot intent stuff')
print('Preloading -- determining bot token')
botToken_loaded = os.path.isfile('botToken.txt')
'''
#endregion