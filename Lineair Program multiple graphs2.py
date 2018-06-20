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
import datetime as dt
import time
start_time = time.time()

filefolder='C:\\Users\\u03mvo\\OneDrive - TRANSAVIA AIRLINES C.V\\Documents\\Pythonexports\\Naivescheduling\\'
Dutyframe = pd.read_pickle(filefolder + 'Dutyframe18-6s50long')

def idlecosts(duty1end,duty2start, duty1start, duty2end):
    if duty2start-mdates.date2num(duty1end)>=0:
        idletime = duty2start-mdates.date2num(duty1end)
    else:
        idletime=10000
        #maximizing early/late duties changes
    if (mdates.num2date(duty1start).hour<6) & (0<duty2end.hour<6):
        idletime=10000
    return idletime
def idlecostweekend(duty1end, Nightflight1, Rest1, duty2start):
    if Nightflight1=='NIGHT':
        if duty2start-(mdates.date2num(duty1end)+Rest1)>3:
            idleweekendtime= duty2start-(mdates.date2num(duty1end)+Rest1)
        else:
            idleweekendtime=10000
    else:
        if duty1end.hour != 0:
            Startweekend = (duty1end + pd.Timedelta(1, unit='d')).replace(hour=1, minute=0)
            if duty2start - mdates.date2num(Startweekend) > 3:
                idleweekendtime = duty2start - mdates.date2num(duty1end)
            else:
                idleweekendtime=10000
        else:
            Startweekend = (duty1end).replace(hour=1, minute=0)
            if duty2start - mdates.date2num(Startweekend) > 3:
                idleweekendtime = duty2start - mdates.date2num(duty1end)
            else:
                idleweekendtime=10000
    return idleweekendtime

z2= [[0 for x in range(len(Dutyframe))] for y in range(len(Dutyframe))]
for i in range(len(Dutyframe)):
   for j in range(len(Dutyframe)):
       z2[i][j] = idlecostweekend(Dutyframe.loc[i,'Endduty'],Dutyframe.loc[i,'Nightflight'],Dutyframe.loc[i,'minrest']/1440,Dutyframe.loc[j,'Startduty'])



crewmembers=115
crewlist=[]
for i in range(1,crewmembers+1):
    crewlist.append('C'+str(i))

#Create Nodes
nodes=[]
nodes.append('Start')
nodes.append('Sink')
for i in crewlist:
    nodes.append(i)
for i in range(1,8*len(Dutyframe)+1):
    nodes.append(i)

# supply or demand of nodes
            #NodeID : [Supply,Demand]
# Start with Start and Sink node
nodeData = {'Start':[crewmembers,0],
            'Sink':[0,crewmembers]}
#Add Crewmembers as nodes
for i in crewlist:
    nodeData[i]=[0,0]
#Add all the flights 2 times as nodes
for i in range(1,8*len(Dutyframe)+1):
    nodeData[i] = [0,0]
print(nodeData)
# Include a Dataframe with the Idle time between flights in matrix form
z= [[0 for x in range(len(Dutyframe))] for y in range(len(Dutyframe))]
for i in range(len(Dutyframe)):
   for j in range(len(Dutyframe)):
      z[i][j] = idlecosts(Dutyframe.loc[i,'Newstart'],Dutyframe.loc[j,'Startduty'],Dutyframe.loc[i,'Startduty'],Dutyframe.loc[j,'Endduty'])
# arcs list
arcs= []

#Add arcs from all second flight nodes to first flight nodes which are sequential in time
for i in range(len(Dutyframe)):
    for j in range(len(Dutyframe)):
        if (z[i][j]<10000) & (mdates.date2num(pd.to_datetime(mdates.num2date(Dutyframe.loc[j,'Startduty']).strftime('%Y-%m-%d')))-mdates.date2num(pd.to_datetime((mdates.num2date(Dutyframe.loc[i,'Startduty']).strftime('%Y-%m-%d'))))==1):
            arcs.append((2*i+2,2*j+1+2*len(Dutyframe)))
            arcs.append((2*i+2+2*len(Dutyframe),2*j+1+4*len(Dutyframe)))
            arcs.append((2*i+2+4*len(Dutyframe),2*j+1+6*len(Dutyframe)))
        if (z[i][j]<10000) & (mdates.date2num(pd.to_datetime(mdates.num2date(Dutyframe.loc[i,'Startduty']).strftime('%Y-%m-%d')))-mdates.date2num(pd.to_datetime((mdates.num2date(Dutyframe.loc[j,'Startduty']).strftime('%Y-%m-%d'))))==2):
            arcs.append((2*i+2,2*j+1+4*len(Dutyframe)))
            arcs.append((2*i+2+2*len(Dutyframe),2*j+1+6*len(Dutyframe)))
        if (z[i][j]<10000) & (mdates.date2num(pd.to_datetime(mdates.num2date(Dutyframe.loc[i,'Startduty']).strftime('%Y-%m-%d')))-mdates.date2num(pd.to_datetime((mdates.num2date(Dutyframe.loc[j,'Startduty']).strftime('%Y-%m-%d'))))==3):
            arcs.append((2*i+2,2*j+1+6*len(Dutyframe)))
        if z2[i][j]<10000:
            arcs.append((2*i+2+6*len(Dutyframe), 2*j+1))


for i in crewlist:
    # Add arcs between Start and Crew nodes
    arcs.append(('Start',i))
    for j in range(4*len(Dutyframe)):
        #Add arcs between Crew nodes and flight nodes
        arcs.append((i,2*j+1))
for j in range(4*len(Dutyframe)):
    #Add arcs between first flight nodes and second flight nodes
    arcs.append((2*j+1,2*j+2))
    #Add arcs from all second flight nodes to Sink node
    arcs.append((2*j+2,'Sink'))


# arcs cost, lower bound and capacity
            #Arc : [Cost,MinFlow,MaxFlow]
arcData={}
for i in range(len(Dutyframe)):
    for j in range(len(Dutyframe)):
        if (z[i][j]<10000) & (mdates.date2num(pd.to_datetime(mdates.num2date(Dutyframe.loc[j,'Startduty']).strftime('%Y-%m-%d')))-mdates.date2num(pd.to_datetime((mdates.num2date(Dutyframe.loc[i,'Startduty']).strftime('%Y-%m-%d'))))==1) :
            arcData[(2*i+2,2*j+1+2*len(Dutyframe))]=[z[i][j],0,1]
            arcData[(2*i+2+2*len(Dutyframe),2*j+1+4*len(Dutyframe))]=[z[i][j],0,1]
            arcData[(2*i+2+4*len(Dutyframe),2*j+1+6*len(Dutyframe))]=[z[i][j],0,1]
        if (z[i][j]<10000) & (mdates.date2num(pd.to_datetime(mdates.num2date(Dutyframe.loc[i,'Startduty']).strftime('%Y-%m-%d')))-mdates.date2num(pd.to_datetime((mdates.num2date(Dutyframe.loc[j,'Startduty']).strftime('%Y-%m-%d'))))==2):
            arcData[(2*i+2,2*j+1+4*len(Dutyframe))]=[z[i][j],0,1]
            arcData[((2*i+2+2*len(Dutyframe),2*j+1+6*len(Dutyframe)))]=[z[i][j],0,1]
        if (z[i][j]<10000) & (mdates.date2num(pd.to_datetime(mdates.num2date(Dutyframe.loc[i,'Startduty']).strftime('%Y-%m-%d')))-mdates.date2num(pd.to_datetime((mdates.num2date(Dutyframe.loc[j,'Startduty']).strftime('%Y-%m-%d'))))==3):
            arcData[(2*i+2,2*j+1+6*len(Dutyframe))] = [z[i][j], 0, 1]
        if z2[i][j]<10000:
            arcData[(2*i+2+6*len(Dutyframe), 2*j+1)] = [z2[i][j], 0, 1]


for i in crewlist:
    arcData[('Start',i)]=[0,1,1]
    for j in range(4*len(Dutyframe)):
        arcData[(i,2*j+1)]=[0,0,1]
        arcData[(2*j+1,2*j+2)]=[0,0,1]
        arcData[(2*j+2,'Sink')]=[0,0,1]

# Splits the dictionaries to be more understandable
(supply, demand) = splitDict(nodeData)
(costs, mins, maxs) = splitDict(arcData)
print(costs)
# Creates the boundless Variables as Integers
vars = LpVariable.dicts("Route", arcs, None, None, LpInteger)

# Creates the upper and lower bounds on the variables
for a in arcs:
    vars[a].bounds(mins[a], maxs[a])

# Creates the 'prob' variable to contain the problem data
prob = LpProblem("Minimum Cost Flow Problem Sample", LpMinimize)

# Creates the objective function
prob += lpSum([vars[a] * costs[a] for a in arcs]), "Total Cost of Transport"

# Creates all problem constraints - this ensures the amount going into each node is
# at least equal to the amount leaving
for n in nodes:
    prob += (supply[n] + lpSum([vars[(i, j)] for (i, j) in arcs if j == n]) >=
             demand[n] + lpSum([vars[(i, j)] for (i, j) in arcs if i == n])), \
            "Flow Conservation in Node %s" % n

for j in range(len(Dutyframe)):
    prob +=(lpSum([vars[(2*j+1, 2*j+2)]+vars[(2*j+1+2*len(Dutyframe), 2*j+2+2*len(Dutyframe))]+vars[(2*j+1+4*len(Dutyframe), 2*j+2+4*len(Dutyframe))]+vars[(2*j+1+6*len(Dutyframe), 2*j+2+6*len(Dutyframe))]]) >= 1)
    prob += (lpSum([vars[(2 * j + 1, 2 * j + 2)] + vars[
        (2 * j + 1 + 2 * len(Dutyframe), 2 * j + 2 + 2 * len(Dutyframe))] + vars[
                        (2 * j + 1 + 4 * len(Dutyframe), 2 * j + 2 + 4 * len(Dutyframe))] + vars[
                        (2 * j + 1 + 6 * len(Dutyframe), 2 * j + 2 + 6 * len(Dutyframe))]]) <= 1)

# The problem data is written to an .lp file
prob.writeLP("simple_MCFP.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The optimised objective function value is printed to the screen
print("Total Idle time = ", value(prob.objective))
print("Time elapsed: {:.2f}s".format(time.time() - start_time))
print(pulp.LpStatus[prob.status])
output = []
#print(len(arcs))
#arcs=arcs[vars[arcs].varValue==1]

for arc in arcs:
    if vars[arc].varValue==0:
        arcs.remove(arc)

#Create Dataframe with all arcs and flow value
for (i, j) in arcs:
    var_output = {
    'Nodefrom': i,
    'Nodeto': j,
    'Flow': vars[(i, j)].varValue,
    }
    output.append(var_output)
df = pd.DataFrame.from_records(output)



#Flowdata is the dataframe containing all sending nodes as columns and receiving nodes as rows with values 1 if there
# is a flow from sending to receiving node and 0 otherwise
#Flowdata = pd.DataFrame(columns=df.Nodefrom.unique(), index=df.Nodeto.unique())
#df.set_index(['Flow'], inplace=True)
#for (i,j) in arcs:
#    Flowdata.loc[j,i]=df.Flow[(i,j)]
#print(Flowdata.C1)

# This loop allocates the crew members to duties in Dutyframe based on Flowdata frame
for crew in crewlist:
    indexlist=[]
    index1=df['Nodeto'][(df['Nodefrom']==crew) & (df['Flow']==1)].iloc[0]
    indexlist.append(index1)
    while df['Nodeto'][(df['Nodefrom']==index1+1) & (df['Flow']==1)].iloc[0]!='Sink':
        index1 = df['Nodeto'][(df['Nodefrom']==index1+1) & (df['Flow']==1)].iloc[0]
        indexlist.append(index1)
    indexlist=np.array(indexlist)
    indexlist=((indexlist-1)/2)%(len(Dutyframe))
    Dutyframe['Crewmember'][indexlist]=crew


#Create weekendframe
Weekendframe = pd.DataFrame(columns=['Startduty', 'Offset', 'Nightflight', 'Crewmember'])
for i in range(len(Dutyframe)):
    for j in range(len(Dutyframe)):
        if z2[i][j]<10000:
            if vars[(2*i+2+6*len(Dutyframe), 2*j+1)].varValue>0:
                if Dutyframe.loc[i, 'Nightflight'] == 'DAY':
                    endlastdutyforweekend = Dutyframe.loc[i, 'Endduty']
                    if endlastdutyforweekend.hour != 0:
                        Startweekend = (endlastdutyforweekend + pd.Timedelta(1, unit='d')).replace(hour=1, minute=0)
                    else:
                        Startweekend = (endlastdutyforweekend).replace(hour=1, minute=0)
                    temporaryweekendframe = pd.DataFrame({'Startweekend': [Startweekend],
                                                          'Endweekend': [Startweekend + pd.Timedelta(3, unit='d')],
                                                          'Weekendsort': [Startweekend.hour],
                                                          'Crewmember': [Dutyframe.loc[i, 'Crewmember']]})
                else:
                    temporaryweekendframe = pd.DataFrame({'Startweekend': [
                        Dutyframe.loc[i, 'Endduty'].ceil('H') + pd.Timedelta(
                            Dutyframe.loc[i, 'minrest'], unit='m')],
                        'Endweekend': [Dutyframe.loc[i, 'Endduty'].ceil(
                            'H') + pd.Timedelta(Dutyframe.loc[i, 'minrest'],
                                                         unit='m') + pd.Timedelta(3,
                                                                                  unit='d')],
                        'Weekendsort': [(Dutyframe.loc[i, 'Endduty'].ceil(
                            'H') + pd.Timedelta(Dutyframe.loc[i, 'minrest'], unit='m')).hour],
                        'Crewmember': [Dutyframe.loc[i, 'Crewmember']]})
                Dutyframe.loc[i, 'Idlebeforedutyweekend'] = Dutyframe.loc[i, 'Startduty'] - mdates.date2num(
                    temporaryweekendframe['Endweekend'].iloc[0])
                Dutyframe.loc[i, 'Idlebeforeduty'] = Dutyframe.loc[i, 'Startduty'] - \
                                                         temporaryweekendframe['Endweekend'].apply(
                                                             mdates.date2num).iloc[0]
#                Weekendframe = Weekendframe[Weekendframe['Crewmember'] != Dutyframe.loc[i, 'Crewmember']]
                temporaryweekendframe['Startweekend'] = temporaryweekendframe['Startweekend'].apply(mdates.date2num)
                Weekendframe = pd.concat([Weekendframe, temporaryweekendframe])


Weekendframe['Startduty']=Weekendframe['Startweekend']
Weekendframe['Nightflight']='Weekend'
Weekendframe['Offset'] = 3
Dutyframe = pd.concat([Dutyframe, Weekendframe])
# Creating figure based on Dutyframe
dict_gantt = Dutyframe.groupby('Crewmember')['Startduty', 'Offset'] \
    .apply(lambda x: list(zip(x['Startduty'].tolist(),
                              x['Offset'].tolist()))) \
    .to_dict()

print(Dutyframe[Dutyframe['Crewmember']=='C5'])


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
    mask = Dutyframe.Crewmember == bar
    Dutyframe2=Dutyframe[(Dutyframe.Crewmember == bar) & (Dutyframe.Nightflight!= 'Weekend')]
    ax.broken_barh(dict_gantt[bar],  # data
                   (10 * (i + 1), bar_size),  # (y position, bar size)
                   alpha=0.75,
                   facecolors=[colors_dict[event] for event in Dutyframe.loc[mask].Nightflight],
                   edgecolor='k',
                   linewidth=1.2)
    for j in range(len(Dutyframe2)):
        ax.text(Dutyframe2.iloc[j].Startduty+0.2, 10 * (i + 1)+4, mdates.num2date(Dutyframe2.iloc[j].Startduty).strftime('%H:%M'),  ha='center',va='center')
#        ax.text(Dutyframe2.iloc[j].Startduty+0.5, 10 * (i + 1)+4, Dutyframe2.iloc[j].route,  ha='center',va='center')
        ax.text(mdates.date2num(Dutyframe2.iloc[j].Newstart)  -0.2, 10 * (i + 1) +4, Dutyframe2.iloc[j].Newstart.strftime('%H:%M'), ha='center', va='center')


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
sys.exit()