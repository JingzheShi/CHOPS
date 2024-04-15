import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 100

import matplotlib.pyplot as plt

# Define data for the plots
x_labels = ['Baseline2:\nExecutor Only\ngpt-3.5-turbo based', '(1-level C)-E\ngpt-3.5-turbo based', '(1-level C)-E-V\ngpt-3.5-turbo based', '(2-level C)-E-V\ngpt-3.5-turbo based', '(2-level C)-E-V\nMixed\n C,V: gpt-3.5-turbo\nE:gpt-4']
accuracy_data = [38.5, 90.4, 96.1, 95.2, 98.0]
accuracy_data_two_line = [82.4, 81.2, 80.4, 90.2, 99.0]
accuracy_data_two_line = [(item_1 + item_2) / 2 for (item_1, item_2) in zip(accuracy_data, accuracy_data_two_line)]
cost_bar = [39.4, 18.6, 101.8, 93.7, 156.8]
baseline_cost = 134.7
relative_cost_bar = [100*item/baseline_cost for item in cost_bar]
print(relative_cost_bar)




fig, ax1 = plt.subplots()

# Left Y-axis (Accuracy) configurations
# ax1.set_xlabel('Label')
ax1.set_ylabel('Averaged Accuracy for SYS and FILE (%)', color='blue')
# ax1.plot(x_labels[:4], accuracy_data[:4], label='Accuracy (sys)', marker='o', color='black', linestyle='-')  # Dark blue for initial segment
# ax1.plot(x_labels[3:], accuracy_data[3:], label='Accuracy (sys)', marker='o', color='black', linestyle='dotted', markersize=5)  # Light blue for point E
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_ylim(60, 100)
ax1.grid(True)  # Enable grid lines for left Y-axis

# Right Y-axis (Relative Cost) configurations
ax2 = ax1.twinx()
ax2.set_ylabel('Relative Cost (%)', color='green')
ax2.bar(['Baseline1:\nExecutor Only\ngpt-4 based'],[100.0],color='lightgreen', alpha=0.5, label='Relative Cost (Bar)')
ax1.plot(['Baseline1:\nExecutor Only\ngpt-4 based'],[84.5],marker='o', color='darkblue', linestyle='', markersize=8)




ax1.plot(x_labels[:4], accuracy_data_two_line[:4], label='Accuracy (file)', marker='o', color='blue', linestyle='-')  # Green line for initial segment
ax1.plot(x_labels[3:], accuracy_data_two_line[3:], label='Accuracy (file)', marker='o', color='blue', linestyle='dotted', markersize=5)
ax2.bar(x_labels, relative_cost_bar, color='green', alpha=0.5, label='Relative Cost (Bar)')
ax2.tick_params(axis='y', labelcolor='green')
ax2.set_ylim(0, 120)

# Disable grid lines for the right Y-axis specifically (if it had any effect)
ax2.grid(False)

fig.tight_layout()
plt.show()
