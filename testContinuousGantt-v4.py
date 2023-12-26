# import pandas as pd
# import plotly.express as pex
#
# d1 = dict(stack=1, start='2023-09-01', finish='2023-10-01', task='Sleep')
# d2 = dict(stack=1, start='2023-10-01', finish='2021-10-15', task='EAT')
# d3 = dict(stack=1, start='2023-09-15', finish='2023-09-30', task='Study')
# d4 = dict(stack=1, start='2023-10-10', finish='2023-10-30', task='Work')
# d5 = dict(stack=1, start='2023-10-15', finish='2023-10-30', task='EAT')
# d6 = dict(stack=1, start='2023-10-15', finish='2023-11-01', task='Study')
# d8 = dict(stack=1, start='2023-11-02', finish='2023-11-15', task='EAT')
# d7 = dict(stack=1, start='2023-11-02', finish='2023-11-15', task='Sleep')
#
# dict_list = [d1,d2,d3,d4,d5,d6,d7,d8]
# for dict in dict_list:
#
#
#
# df = pd.DataFrame([d1,d2,d3,d4,d5,d6,d7,d8])
#
# gantt = pex.timeline(df, x_start='start', x_end='finish', y='stack', color='task', height=300)
# gantt


import pandas as pd
import plotly.express as pex
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import sys
import kaleido
from datetime import datetime
from datetime import date
from itertools import cycle
from matplotlib.pyplot import cm
import numpy as np
#import plotly.graph_objects as go
#filename = askopenfilename(title="Select project sheet")

filename = "FY24 Projects DRAFT-v2.xlsx"

projects_df = pd.read_excel(filename, engine="openpyxl")

projects_df['stack'] = 0
projects_df = projects_df.sort_values(['start_date', 'end_date'])
pd.set_option('display.max_columns', None)
pd.options.display.max_colwidth = 200
print(projects_df)





min_start_date = projects_df['start_date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d")).min()

max_end_date = projects_df['end_date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d")).max()#  max_end_date = projects_df.max(pd.to_datetime('finish'))
delta = max_end_date - min_start_date
length_of_matrix = delta

delta = int(delta.total_seconds()/60/60/24)
height_of_matrix = projects_df['level_of_effort'].sum()

print("Height of matrix: " + str(height_of_matrix))

print("Width of Matrix:  " + str(delta))
rows, cols = (delta, height_of_matrix)
arr = [[0]*cols]*rows

date_range = pd.date_range(min_start_date, max_end_date)

range_list = list(reversed(list(range(0, height_of_matrix))))

for z in range(0, len(range_list)):
    
    range_list[z] = str(range_list[z])
    print (range_list[z])
    print(type(range_list[z]))



master_plotting_df = pd.DataFrame(columns=date_range, index=range_list)

master_plotting_df = master_plotting_df.applymap(lambda x: 0)


# print(master_plotting_df)

# sys.exit()

for x in range(0, len(projects_df)):


    project_plotting_df = master_plotting_df.copy()

    # print(project_plotting_df)

    
    #print(str(x) + " time through")
    for y in range(0, height_of_matrix - 1):
        #print(str(y + int(projects_df.loc[x, 'level_of_effort']) - 1))
        
        try:
            project_dates_and_effort_df = project_plotting_df.loc[str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y), projects_df.loc[x, 'start_date']: projects_df.loc[x, 'end_date']]

        except:
            break
        master_plotting_subslice_df = master_plotting_df.copy()

        master_plotting_subslice_df = master_plotting_df.loc[str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y), projects_df.loc[x, 'start_date']: projects_df.loc[x, 'end_date']].loc[str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y), projects_df.loc[x, 'start_date']: projects_df.loc[x, 'end_date']]
        


        #print(master_plotting_df.loc[str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y), projects_df.loc[x, 'start_date']: projects_df.loc[x, 'end_date']])
        #print(project_dates_and_effort_df)

        # print(project_dates_and_effort_df.equals(master_plotting_subslice_df))
        # sys.exit()
        
        

        if (project_dates_and_effort_df.equals(master_plotting_df.loc[str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y), projects_df.loc[x, 'start_date']: projects_df.loc[x, 'end_date']])):
            projects_df.iloc[x, projects_df.columns.get_loc('stack')] = y
            print("got in")
            master_plotting_df.loc[str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y), projects_df.loc[x, 'start_date']: projects_df.loc[x, 'end_date']] =  master_plotting_df.loc[str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y), projects_df.loc[x, 'start_date']: projects_df.loc[x, 'end_date']].applymap(lambda x: 1)

            #print(master_plotting_df.loc[str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y), projects_df.loc[x, 'start_date']: projects_df.loc[x, 'end_date']])

            
        
            master_plotting_df.to_excel("Plotting Dataframe for Testing - " +str(x) + ".xlsx")

            break

        
        else:
            print('miss')
        
master_plotting_df.to_excel("Plotting DataFrame.xlsx")
print(projects_df)

sys.exit()

#         print(project_dates_and_effort_df)
#         print(projects_df.iloc[x, projects_df.columns.get_loc('task')])
#         sys.exit()

#     task_dict = dict(order=x, bandwidth=0, effort=projects_df.loc[x, 'level_of_effort'], start=projects_df.loc[x, 'start_date'],
#                      finish=projects_df.loc[x, 'end_date'], task=projects_df.loc[x, 'task'])
#     data.append(task_dict)


# df = pd.DataFrame(data)




# # Adjusting stack value for overlapping events
# df = df.sort_values(by=['start', 'finish']).reset_index(drop=True)

# max_i = 0
# position = 1
# df2 = df.copy()

# def test(i=None, bandwidth_df_function=None):
#     #bandwidth_df = bandwidth_df.drop(df[df['order'] == i]['order'], axis=0)
#     #print(bandwidth_df_function)



#     bandwidth_adjustment = 0
#     #print(len(bandwidth_df_function))
#     if (len(bandwidth_df_function) != 0):
#         for j in range(0, len(bandwidth_df_function)):

#             bandwidth_current = bandwidth_df_function.loc[j, 'bandwidth'] + bandwidth_df_function.loc[j, 'effort']

#             #print("i row " + str(i) + ": " + str(df.iloc[i]))
#             #print("j row " + str(j) + ": " + str(bandwidth_df_function.iloc[j]))

#             #print("length main df:      " + str(len(df)))
#             #print("length bandwidth df: " + str(len(bandwidth_df_function)))


#             if (df.loc[i, 'start'] <= bandwidth_df_function.loc[j, 'finish'] and df.loc[i, 'finish'] >= bandwidth_df_function.loc[j, 'start']):
#                 print("got in")
#                 if (bandwidth_current > bandwidth_adjustment):
#                     bandwidth_adjustment =   bandwidth_df_function.loc[j, 'bandwidth'] + bandwidth_df_function.loc[j, 'effort']
#                     df.loc[i, 'bandwidth'] = bandwidth_adjustment
#                     #bandwidth_df_function.loc[i, 'bandwidth'] + bandwidth_df_function.loc[j, 'effort']


#                     bandwidth_df_function = df[(df['bandwidth'] >= df.loc[i, 'bandwidth']) & (df['bandwidth'] < df.loc[i, 'bandwidth'] + df.loc[i, 'effort'])]
#                     bandwidth_df_function = bandwidth_df_function.drop(df[df['order'] == i]['order'], axis=0)
#                     #df[(df['bandwidth'] >= df.loc[i, 'bandwidth']) & (df['bandwidth'] < df.loc[i, 'bandwidth'] + df.loc[i, 'effort'])]
#                     #print(bandwidth_df_function)
#                     #print(bandwidth_df_inner)


#                     bandwidth_df_function = bandwidth_df_function.reset_index()
#                     #print(bandwidth_df_function)
#                     return test(i, bandwidth_df_function)


#             #df.loc[i, 'bandwidth'] >= bandwidth & df['bandwidth'] + bandwidth <= df['bandwidth'] + df['level_of_effort']  ]
#             #df.loc[i, 'bandwidth'] = bandwidth + bandwidth_df.loc[j, 'effort'] + .5

#             # print("i")
#             # print(df.iloc[i])
#             # print("bandwidth df at j")
#             # print(bandwidth_df.iloc[j])
#             # sys.exit()

#             # df.loc[i, 'bandwidth'] = bandwidth + .5
#             # print("i")
#             # print(df.iloc[i])
#             # print("bandwidth at j")
#             # print(df.iloc[j])
#             # print('break')

#     else:
#         return "test"
# i = 0
# bandwidth_df = df.copy()
# while i < len(df):
#     df = df.reset_index(drop=True)
#     #bandwidth_list = df['bandwidth'].unique().tolist()
#     #bandwidth_list.sort()
#     #found_place = False
#                   # (df['A'] > 1) & (df['B'] < 5)
#     bandwidth_df = df[(df['bandwidth'] >= df.loc[i, 'bandwidth']) & (df['bandwidth'] < df.loc[i, 'bandwidth'] + df.loc[i, 'effort'])].reset_index()
#     # print(len(bandwidth_df))
#     # print(i)
#     # print(df)
#     # print(bandwidth_df)
#     if(len(bandwidth_df) > 0):
#         if len(df[df['order'] == i]['order']) > 0:
#             print("test")
#             print(df[df['order'] == i]['order'])

#             index_to_drop = df[df['order'] == i]['order'].tolist()[0]

#             print(index_to_drop)
#             bandwidth_df = bandwidth_df[bandwidth_df['order'] != index_to_drop]
#         else:
#             i += 1
#             continue

#     else:


#         continue
#     bandwidth_df = bandwidth_df.drop(['index'], axis=1)

#     bandwidth_df = bandwidth_df.reset_index()
#     #print("i: " + str(i))
#     #print(bandwidth_df)

#     test(i, bandwidth_df)

#     #print(df)
#     i += 1
#     # for bandwidth in bandwidth_list:
#     #     collision = False
#     #     # print("----bandwidth iteration: " + str(bandwidth) + "----")
#     #     bandwidth_df = df[df['bandwidth'] == bandwidth]
#     #     second_collision = False
#     #     bandwidth_df = bandwidth_df.reset_index()
#     #     amount_to_add = 0
#     #     for j in range(0, len(bandwidth_list)):
#     #         print("i: " + str(i))
#     #         print("j: " + str(j))
#     #
#     #         try:
#     #             if ((df.loc[i, 'start'] <= bandwidth_df.loc[j, 'finish'] and df.loc[i, 'finish'] >= bandwidth_df.loc[j, 'start']) and df.loc[i, 'order'] != bandwidth_df.loc[j, 'order']):
#     # bandwidth_df = and df.loc[i, 'bandwidth'] >= bandwidth & df['bandwidth'] + bandwidth <= df['bandwidth'] + df['level_of_effort']  ]
#     #                 #df.loc[i, 'bandwidth'] = bandwidth + bandwidth_df.loc[j, 'effort'] + .5
#     #                 df.loc[i, 'bandwidth'] = bandwidth + bandwidth_df.loc[j, 'effort'] + .5
#     #                 # print("i")
#     #                 # print(df.iloc[i])
#     #                 # print("bandwidth df at j")
#     #                 # print(bandwidth_df.iloc[j])
#     #                 # sys.exit()
#     #                 collision = True
#     #                 # df.loc[i, 'bandwidth'] = bandwidth + .5
#     #                 # print("i")
#     #                 # print(df.iloc[i])
#     #                 # print("bandwidth at j")
#     #                 # print(df.iloc[j])
#     #                 # print('break')
#     #                 break
#     #
#     #
#     #
#     #
#     #                 # else:
#     #                 #     df.loc[i, 'bandwidth'] = bandwidth
#     #         except:
#     #             continue
#     #     if collision == False and second_collision == False:
#     #
#     #         df.loc[i, 'bandwidth'] = bandwidth
#     #         break
#     #

#     # print("i")
#     # print("task: " + df.loc[i, 'task'] + "; bandwidth: " + str(df.loc[i, 'bandwidth']))
#     # bandwidth = df.loc[i, 'bandwidth']
#     # bandwidth_list = []
#     # bandwidth_list.append(bandwidth)
#     # for j in range(0, len(df)):
#     #     # print("j begin")
#     #     # print("task: " + df.loc[j, 'task'] + "; bandwidth: " + str(df.loc[j, 'bandwidth']))
#     #
#     #     # if i == 1 and j == 0:
#     #     #     print("at 1,0")
#     #     #     print("i task:      " + df.loc[i, 'task'])
#     #     #     print("i start:     " + df.loc[i, 'start'])
#     #     #     print("i finish:    " + df.loc[i, 'finish'])
#     #     #     print("i bandwidth: " + str(df.loc[i, 'bandwidth']))
#     #     #
#     #     #     print("j task:      " + df.loc[j, 'task'])
#     #     #     print("j start:     " + df.loc[j, 'start'])
#     #     #     print("j finish:    " + df.loc[j, 'finish'])
#     #     #     print("j bandwidth: " + str(df.loc[j, 'bandwidth']))
#     #
#     #     if (df.loc[i, 'start'] < df.loc[j, 'finish'] and df.loc[i, 'bandwidth'] == df.loc[j, 'bandwidth'] and i != j):
#     #
#     #         df.loc[i, 'bandwidth'] = df.loc[j, 'bandwidth'] + .5
#     #
#     #         print("i updated: task: " + df.loc[i, 'task'] + "; bandwidth: " + str(df.loc[i, 'bandwidth']))
#     #         print("j updated: task: " + df2.loc[j, 'task'] + "; bandwidth: " + str(df2.loc[j, 'bandwidth']))
#     #     # elif df.loc[i, 'start'] >= df2.loc[j, 'finish'] :
#     #     #     df.loc[i, 'bandwidth'] = df2.loc[j, 'bandwidth']
#     #     #     df2.loc[i, 'bandwidth'] = df2.loc[j, 'bandwidth']
#     #
#     #     # print("j end")
#     #     # print("task: " + df.loc[j, 'task'] + "; bandwidth: " + str(df.loc[j, 'bandwidth']))
#     # print("i end")
#     # print("task: " + df.loc[i, 'task'] + "; bandwidth: " + str(df.loc[i, 'bandwidth']))
#     #
#     #     # else:
#     #     #     df.loc[i, 'bandwidth']
#     #     #     df.loc[i, 'bandwidth'] = df.loc[i-j, 'bandwidth'] + .5
#     #     # position_df = df[df['bandwidth'] == df.loc[j, 'bandwidth']]
#     #     # for k in reversed(range(0, len(position_df))):
#     #     #     if (df.loc[i, 'start'] < df.loc[i-j, 'finish']):
#     #     #
#     #     #         df.loc[i, 'bandwidth'] = df.loc[i-j, 'bandwidth'] + .5


# print(df)

# #position_df = df[df['bandwidth'] == df.loc[j, 'bandwidth']]
# # print("k")
# # print(position_df)

# # for k in range(0, len(position_df)):

# # df.loc[i, 'bandwidth'] = last_bandwidth

# # elif (df.loc[i, 'start'] >= df.loc[j, 'finish']):
# #     position_df = df[df['bandwidth'] == ][j, 'bandwidth']
# #     found = False
# #     for k in len(position_df):
# #         if (df.loc[i, 'start'] < df.loc[j, 'finish']):
# #             found = true
# #     if


# tasks = df['task']

# for task in tasks:
#     print(task)
#     stacks = []
#     stacks = df[df['task'] == task]['stack'].tolist()
#     print("stacks")
#     print(stacks)
#     stacks.sort()
#     min = stacks[0]
#
#     df.loc[df['task'] == task, 'stack'] = min
fig, gnt = plt.subplots()
array = np.linspace(0, 1, len(df))
np.random.shuffle(array)
color = iter(cm.rainbow(array))
#
# Plotting the area chart
# palette = cycle(pex.colors.qualitative.Bold)
# plt.style.use('ggplot')
for l in range(0, len(df)):
    #print(df.loc[l, 'start'])
    #print(df.loc[l, 'finish'])
    start = datetime.strptime(df.loc[l, 'start'], "%Y-%m-%d")
    #print(pd.to_datetime(start))
    #print(type(pd.to_datetime(start)))
    finish = datetime.strptime(df.loc[l, 'finish'], "%Y-%m-%d")
    #print(type(pd.to_datetime(finish)))
    #print(type(pd.to_datetime(finish)))
    #gnt.broken_barh([(pd.to_datetime(start).timestamp(), pd.to_datetime(finish).timestamp()-pd.to_datetime(start).timestamp())], [int(df.loc[l, 'bandwidth']), int(df.loc[l, 'effort'])], color=next(color))
    gnt.broken_barh([(pd.to_datetime(start), pd.to_datetime(finish)-pd.to_datetime(start))], [int(df.loc[l, 'bandwidth']), int(df.loc[l, 'effort'])], color=next(color), label=df.loc[l, 'task'])

# ax.set_yticks(range(len(label)))
# ax.set_yticklabels(label)


# gantt = pex.timeline(df, x_start='start', x_end='finish',
#                      y='bandwidth', color='task', height=600, width=height)
# for i, d in enumerate(gantt.data):
#     gantt.data[i]['width'] = df.loc[x, 'width']
#
fig.set_figheight(30)
fig.set_figwidth(80)
# fig.tight_layout()
gnt.set_xlabel("Date")
gnt.set_ylabel("Bandwidth")
#gnt.update_traces(marker_color=df.loc['task'].tolist(), marker_colorscale="Rainbow")
#gnt.set_ylabel('fruit supply')
#fig.show()
# gantt.update_traces(width=width_list)
#fig.write_image("yourfile.png")

fig.legend()
plt.subplots_adjust(right=0.6, bottom=0.2, top=1)
plt.xticks(rotation=45)
# plt.update_layout(legend=dict(font=dict(size(10))))
plt.show(block=True)
