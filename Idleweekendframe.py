import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys
from matplotlib import colors
from collections import defaultdict
import pickle
import networkx as nx
import pulp
from pulp import *

filefolder='C:\\Users\\u03mvo\\OneDrive - TRANSAVIA AIRLINES C.V\\Documents\\Pythonexports\\Naivescheduling\\'
Totalframe = pd.read_pickle(filefolder + 'Totalframe6-6s10')
Dutyframe = pd.read_pickle(filefolder + 'Dutyframe6-6s10')
Weekendframe = pd.read_pickle(filefolder + 'Weekendframe6-6s10')
print(Dutyframe.columns)
print(len(Dutyframe))
def idlecosts(duty1end,duty2start):
    if duty2start-mdates.date2num(duty1end)>=0:
        idletime = duty2start-mdates.date2num(duty1end)
    else:
        idletime=10000
    return idletime
def idlecostweekend(duty1end, Nightflight1, Rest1, duty2start):
    if Nightflight1=='NIGHT':
        if duty2start-(mdates.date2num(duty1end)+Rest1)>3:
            idleweekendtime= duty2start-(mdates.date2num(duty1end)+Rest1)
        else:
            idleweekendtime=0
    else:
        if duty1end.hour != 0:
            Startweekend = (duty1end + pd.Timedelta(1, unit='d')).replace(hour=1, minute=0)
            if duty2start - mdates.date2num(Startweekend) > 3:
                idleweekendtime = duty2start - mdates.date2num(duty1end)
            else:
                idleweekendtime=0
        else:
            Startweekend = (duty1end).replace(hour=1, minute=0)
            if duty2start - mdates.date2num(Startweekend) > 3:
                idleweekendtime = duty2start - mdates.date2num(duty1end)
            else:
                idleweekendtime=0
    return idleweekendtime

z2= [[0 for x in range(len(Dutyframe))] for y in range(len(Dutyframe))]
for i in range(len(Dutyframe)):
   for j in range(len(Dutyframe)):
       z2[i][j] = idlecostweekend(Dutyframe.loc[i,'Endduty'],Dutyframe.loc[i,'Nightflight'],Dutyframe.loc[i,'minrest']/1440,Dutyframe.loc[j,'Startduty'])


write_loc ='C:\\Users\\u03mvo\\OneDrive - TRANSAVIA AIRLINES C.V\\Documents\\Pythonexports\\Naivescheduling\\'
z2.to_pickle(write_loc+ 'z2-10')
sys.exit()