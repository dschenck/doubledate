import datetime

def isdatelike(value):
    """
    Returns whether a given value has a date-like interface
    To support the arrow library, we do not check for instanceof(date, (datetime.date, datetime.datetime))

    Returns
    ------------
    bool
    """
    try: 
        value.year, value.month, value.day
        return True
    except: 
        return False