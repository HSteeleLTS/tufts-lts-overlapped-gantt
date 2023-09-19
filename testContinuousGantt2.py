import pandas as pd
import matplotlib.pyplot as plt

fig, gnt = plt.subplots()

df = pd.DataFrame([dict(Task="Task1", Start='2017-01-01', Finish='2017-02-15', Phase ='Phase1', Height=0.5),
      dict(Task="Task1", Start='2017-02-15', Finish='2017-03-15', Phase ='Phase2', Height=0.5),
      dict(Task="Task2", Start='2017-01-17', Finish='2017-02-17', Phase ='Phase2', Height=0.2),
      dict(Task="Task2", Start='2017-02-18', Finish='2017-03-17', Phase ='Phase3', Height=0.2),
      dict(Task="Task3", Start='2017-03-10', Finish='2017-03-31', Phase ='Phase1', Height=0.9),
      dict(Task="Task3", Start='2017-04-01', Finish='2017-05-20', Phase ='Phase2', Height=0.9),
      dict(Task="Task3", Start='2017-05-18', Finish='2017-06-18', Phase ='Phase3', Height=0.9),
      dict(Task="Task4", Start='2017-01-14', Finish='2017-03-14', Phase ='Phase4', Height=0.4)])

df['Start']= pd.to_datetime(df['Start'])
df['Finish']= pd.to_datetime(df['Finish'])

colors = pd.DataFrame([('Phase1', 'tab:brown', 0), ('Phase2', 'tab:blue', 0),
                       ('Phase3', 'tab:orange', 0),('Phase4', 'tab:green', 0)],
                      columns = ['Phase', 'Color', 'LegendUse'])

bar_height = pd.DataFrame([('Task1', 0.5), ('Task2', 0.2), ('Task3', 0.9), ('Task4', 0.4)],
                          columns = ['Task', 'Height'])

for i in df.index:
    if colors.loc[colors['Phase'] == df.Phase[i], 'LegendUse'].iloc[0] == 0:
        colors.loc[colors['Phase'] == df.Phase[i], 'LegendUse'] = 1
        prefix = ''
    else:
        prefix = '_'
    thisbar = float(bar_height.loc[bar_height.Task == df.Task[i]].Height)
    thisYaxis = int(bar_height.loc[bar_height.Task == df.Task[i]].index[0])
    thiscolor = colors.loc[colors['Phase'] == df.Phase[i], 'Color'].iloc[0]
    gnt.broken_barh([(df.Start[i], (df.Finish[i] - df.Start[i]))], (thisYaxis, thisbar),
                    facecolors=(thiscolor), label = prefix+df.Phase[i])

plt.legend(loc='upper left', bbox_to_anchor=(1.01, 1))

gnt.axes.get_yaxis().set_ticks([])
gnt.set_xticklabels(pd.date_range(start="2017-01-01",end="2017-07-01",freq = 'M').strftime('%b %Y'))

fig.set_figheight(4)
fig.set_figwidth(15)
fig.show()
plt.show(block=True)
