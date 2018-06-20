import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys
from matplotlib import colors
from collections import defaultdict
import pickle

filefolder='C:\\Users\\u03mvo\\OneDrive - TRANSAVIA AIRLINES C.V\\Documents\\Pythonexports\\Naivescheduling\\'
Totalframe = pd.read_pickle(filefolder + 'Totalframe5-6')
Dutyframe = pd.read_pickle(filefolder + 'Dutyframe5-6')
Weekendframe = pd.read_pickle(filefolder + 'Weekendframe5-6')
print(Dutyframe)

dict_gantt = Totalframe.groupby('Crewmember')['Startduty', 'Offset'] \
    .apply(lambda x: list(zip(x['Startduty'].tolist(),
                              x['Offset'].tolist()))) \
    .to_dict()



# Making Gantt figure
FltReg_list = sorted(dict_gantt)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

start_datetime = Dutyframe['Startduty'].min()
end_datetime = Dutyframe['Newstart'].max()

# parameters for yticks, etc.
# you might have to play around
# with the different parts to modify
n = len(FltReg_list)
bar_size = 9
default_color = 'blue'
colors_dict = defaultdict(lambda: default_color, DAY='green', NIGHT='red', Weekend='blue', Preweekend='blue')

for i, bar in enumerate(FltReg_list):
    mask = Totalframe.Crewmember == bar
    ax.broken_barh(dict_gantt[bar],  # data
                   (10 * (i + 1), bar_size),  # (y position, bar size)
                   alpha=0.75,
                   facecolors=[colors_dict[event] for event in Totalframe.loc[mask].Nightflight],
                   edgecolor='k',
                   linewidth=1.2)



# I got date formatting ideas from
# https://matplotlib.org/examples/pylab_examples/finance_demo.html
ax.set_xlim(start_datetime, end_datetime)
ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 24)))  # HourLocator(byhour=range(0, 24, 6))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=range(0, 24, 1)))
# omitting minor labels ...

# plt.grid(b=True, which='minor', color='r', linestyle='solid')

ax.set_yticks([5 + 10 * n for n in range(1, n + 1)])
ax.set_ylim(5, 5 + 10 * (n + 1))
ax.set_yticklabels(FltReg_list)

ax.set_title('Roster')
ax.set_ylabel('Task Sort')

plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')

plt.tight_layout()
fig.show('gantt.png')
fig.canvas._master.wait_window()

crewlist=Dutyframe.Crewmember.unique()
for crewmember in crewlist:
    Dutyframecrew = Dutyframe[Dutyframe['Crewmember'] == crewmember]
    totidle = Dutyframecrew['Idlebeforeduty'].sum()
    print(crewmember, totidle)


for index, row in Dutyframe.iterrows():
    if Dutyframe.loc[index,'Idlebeforedutyweekend']>3:
        Tempoframe=Dutyframe[Dutyframe['Crewmember']==Dutyframe.loc[index,'Crewmember']]
        jobindex = Tempoframe.index[Tempoframe.index.get_loc(index)-1]
        if Dutyframe.loc[jobindex, 'Nightflight'] == 'DAY':
            endlastdutyforweekend = Dutyframe.loc[jobindex, 'Endduty']
            if endlastdutyforweekend.hour != 0:
                Startweekend = (endlastdutyforweekend + pd.Timedelta(1, unit='d')).replace(hour=1, minute=0)
            else:
                Startweekend = (endlastdutyforweekend).replace(hour=1, minute=0)
            temporaryweekendframe = pd.DataFrame({'Startweekend': [Startweekend],
                                                  'Endweekend': [Startweekend + pd.Timedelta(3, unit='d')],
                                                  'Weekendsort': [Startweekend.hour],
                                                  'Crewmember': [Dutyframe.loc[jobindex, 'Crewmember']]})
        else:
            temporaryweekendframe = pd.DataFrame({'Startweekend': [
                Dutyframe.loc[jobindex, 'Endduty'].dt.ceil('H') + pd.Timedelta(
                    Dutyframe.loc[jobindex, 'minrest'], unit='m')],
                'Endweekend': [Dutyframe.loc[jobindex, 'Endduty'].dt.ceil(
                    'H').iloc[-1] + pd.Timedelta(Dutyframe.loc[jobindex, 'minrest'],
                                                 unit='m') + pd.Timedelta(3,
                                                                          unit='d')],
                'Weekendsort': [(Dutyframe.loc[jobindex, 'Endduty'].dt.ceil(
                    'H') + pd.Timedelta(Dutyframe.loc[jobindex, 'minrest'], unit='m')).hour],
                'Crewmember': [Dutyframe.loc[jobindex, 'Crewmember']]})
        Dutyframe.loc[index, 'Idlebeforedutyweekend']=Dutyframe.loc[index,'Startduty']-mdates.date2num(temporaryweekendframe['Endweekend'].iloc[0])
        Dutyframe.loc[index, 'Idlebeforeduty']=Dutyframe.loc[index,'Startduty']-temporaryweekendframe['Endweekend'].apply(mdates.date2num).iloc[0]
        Weekendframe = Weekendframe[Weekendframe['Crewmember']!=Dutyframe.loc[index,'Crewmember']]
        temporaryweekendframe['Startweekend'] = temporaryweekendframe['Startweekend'].apply(mdates.date2num)
        Weekendframe = pd.concat([Weekendframe, temporaryweekendframe])

for crewmember in crewlist:
    Dutyframecrew = Dutyframe[Dutyframe['Crewmember'] == crewmember]
    totidle = Dutyframecrew['Idlebeforeduty'].sum()
    print(crewmember, totidle)

Weekendframe['Offset'] = 3
Totalframe = Weekendframe[['Startweekend', 'Offset', 'Nightflight', 'Crewmember']]
Totalframe.columns = ['Startduty', 'Offset', 'Nightflight', 'Crewmember']
Totalframe = pd.concat([Dutyframe[['Startduty', 'Offset', 'Nightflight', 'Crewmember']], Totalframe])
print(Totalframe)
dict_gantt = Totalframe.groupby('Crewmember')['Startduty', 'Offset'] \
    .apply(lambda x: list(zip(x['Startduty'].tolist(),
                              x['Offset'].tolist()))) \
    .to_dict()



# Making Gantt figure
FltReg_list = sorted(dict_gantt)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

start_datetime = Dutyframe['Startduty'].min()
end_datetime = Dutyframe['Newstart'].max()

# parameters for yticks, etc.
# you might have to play around
# with the different parts to modify
n = len(FltReg_list)
bar_size = 9
default_color = 'blue'
colors_dict = defaultdict(lambda: default_color, DAY='green', NIGHT='red', Weekend='blue', Preweekend='blue')

for i, bar in enumerate(FltReg_list):
    mask = Totalframe.Crewmember == bar
    ax.broken_barh(dict_gantt[bar],  # data
                   (10 * (i + 1), bar_size),  # (y position, bar size)
                   alpha=0.75,
                   facecolors=[colors_dict[event] for event in Totalframe.loc[mask].Nightflight],
                   edgecolor='k',
                   linewidth=1.2)



# I got date formatting ideas from
# https://matplotlib.org/examples/pylab_examples/finance_demo.html
ax.set_xlim(start_datetime, end_datetime)
ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 24)))  # HourLocator(byhour=range(0, 24, 6))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=range(0, 24, 1)))
# omitting minor labels ...

# plt.grid(b=True, which='minor', color='r', linestyle='solid')

ax.set_yticks([5 + 10 * n for n in range(1, n + 1)])
ax.set_ylim(5, 5 + 10 * (n + 1))
ax.set_yticklabels(FltReg_list)

ax.set_title('Roster')
ax.set_ylabel('Task Sort')

plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')

plt.tight_layout()
fig.show('gantt.png')
fig.canvas._master.wait_window()