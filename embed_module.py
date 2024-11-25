'''
Handles creating embeds.
\nEmbeds are created here and then returned. Embeds are not sent to discord from here!
'''


import os.path
import json
import asyncio
import discord
from discord import app_commands

# importing from config files -- DO NOT INCLUDE THESE FILES IN PUBLIC REPO
from bot_settings import VERSION, COMMAND_DELAY
from console_module import Console
from time import sleep

MODULE_NAME = 'embed_module.py'

async def createTestEmbed():
    '''
    creates a sample embed with all of the fields
    '''
    embed = discord.Embed(title="embedTitle", 
                        description="embedDescription",
                        color=discord.Color.blurple(),
                            )
    
    embed.add_field(name="inline field", value="fieldValue", inline=True)
    embed.add_field(name="!inline field", value="fieldValue", inline=False)
    embed.set_footer(text="footer")
    embed.set_thumbnail(url="https://i.imgur.com/3DxCgxi.png")
    
    await Console.Log('record', 'info_dump', "Creating & sending a test embed", MODULE_NAME)

    return embed

# older, commented out code. ignore for now.
'''from time import sleep
import asyncio
import discord
from discord.ext import commands
#from mainModule import grabAvatarUrlFromID
from consoleModule import Console, VERSION

MODULE_NAME = 'embedModule'

commandsToShowPicture = ['$shop', '$bal', '$inv']

async def sendEmbedMessage(message, embedTitle, embedDescription, embedColour, fieldName, fieldValue, fieldInlineTF, embedFooter, originCommand, avatar_url):
    showPicture = False

    # so that I don't have to worry about figuring out what to send unless i care
    if embedColour == 'default':
        embedColour = discord.Color.blurple()
    if fieldInlineTF == 'default':
        fieldInlineTF = False
    if embedFooter == 'default':
        embedFooter = f"Running MachineDweeb {VERSION}"
        
    currentEmbedSize = 0

    # field title char count
    #await Console.Log('record', 'info_dump', f'Embed title character count: {len(embedTitle)}/256', f'{MODULE_NAME}')
    if len(embedTitle) >= 256:
        await Console.Log('error', 'info_dump', f'Err:1000', f'{MODULE_NAME}')
        embedTitle = 'Err:1000'

    currentEmbedSize += len(embedTitle)

    # field description char count
    #await Console.Log('record', 'info_dump', f'Embed description character count: {len(embedDescription)}/4096', f'{MODULE_NAME}')
    if len(embedDescription) >= 4096:
        await Console.Log('error', 'info_dump', f'Err:1001', f'{MODULE_NAME}')
        embedDescription = 'Err:1001'

    currentEmbedSize += len(embedDescription)

    embed = discord.Embed(title=embedTitle, 
                            description=embedDescription,
                            color=embedColour)

    # if fieldName or fieldValue are 'none', don't show field
    if fieldName == 'none' or fieldValue == 'none':
        pass
    else:
        embed.add_field(name=fieldName, value=fieldValue, inline=fieldInlineTF)

    # if embedFooter is none, don't show footer
    if embedFooter == 'none':
        pass
    else:
        #await Console.Log('record', 'info_dump', f'Embed footer character count: {len(embedFooter)}/2048', f'{MODULE_NAME}')
        if len(embedFooter) >= 2048:
            await Console.Log('error', 'info_dump', f'Err:1002', f'{MODULE_NAME}')
            embedFooter = 'Err:1002'

        embed.set_footer(text=embedFooter)

    currentEmbedSize += len(embedFooter)

    if originCommand in commandsToShowPicture:
        #await Console.Log('record', 'info_dump', f'originCommand in commandsToShowPicture | show picture is true', f'{MODULE_NAME}')
        showPicture = True
    else:
        showPicture = False # defaults to False but doing this anyway just incase

    if showPicture:
        match originCommand:
            case '$inv':
                pictureToUse = avatar_url
            case '$bal':
                pictureToUse = avatar_url
            case '$shop':
                pictureToUse = "https://i.imgur.com/3DxCgxi.png"

        embed.set_thumbnail(url=pictureToUse)

    #print(f'in sendEmbedMessage -- literally right before sending the embed')
    #await Console.Log('record', 'info_dump', f'just before sending embed | characters vs limit: {len(embed)}/6000', f'{MODULE_NAME}')


    #Embed title is limited to 256 characters
    #Embed description is limited to 4096 characters
    #An embed can contain a maximum of 25 fields
    #A field name/title is limited to 256 character and the value of the field is limited to 1024 characters
    #Embed footer is limited to 2048 characters
    #Embed author name is limited to 256 characters
    #The total of characters allowed in an embed is 6000

    # determining character count of fields and their names
    for field in list(embed.fields):
        fieldsIndex = list(embed.fields).index(field)
        #await Console.Log('record', 'info_dump', f'Embed field ({(field.name)}) at index ({fieldsIndex}) character counts: name: {len(field.name)}/256 | value: {len(field.value)}/1024', f'{MODULE_NAME}')

        # field value (the text in each)
        if len(field.value) >= 1024:
            fieldValue = f'Err:1003-{fieldsIndex}'
            await Console.Log('error', 'info_dump', f'Err:1003-{fieldsIndex}', f'{MODULE_NAME}')
            embed.remove_field(fieldsIndex)
            embed.insert_field_at(fieldsIndex, name=f'Err:1003-{fieldsIndex}', value=f'Err:1003-{fieldsIndex}', inline=False)

        currentEmbedSize += len(field.value)

        # field name
        if len(field.name) >= 256:
            fieldName = f'Err:1004-{fieldsIndex}'
            await Console.Log('error', 'info_dump', f'Err:1004-{fieldsIndex}', f'{MODULE_NAME}')
            embed.remove_field(fieldsIndex)
            embed.insert_field_at(fieldsIndex, name=fieldName, value=fieldValue, inline=False)

        currentEmbedSize += len(field.name)

    # number of fields
    #await Console.Log('record', 'info_dump', f'Embed field count: {len(embed.fields)}/25', f'{MODULE_NAME}')
    if len(embed.fields) >= 25:
        await Console.Log('error', 'info_dump', f'Err:1005', f'{MODULE_NAME}')
        embedDescription = 'Err:1005'
        while len(embed.fields) == 25:
            embed.remove_field(24)

    await Console.Log('record', 'info_dump', f'Final embed character count: {currentEmbedSize}/6000', f'{MODULE_NAME}')


    # final check, will throw unique error and purge all but title & footer in embed if max character limit (6000) is met
    if currentEmbedSize >= 6000:
        await Console.Log('error', 'info_dump', f'Err:1006', f'{MODULE_NAME}')
        embed = discord.Embed(title=embedTitle, 
                            description='Err:1006',
                            color=embedColour)

        embed.set_footer(embedFooter)

    await message.channel.send(embed=embed)'''