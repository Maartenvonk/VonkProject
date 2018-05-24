def isfloat(value):
    """"Checks if value can be converted to a float, then returns True"""
    try:
        float(value)
        return True
    except:
        return False