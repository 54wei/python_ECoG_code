# 2023-8-8
# awake monkey pure tone trigger events extract,wxc

import mne
import matplotlib.pyplot as plt
from matplotlib import colormaps
from mne_bids import BIDSPath, read_raw_bids
import os
import numpy as np
import tkinter as tk
import tkinter.filedialog

# load fif_raw
# load folder
file_path  = '/Users/wxc/Desktop/mne_file_0821'
# load raw file
file_pathraw = '/Users/wxc/Desktop/mne_file_0821/awake_fre4004_preprocessed_1.fif'
file_pathevents = '/Users/wxc/Desktop/mne_file_0821/awake_fre4004_events_1000Hz.fif'
raw = mne.io.read_raw_fif(file_pathraw)

raw.info['bads'] = list(map(str, list(range(33,129))))

# load eventfile
events = mne.read_events(file_pathevents)

#resample 500Hz
new_events = np.copy(events) # 创建一个events的副本
new_events[:, 0] = np.round(new_events[:, 0] / 2) # 将第一列除以2，第一列所有行，使用了切片的技巧

new_events[new_events[:, 2] == 0, 2] = 1 # 将第三列中等于0的元素替换成1

# print(new_events)
# codi1+75ms;codtion2+1000，第1列是时间点fs*time,
# 选择了new_events的第一列，找到1的行，进行相加
new_events[new_events[:,2]==1,0] += int(500*0.075) 
new_events[new_events[:,2]==16777215,0] += int(500*1)
new_events[new_events[:,2]==255,0] += int(500*0.5)

# Events & samp; Epochs
event_dict = {
    "cond_1": 1,
    "cond_2": 16777215,
    "cond_3": 255,
    # "cond_4": 65280,
    # "cond_5": 16711680,
}

event_color = {
    'cond_1' : 'black',
    'cond_2' : 'green',
    'cond_3': 'red',
}

# epoch的实现
epochs = mne.Epochs(raw, new_events, event_id=event_dict, tmin=-1, tmax=1, preload=True)
# fig = epochs.plot(events=events)
epoch_colors = [['b']*128]*epochs.__len__()
mne.viz.plot_epochs(epochs, scalings=300e-6, n_epochs=6, n_channels=32, 
                    event_color=event_color, event_id=event_dict, events=new_events, 
                    epoch_colors=epoch_colors)
plt.show()

file_name = '444'
# Save
epochs.save(file_path + '/' + file_name + '_epochs(badChoosed).fif', overwrite=True)