import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys
from matplotlib import colors
from collections import defaultdict
import pickle

Dutyframe = pd.read_excel(
    'C:\\Users\\u03mvo\\OneDrive - TRANSAVIA AIRLINES C.V\\Documents\\ZENZ export\\Flight data summer17.xlsx')
Dutyframe = Dutyframe[Dutyframe['meldstation'] == 'AMS']
Dutyframe = Dutyframe[(Dutyframe['date'] >= 20170522) & (Dutyframe['date'] <= 20170604)]
Dutyframe['CI hhmm'][Dutyframe['CI hhmm'].astype(str).str.len() == 3] = str(0) + Dutyframe['CI hhmm'].astype(str)
Dutyframe['CO hhmm'][Dutyframe['CO hhmm'].astype(str).str.len() == 1] = str(000) + Dutyframe['CO hhmm'].astype(str)
Dutyframe['CO hhmm'][Dutyframe['CO hhmm'].astype(str).str.len() == 2] = str(00) + Dutyframe['CO hhmm'].astype(str)
Dutyframe['CO hhmm'][Dutyframe['CO hhmm'].astype(str).str.len() == 3] = str(0) + Dutyframe['CO hhmm'].astype(str)

Dutyframe['next CI time hhmm'][Dutyframe['next CI time hhmm'].astype(str).str.len() == 3] = str(0) + Dutyframe[
    'next CI time hhmm'].astype(str)
dates = Dutyframe['date'].unique()
print(dates)
Partframe2 = pd.DataFrame(columns=Dutyframe.columns)
for date in dates:
     Partframe = Dutyframe[Dutyframe['date'] == date]
     Partframe = Partframe.sample(50)
     print(Partframe)
     Partframe2 = pd.concat([Partframe2, Partframe])
# print(Partframe2)
Dutyframe = Partframe2
Dutyframe['Startduty'] = Dutyframe['date'].astype(str) + Dutyframe['CI hhmm'].astype(str)
Dutyframe['Endduty'] = Dutyframe['date'].astype(str) + Dutyframe['CO hhmm'].astype(str)
Dutyframe['Newstart'] = Dutyframe['next CI date'].astype(str) + Dutyframe['next CI time hhmm'].astype(str)
Dutyframe['Startduty'] = pd.to_datetime(Dutyframe['Startduty'])
Dutyframe['Newstart'] = pd.to_datetime(Dutyframe['Newstart'])
Dutyframe['Endduty'] = pd.to_datetime(Dutyframe['Endduty'])
print(Dutyframe['Endduty'])
Dutyframe['Endduty'][Dutyframe['days'] == 1] = Dutyframe['Endduty'] + pd.Timedelta(1, unit='d')
Dutyframe['Endduty'][Dutyframe['days'] == 2] = Dutyframe['Endduty'] + pd.Timedelta(2, unit='d')
print(Dutyframe['Endduty'])
Dutyframe['Nightflight'] = Dutyframe['night flight']
Dutyframe['minrest'] = Dutyframe['min rest']
# Dutyframe['Startduty']=pd.to_datetime(Dutyframe['date'], format='%Y%M%d')+pd.to_datetime(Dutyframe['CI hhmm'], format='%H%M' )
# print(Dutyframe['Startduty'])
Dutyframe = Dutyframe.sort_values(['Startduty'])
Dutyframe['length'] = list(range(0, len(Dutyframe)))
Dutyframe = Dutyframe.set_index(['length'])
emptyweekendframe = pd.DataFrame(columns=['Startweekend', 'Endweekend', 'Nightflight', 'Crewmember'])
emptyweekendframe['Startweekend'] = pd.to_datetime(emptyweekendframe['Startweekend'])
emptyweekendframe['Endweekend'] = pd.to_datetime(emptyweekendframe['Endweekend'])

crewlist = pd.Series(data=pd.Timestamp(2017, 5, 22, 1, 00), index=range(1, 130))
## Add when Free time should be added before beginning of duties
Preweekendframe = pd.DataFrame(columns=['Startduty', 'Offset', 'Nightflight', 'Crewmember'])
# 4*round((29-i)/29)
for i in range(1, 130):
    Preweekendframe = Preweekendframe.append(
        pd.DataFrame({'Startduty': [Dutyframe['Startduty'].iloc[0] - pd.Timedelta(0, unit='d')],
                      'Offset': [0],
                      'Nightflight': ['Preweekend'],
                      'Crewmember': [i]}))
    crewlist.ix[i] = Preweekendframe['Startduty'].iloc[-1] + pd.Timedelta(0, unit='d')

Dutyframe['Crewmember'] = 0
Dutyframe['Idlebeforeduty'] = 0
Dutyframe['Idlebeforedutyweekend'] = 0
print(crewlist)
crewlist = pd.to_datetime(crewlist)
print(crewlist)
for index, row in Dutyframe.iterrows():
    availablecrew = crewlist[(crewlist <= Dutyframe.loc[index, 'Startduty'])]
    print(Dutyframe.loc[index, ['Newstart']])
    print(availablecrew)
    if len(availablecrew) != 0:
        Dutyframe.loc[index, ['Crewmember']] = availablecrew.argmax()
        if availablecrew.max() != Dutyframe.loc[0 ,'Startduty' ]:
            Dutyframe.loc[index, 'Idlebeforeduty'] = mdates.date2num(Dutyframe.loc[index, 'Startduty']) - mdates.date2num(
            availablecrew.max())
            Tempoframe = Dutyframe[Dutyframe['Crewmember'] == Dutyframe.loc[index, 'Crewmember']]
            jobindex = Tempoframe.index[Tempoframe.index.get_loc(index) - 1]
            if Tempoframe.loc[jobindex, 'Nightflight'] == 'DAY':
                endlastdutyforweekend = Dutyframe.loc[jobindex, 'Endduty']
                if endlastdutyforweekend.hour != 0:
                    Startweekend = (endlastdutyforweekend + pd.Timedelta(1, unit='d')).replace(hour=1, minute=0)
                    Dutyframe.loc[index, 'Idlebeforedutyweekend'] = mdates.date2num(
                        Dutyframe.loc[index, 'Startduty']) - mdates.date2num(Startweekend)
                else:
                    Startweekend = (endlastdutyforweekend).replace(hour=1, minute=0)
                    Dutyframe.loc[index, 'Idlebeforedutyweekend'] = mdates.date2num(
                        Dutyframe.loc[index, 'Startduty']) - mdates.date2num(Startweekend)
            else:
                Startweekend = Tempoframe.loc[jobindex, 'Endduty'].ceil('H') + pd.Timedelta(
                    Tempoframe.loc[jobindex, 'minrest'], unit='m')
                Dutyframe.loc[index, 'Idlebeforedutyweekend'] = mdates.date2num(
                    Dutyframe.loc[index, 'Startduty']) - mdates.date2num(Startweekend)
            if len(emptyweekendframe['Startweekend'][emptyweekendframe['Crewmember'] == Dutyframe.loc[index, 'Crewmember']])!=0:
                if Tempoframe.loc[jobindex, 'Startduty'] < emptyweekendframe['Startweekend'][emptyweekendframe['Crewmember'] == Dutyframe.loc[index, 'Crewmember']].iloc[0]:
                    Dutyframe.loc[index, 'Idlebeforedutyweekend']=Dutyframe.loc[index, 'Idlebeforeduty']
        else:
            Dutyframe.loc[index, ['Idlebeforeduty']]=0
        crewlist.ix[availablecrew.argmax()] = Dutyframe.loc[index, 'Newstart']
        print('hoir', crewlist.ix[availablecrew.argmax()])
        print(mdates.date2num(Dutyframe['Newstart'][Dutyframe['Crewmember'] == availablecrew.argmax()])[-1])
        if (mdates.date2num(Dutyframe['Newstart'][Dutyframe['Crewmember'] == availablecrew.argmax()])[-1] -
            mdates.date2num(Dutyframe['Startduty'][Dutyframe['Crewmember'] == availablecrew.argmax()])[0] > 4) and len(
                emptyweekendframe[emptyweekendframe['Crewmember'] == availablecrew.argmax()]) == 0:
            print(Dutyframe[Dutyframe['Crewmember'] == availablecrew.argmax()])
            if Dutyframe['Nightflight'][Dutyframe['Crewmember'] == availablecrew.argmax()].iloc[-1] == 'DAY':
                endlastdutyforweekend = Dutyframe['Endduty'][Dutyframe['Crewmember'] == availablecrew.argmax()].iloc[-1]
                if endlastdutyforweekend.hour != 0:
                    Startweekend = (endlastdutyforweekend + pd.Timedelta(1, unit='d')).replace(hour=1, minute=0)
                else:
                    Startweekend = (endlastdutyforweekend).replace(hour=1, minute=0)
                temporaryweekendframe = pd.DataFrame({'Startweekend': [Startweekend],
                                                      'Endweekend': [Startweekend + pd.Timedelta(3, unit='d')],
                                                      'Weekendsort': [Startweekend.hour],
                                                      'Crewmember': [Dutyframe['Crewmember'][Dutyframe[
                                                                                                 'Crewmember'] == availablecrew.argmax()].iloc[
                                                                         -1]]})
            else:
                print(Dutyframe[Dutyframe['Crewmember'] == availablecrew.argmax()])
                temporaryweekendframe = pd.DataFrame({'Startweekend': [
                    Dutyframe['Endduty'][Dutyframe['Crewmember'] == availablecrew.argmax()].dt.ceil('H').iloc[
                        -1] + pd.Timedelta(
                        Dutyframe['minrest'][Dutyframe['Crewmember'] == availablecrew.argmax()].iloc[-1], unit='m')],
                                                      'Endweekend': [Dutyframe['Endduty'][Dutyframe[
                                                                                              'Crewmember'] == availablecrew.argmax()].dt.ceil(
                                                          'H').iloc[-1] + pd.Timedelta(Dutyframe['minrest'][Dutyframe[
                                                                                                                'Crewmember'] == availablecrew.argmax()].iloc[
                                                                                           -1],
                                                                                       unit='m') + pd.Timedelta(3,
                                                                                                                unit='d')],
                                                      'Weekendsort': [(Dutyframe['Endduty'][Dutyframe[
                                                                                                'Crewmember'] == availablecrew.argmax()].dt.ceil(
                                                          'H').iloc[-1] + pd.Timedelta(Dutyframe['minrest'][Dutyframe[
                                                                                                                'Crewmember'] == availablecrew.argmax()].iloc[
                                                                                           -1], unit='m')).hour],
                                                      'Crewmember': [Dutyframe['Crewmember'][Dutyframe[
                                                                                                 'Crewmember'] == availablecrew.argmax()].iloc[
                                                                         -1]]})
            crewlist.ix[availablecrew.argmax()] = temporaryweekendframe.loc[0, 'Endweekend']

            emptyweekendframe = pd.concat([emptyweekendframe, temporaryweekendframe])
    else:
        crewlist = crewlist.append(pd.Series(crewlist.iloc[-1] + 1))
        Dutyframe.loc[index, ['Crewmember']] = crewlist.iloc[-1]
print(emptyweekendframe)
print(Dutyframe)

for crewmember in crewlist.index:
    Dutyframecrew = Dutyframe[Dutyframe['Crewmember'] == crewmember]
    totidle = Dutyframecrew['Idlebeforeduty'].sum()
    print(crewmember, totidle)

Dutyframe['Nightflight'] = Dutyframe['night flight']
Dutyframe['Offset'] = Dutyframe['Newstart'].apply(mdates.date2num) - Dutyframe['Startduty'].apply(mdates.date2num)
Dutyframe['Startduty'] = Dutyframe['Startduty'].apply(mdates.date2num)
emptyweekendframe['Startweekend'] = emptyweekendframe['Startweekend'].apply(mdates.date2num)
emptyweekendframe['Offset'] = 3
emptyweekendframe['Nightflight'] = 'Weekend'
Totalframe = emptyweekendframe[['Startweekend', 'Offset', 'Nightflight', 'Crewmember']]
Totalframe.columns = ['Startduty', 'Offset', 'Nightflight', 'Crewmember']
Totalframe = pd.concat([Dutyframe[['Startduty', 'Offset', 'Nightflight', 'Crewmember']], Totalframe])
Preweekendframe['Startduty'] = Preweekendframe['Startduty'].apply(mdates.date2num)
Weekendframe=pd.concat([emptyweekendframe, Preweekendframe])
Totalframe = pd.concat([Totalframe, Preweekendframe])

print(Totalframe)
print(Dutyframe)
print(Weekendframe)
write_loc ='C:\\Users\\u03mvo\\OneDrive - TRANSAVIA AIRLINES C.V\\Documents\\Pythonexports\\Naivescheduling\\'
Totalframe.to_pickle(write_loc+ 'Totalframe18-6s50long')
Dutyframe.to_pickle(write_loc+ 'Dutyframe18-6s50long')
Weekendframe.to_pickle(write_loc+ 'Weekendframe18-6s50long')
print(Dutyframe['Idlebeforeduty'])
print(Dutyframe['Idlebeforedutyweekend'])
sys.exit()
