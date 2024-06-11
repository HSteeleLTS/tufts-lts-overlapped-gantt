import pandas as pd
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
from datetime import datetime, timedelta
from itertools import cycle
from matplotlib.animation import FuncAnimation
import numpy as np

# File selection and DataFrame loading
filename = askopenfilename(title="Select project sheet")
projects_df = pd.read_excel(filename, engine="openpyxl", dtype={'start_date': 'str', 'end_date': 'str'})

projects_df['stack'] = 0
projects_df = projects_df.sort_values(['start_date', 'end_date'])

min_start_date = projects_df['start_date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d")).min()
max_end_date = projects_df['end_date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d")).max()

delta = (max_end_date - min_start_date).days
height_of_matrix = projects_df['level_of_effort'].sum()

date_range = pd.date_range(min_start_date, max_end_date)
range_list = list(reversed(list(range(0, height_of_matrix))))
range_list = [str(x) for x in range_list]

master_plotting_df = pd.DataFrame(columns=date_range, index=range_list)

# Fill the master_plotting_df (simplified for illustration)
for x in range(len(projects_df)):
    y = 0
    while True:
        try:
            project_dates_and_effort_df = master_plotting_df.loc[
                str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y),
                projects_df.iloc[x, projects_df.columns.get_loc('start_date')]: projects_df.iloc[x, projects_df.columns.get_loc('end_date')]
            ]
            if project_dates_and_effort_df.equals(master_plotting_df.loc[
                str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y),
                projects_df.iloc[x, projects_df.columns.get_loc('start_date')]: projects_df.iloc[x, projects_df.columns.get_loc('end_date')]
            ]):
                projects_df.at[x, 'stack'] = y
                master_plotting_df.loc[
                    str(y + int(projects_df.iloc[x, projects_df.columns.get_loc('level_of_effort')]) - 1): str(y),
                    projects_df.iloc[x, projects_df.columns.get_loc('start_date')]: projects_df.iloc[x, projects_df.columns.get_loc('end_date')]
                ] = 1
                y += 1
                break
            else:
                y += 1
        except Exception as e:
            print(f"Error processing row {x}: {e}")
            break

# Set up the figure and axis for animation
fig, gnt = plt.subplots(figsize=(16, 10))
colors = cycle(['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray'])

# Function to update the plot
def update_plot(i):
    gnt.cla()  # Clear the axis
    step_df = projects_df.copy()
    step_df['start_date'] = step_df['start_date'].apply(lambda x: (datetime.strptime(x, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d"))
    step_df['end_date'] = step_df['end_date'].apply(lambda x: (datetime.strptime(x, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d"))

    for l, row in step_df.iterrows():
        try:
            start = pd.to_datetime(row['start_date'])
            finish = pd.to_datetime(row['end_date'])
            stack = row['stack']
            level_of_effort = row['level_of_effort']
            task = row['task']
            color = next(colors)

            gnt.broken_barh([(start, finish - start)], [stack, level_of_effort], color=color, label=task)
            gnt.text(x=start + (finish - start) / 2,
                     y=(stack + level_of_effort) - level_of_effort / 2,
                     s=task,
                     ha='center',
                     va='center',
                     color='blue',
                     fontsize='xx-small')
        except Exception as e:
            print(f"Error in animation frame {i} for row {l}: {e}")

    gnt.set_xlabel('Time')
    gnt.set_ylabel('Task Effort')
    gnt.set_title('Animated Broken Barh Plot')

# Create the animation
ani = FuncAnimation(fig, update_plot, frames=np.arange(0, 10), repeat=False)

# Display the animation
plt.show()
