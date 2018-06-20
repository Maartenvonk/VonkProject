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
Totalframe = pd.read_pickle(filefolder + 'Totalframe6-6s50')
Dutyframe = pd.read_pickle(filefolder + 'Dutyframe6-6s50')
Weekendframe = pd.read_pickle(filefolder + 'Weekendframe6-6s50')
print(Dutyframe)
print(len(Dutyframe))
def idlecosts(duty1end,duty2start):
    if duty2start-mdates.date2num(duty1end)>=0:
        idletime = duty2start-mdates.date2num(duty1end)
    else:
        idletime=10000
    return idletime


crewmembers=90
crewlist=[]
for i in range(1,crewmembers+1):
    crewlist.append('C'+str(i))

#Create Nodes
nodes=[]
nodes.append('Start')
nodes.append('Sink')
for i in crewlist:
    nodes.append(i)
for i in range(1,2*len(Dutyframe)+1):
    nodes.append(i)
print(nodes)

# supply or demand of nodes
            #NodeID : [Supply,Demand]
# Start with Start and Sink node
nodeData = {'Start':[crewmembers,0],
            'Sink':[0,crewmembers]}
#Add Crewmembers as nodes
for i in crewlist:
    nodeData[i]=[0,0]
#Add all the flights 2 times as nodes
for i in range(1,2*len(Dutyframe)+1):
    nodeData[i] = [0,0]
print(nodeData)
# Include a Dataframe with the Idle time between flights in matrix form
z= [[0 for x in range(len(Dutyframe))] for y in range(len(Dutyframe))]
for i in range(len(Dutyframe)):
   for j in range(len(Dutyframe)):
      z[i][j] = idlecosts(Dutyframe.loc[i,'Newstart'],Dutyframe.loc[j,'Startduty'])
print(z)
# arcs list
arcs= []

#Add arcs from all second flight nodes to first flight nodes which are sequential in time
for i in range(len(Dutyframe)):
    for j in range(len(Dutyframe)):
        if z[i][j]<10000:
            arcs.append((2*i+2,2*j+1))

print(len(arcs))
for i in crewlist:
    # Add arcs between Start and Crew nodes
    arcs.append(('Start',i))
    for j in range(len(Dutyframe)):
        #Add arcs between Crew nodes and flight nodes
        arcs.append((i,2*j+1))
for j in range(len(Dutyframe)):
    #Add arcs between first flight nodes and second flight nodes
    arcs.append((2*j+1,2*j+2))
    #Add arcs from all second flight nodes to Sink node
    arcs.append((2*j+2,'Sink'))


# arcs cost, lower bound and capacity
            #Arc : [Cost,MinFlow,MaxFlow]
arcData={}
for i in range(len(Dutyframe)):
    for j in range(len(Dutyframe)):
        if z[i][j]<10000:
            arcData[(2*i+2,2*j+1)]=[z[i][j],0,1]
print(len(arcData))
for i in crewlist:
    arcData[('Start',i)]=[0,1,1]
    for j in range(len(Dutyframe)):
        arcData[(i,2*j+1)]=[0,0,1]
        arcData[(2*j+1,2*j+2)]=[0,1,1]
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

# The problem data is written to an .lp file
prob.writeLP("simple_MCFP.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The optimised objective function value is printed to the screen
print("Total Cost of Transportation = ", value(prob.objective))
print(pulp.LpStatus[prob.status])
output = []
#print(len(arcs))
#arcs=arcs[vars[arcs].varValue==1]
print(len(arcs))
for arc in arcs:
    if vars[arc].varValue==0:
        arcs.remove(arc)
print(len(arcs))
print(arcs)
#Create Dataframe with all arcs and flow value
for (i, j) in arcs:
    var_output = {
    'Nodefrom': i,
    'Nodeto': j,
    'Flow': vars[(i, j)].varValue,
    }
    output.append(var_output)
df = pd.DataFrame.from_records(output)
print(df)

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
    df2=df[df['Nodefrom']==crew]
    index1=df['Nodeto'][(df['Nodefrom']==crew) & (df['Flow']==1)].iloc[0]
    indexlist.append(index1)
    while df['Nodeto'][(df['Nodefrom']==index1+1) & (df['Flow']==1)].iloc[0]!='Sink':
        index1 = df['Nodeto'][(df['Nodefrom']==index1+1) & (df['Flow']==1)].iloc[0]
        indexlist.append(index1)
    indexlist=np.array(indexlist)
    indexlist=(indexlist-1)/2
    Dutyframe['Crewmember'][indexlist]=crew



# Creating figure based on Dutyframe
dict_gantt = Dutyframe.groupby('Crewmember')['Startduty', 'Offset'] \
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
    mask = Dutyframe.Crewmember == bar
    ax.broken_barh(dict_gantt[bar],  # data
                   (10 * (i + 1), bar_size),  # (y position, bar size)
                   alpha=0.75,
                   facecolors=[colors_dict[event] for event in Dutyframe.loc[mask].Nightflight],
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
sys.exit()