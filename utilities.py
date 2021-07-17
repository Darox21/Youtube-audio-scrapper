import sys

def convert_time(seconds: int):
    '''
    Returns a string of the time in the most optimal units
    Form: hours, minutes, seconds
    '''
    if seconds < 60:
        return str(seconds) + ' seconds'
    elif seconds < 3600:
        return str(seconds // 60) + ' minutes ' + str(seconds % 60) + ' seconds'
    else:
        return str(seconds // 3600) + ' hours ' + str(seconds // 60) + ' minutes ' + str(seconds % 60) + ' seconds'


def delete_last_lines(n:int=1):
    for _ in range(n):
        sys.stdout.write('\x1b[1A') # Cursor up line
        sys.stdout.write('\x1b[2K') # Erase line
