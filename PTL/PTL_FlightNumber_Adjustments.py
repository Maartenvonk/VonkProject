
def get_Odd_Number(x):
    """
    #usefull to get a returnnumber.
    #checks if number is even or odd
    #if even, -1, make it odd and return
    :param x: flight number of the form "HV1234"
    :return: an oneven flightnumber
    """
    nummer = ""
    for i in range(2, 6):
        nummer += x[i]
    nummertje = int(nummer)
    #if even
    if nummertje % 2 == 0:
        nummertje -= 1
        #new number odd
        return str(nummertje)
    else:
        return str(nummertje)