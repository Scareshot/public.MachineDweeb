'''
Exists to provide an easy-to-use method for printing formatted text to console. 
\nSee docstrings for Console and Log for more info.
'''
#TODO: clean this file up and establish a new/updated logging system

from time import sleep
import datetime # used to track date and time of logs
import asyncio
from bot_settings import VERSION, COMMAND_DELAY


CURRENT_EVENT = 'None'

MODULE_NAME = 'console_module.py'

# simple class & method combo so that I can use Console.Log when printing stuff to 
class Console:
    '''
    Allows the use of Console.Log(...) to print formatted logs to console. 
    Usage:
        logType: error, record, catastrophic_error, empty
        logCategory: info_dump, returned, 
        logDesc: string to print
        logModule: pass in MODULE_NAME
    For more detailed descriptions, see Log.
    '''
    async def Log(logType, logCategory, logDesc, logModule):
        '''
        Note: <state> = Failed/Successful(ly)/Unsuccessfully or success/failure
        \nCommon examples:\n

        logType:
        \n* record:             'Record -- '
        \n* status:             'Status -- '
        \n* error:              '[!] Error -- '
        \n* catastrophic_error: 'CATASTROPHIC FAILURE -- ' (prints newline before itself too)
        \n* empty:              ''  (this doesn't print the time)
        \n* _:                  'ConsoleError[null_log_type] -- '

        logCategory:
        \n* info_dump:             '{logDesc} -- [{logModule}]'
        \n* returned:              'Return value of {logDesc} -- [{logModule}]'
        \n* function_call:         'Calling function {logDesc} -- [{logModule}]'
        \n* command_<state>:       '<state> command input {logDesc} -- [{logModule}]'
        \n* purchase_<state>:      'Purchase <state> | purchase details: \n{logDesc} -- [{logModule}]'
        \n* _:                     '[null_log_category] -- {logDesc} -- [{logModule}]'
        '''
        sleep(COMMAND_DELAY)

        # standardising cases in string logType
        logType = logType.lower()
        #logCategory = logCategory.lower()

        # 2 strings (1 for: logType, 1 for logCategory and logDesc) which are concatenated into logString before it is then printed to the console.

        #logString = f'{datetime.datetime.now()} -- '

        time = datetime.datetime.now()
        time = time.strftime("%b %d %Y %-I:%M %p -- ")
        printNewLine = False

        # if it's empty, then it won't print the time (i.e., when using it to just print an empty line)
        if (logType != 'empty'):
            logString = f'{time}'
        else:
            logString = ''

        match logType:
            case 'error':
                logString += '[!] Error -- '
            case 'record':
                logString += 'Record -- '
            case 'status':
                logString += 'Status -- '
            case 'catastrophic_error':
                logString += '\nCATASTROPHIC FAILURE -- '
            case 'empty':
                logString += ''
            case _:
                logString += 'ConsoleError[null_log_type] -- '

        if logDesc == None:
            logDesc = '[null_log_desc]'

        if logModule == None:
            logModule = '[null_log_module]'
        elif logModule == "empty":
            logModule = ' '

        match logCategory:
            case 'info_dump':
                logString += f'{logDesc} -- [{logModule}]'

            case 'timed_reward':
                logString += f'Handed out {logDesc} to all users -- [{logModule}]'

            case 'command_failure':
                logString += f'Failed command input {logDesc} -- [{logModule}]'
            case 'command_success':
                logString += f'Successful command input {logDesc} -- [{logModule}]'

            case 'purchase_failure':
                logString += f'Purchase failure | purchase details: \n{logDesc} -- [{logModule}]'
            case 'purchase_success':
                logString += f'Purchase success | purchase details: \n{logDesc} -- [{logModule}]'

            case 'initialise_start':
                logString += f'Initialising {logDesc} -- [{logModule}]'
            case 'initialise_success':
                logString += f'Successfully initialised {logDesc} -- [{logModule}]'
            case 'initialise_failure':
                logString += f'Failed to initialise {logDesc} -- How did this even print? -- [{logModule}]'

            case 'returned':
                logString += f'Return value of {logDesc} -- [{logModule}]'

            case 'function_call':
                logString += f'Calling function {logDesc} -- [{logModule}]'

            case 'save_start':
                logString += f'Attempting to save {logDesc} -- [{logModule}]'
            case 'save_success':
                logString += f'Successfully saved {logDesc} -- [{logModule}]'
            case 'save_failure':
                logString += f'Failed to save {logDesc} -- [{logModule}]'

            case 'check_success':
                logString += f'Check success for {logDesc} -- [{logModule}]'
            case 'check_failure':
                logString += f'Check failure for {logDesc} -- [{logModule}]'

            case 'load_start':
                logString += f'Loading {logDesc} -- [{logModule}]'
            case 'load_success':
                logString += f'Successfully loaded {logDesc} -- [{logModule}]'
            case 'load_failure':
                logString += f'Failed to load {logDesc} -- [{logModule}]'

            case 'locate_success':
                logString += f'Successfully loaded data from {logDesc} -- [{logModule}]'
            case 'locate_failure':
                logString += f'Failed to locate data from {logDesc} -- [{logModule}]'

            case 'found_in_success':
                logString += f'Successfully found {logDesc} -- [{logModule}]'
            case 'found_in_failure':
                logString += f'Failed to find {logDesc} -- [{logModule}]'

            case 'final_load':
                logString += f'Successfully loaded MachineDweeb {VERSION}.\n'
                printNewLine = True

            case 'empty':
                logString += ' '

            case _:
                logString += f'[null_log_category] -- {logDesc} -- [{logModule}]'

        print(logString)

        #if printNewLine:
        #    print()

    async def logNewLine():
        '''
        Literally just prints an empty line to the console. That's all.
        It's to prevent any confusion caused by using print("") admist Console.Log(...).
        \nNOTE: This is for use in main_module.py! place it at the end of every command.
        '''
        # await Console.Log('empty', 'empty', "-", 'empty') # why did I ever even use this in the first place?
        print('\n ')