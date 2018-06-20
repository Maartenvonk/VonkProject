import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys
from matplotlib import colors
from collections import defaultdict
import pickle
import networkx as nx

filefolder='C:\\Users\\u03mvo\\OneDrive - TRANSAVIA AIRLINES C.V\\Documents\\Pythonexports\\Naivescheduling\\'
Totalframe = pd.read_pickle(filefolder + 'Totalframe6-6s10')
Dutyframe = pd.read_pickle(filefolder + 'Dutyframe6-6s10')
Weekendframe = pd.read_pickle(filefolder + 'Weekendframe6-6s10')
print(Dutyframe)
print(len(Dutyframe))
def idlecosts(duty1end,duty2start):
    if duty2start-mdates.date2num(duty1end)>=0:
        idletime = duty2start-mdates.date2num(duty1end)
    else:
        idletime=10000
    return idletime

z= [[0 for x in range(len(Dutyframe))] for y in range(len(Dutyframe))]
for i in range(len(Dutyframe)):
   for j in range(len(Dutyframe)):
      z[i][j] = idlecosts(Dutyframe.loc[i,'Newstart'],Dutyframe.loc[j,'Startduty'])

crewmembers=15
crewlist=[]
for i in range(1,crewmembers+1):
    crewlist.append('C'+str(i))

x = range(len(Dutyframe))
G = nx.DiGraph()
G.add_node('Start', demand=-crewmembers)
G.add_nodes_from(crewlist)
G.add_node('Sink', demand= crewmembers)

for crew in crewlist:
    G.add_edge('Start', crew, weight = 0, capacity = 1)

G.add_nodes_from(range(0,2*len(Dutyframe)))

for i in range(len(Dutyframe)):
    for crew in crewlist:
        G.add_edge(crew, i, weight=0, capacity=1)
    G.add_edge(i+len(Dutyframe), 'Sink', weight=0, capacity=1)
    G.add_edge(i, i+len(Dutyframe), weight=-10000, capacity=1)
    for j in range(len(Dutyframe)):
        if j>i and z[i][j]<10000:
            G.add_edge(i+len(Dutyframe), j, weight = z[i][j], capacity = 1)

# edge_colours = ['black'
#                 for edge in G.edges()]
# black_edges = [edge for edge in G.edges()]
# pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 100)
# nx.draw_networkx_labels(G, pos)
# nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
flowCost, flowDict = nx.capacity_scaling(G)

df=pd.DataFrame.from_dict(flowDict)
print(df.index)
print(flowCost+len(Dutyframe)*10000)
plt.show()

for crew in crewlist:
    indexlist=[]
    index1=df[df[crew]==1].index[0]
    indexlist.append(index1)
    while df[df[index1+len(Dutyframe)] == 1].index[0]!='Sink':
        index1 = df[df[index1+len(Dutyframe)] == 1].index[0]
        indexlist.append(index1)
    Dutyframe['Crewmember'][indexlist]=crew


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