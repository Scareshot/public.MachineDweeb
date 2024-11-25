'''
Handles accessing the database. All methods tied to interacting with the database must be in here.
Invoke said methods from outside this module, but DO NOT access the database outside of this module.
'''
# Handles accessing the database

# emoji bank 1 guild id: 540103781162156042

import mysql.connector
import os.path
import json
#import discord
import asyncio
from time import sleep

# importing from config files -- DO NOT INCLUDE THESE FILES IN PUBLIC REPO
#from bot_settings import VERSION, COMMAND_DELAY
from database_settings import *
from console_module import Console #, CURRENT_EVENT
from bot_settings import VERSION, COMMAND_DELAY
#from embed_module import createTestEmbed
#import random
#from time import sleep

# global so can be accessed in other module(?)
#global mydb

MODULE_NAME = 'access_module.py'

config = {
    'host': DB_HOST,
    'user': DB_USER,
    'passwd': DB_PASS,
    'database': DB_ITSELF,
    'get_warnings': True
}

class sql:
    '''
    Handles connecting to the SQL database. checkConnection() is called whenever a command needs to use the db,
    and it will reconnect if needed.
    @implNote: make sure to put "sql." infront when accessing mydb or cursor in any command.
    '''
    mydb = mysql.connector.connect(**config) # initial connection upon startup
    cursor = mydb.cursor()

    async def checkConnection():
        '''
        Checks to make sure bot is connected to the database and, if not, reestablishes the connection.
        '''
        print(f"accessed checkConnection()")
        print(f"sql.mydb.is_connected(): ", sql.mydb.is_connected())

        try:
            if sql.mydb.is_connected():
                await Console.Log('status', 'info_dump', "SQL connection ONLINE", MODULE_NAME)
            elif (sql.mydb.is_connected() == False):
                await Console.Log('status', 'info_dump', "SQL connection OFFLINE; reconnecting. . .", MODULE_NAME)
                sql.mydb = mysql.connector.connect(**config)
                sql.cursor = sql.mydb.cursor()

                if (sql.mydb.is_connected()):
                    await Console.Log('status', 'info_dump', "SQL connection ONLINE; successfully reestablished connection", MODULE_NAME)
                else:
                    await Console.Log('error', 'info_dump', "SQL connection OFFLINE; error in reconnecting to database", MODULE_NAME)
            else:
                await Console.Log('error', 'info_dump', "Error in testing connection", MODULE_NAME)
        except:
            await Console.Log('catastrophic_error', 'info_dump', "Exception caught in checkConnection()", MODULE_NAME)

        print("after try-except in checkConnection()")


async def testSQLCommand():
    sleep(COMMAND_DELAY)
    '''
    should return same data as original SQL testing command used
    '''
    await Console.Log('record', 'info_dump', "Accessing testSQLCommand()", MODULE_NAME)

    await sql.checkConnection()
    await Console.Log('record', 'info_dump', "After invocation of sql.checkConnection()", MODULE_NAME)

    try:
        sql.cursor.execute("SELECT guildID FROM Guild;")
        data = sql.cursor.fetchone()
        await Console.Log('record', 'returned', f"data: {data}", MODULE_NAME)

        sql.mydb.close()
        sleep(COMMAND_DELAY)
        return data
    except:
        await Console.Log('error', 'info_dump', "Accessing testSQLCommand()", MODULE_NAME)

    return None


# maybe i'll have this cycle thro a list of guilds the bot is in, if i can find a command that gives such a list
async def insertGuildIDIfNeeded(guildID):
    guildID = int(guildID)
    sleep(COMMAND_DELAY)
    '''
    should check if the guildID is in the db, and if not, insert it.
    '''
    await Console.Log('record', 'info_dump', "Accessing insertGuildIDIfNeeded()", MODULE_NAME)

    await sql.checkConnection()
    await Console.Log('record', 'info_dump', "After invocation of sql.checkConnection()", MODULE_NAME)

    try:
        sql.cursor.execute(
                           f'IF NOT EXISTS(Select guildID from Guild where guildID={guildID})',
                           'BEGIN',
                           f'INSERT INTO Guild (guildID) Values ({guildID})',
                           'END;'
                           )

        await Console.Log('record', 'info_dump', f"inserted: {guildID}", MODULE_NAME)

        sql.mydb.close()
        sleep(COMMAND_DELAY)
    except:
        await Console.Log('error', 'info_dump', "Accessing insertGuildIDIfNeeded()", MODULE_NAME)

'''
IF NOT EXISTS(Select ProductName from Productsnew where ProductName='Jeera Rice')
BEGIN
INSERT INTO Productsnew (ProductName,SupplierID,CategoryID,Unit,Price) Values ('Jeera Rice',1,7,'7,5 kg',120)
END'''