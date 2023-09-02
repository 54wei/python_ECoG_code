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
file_pathraw = '/Users/wxc/Desktop/mne_file_0821/awake_fre2002_preprocessed_1.fif'
file_pathevents = '/Users/wxc/Desktop/mne_file_0821/awake_fre2002_events_1000Hz.fif'
raw = mne.io.read_raw_fif(file_pathraw)


raw.info['bads'] = list(map(str, list(range(33,129))))
# use the average of all channels as reference
# raw.load_data()
# raw.set_eeg_reference(ref_channels="average")

# load eventfile
events = mne.read_events(file_pathevents)

#resample 500Hz
new_events = np.copy(events) # 创建一个events的副本
new_events[:, 0] = np.round(new_events[:, 0] / 2) # 将第一列除以2

new_events[new_events[:, 2] == 0, 2] = 1 # 将第三列中等于0的元素替换成1

# print(new_events)


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

file_name = '111'
# Save
epochs.save(file_path + '/' + file_name + '_epochs(badChoosed).fif', overwrite=True)
# # 提取ERP
# erp_cond1 = epochs["cond_1"].average()
# erp_cond2 = epochs["cond_2"].average()
# erp_cond3 = epochs["cond_3"].average()
# #
# channels = list(range(1,33))
# for i in range(1,33):
#     channels[i-1] = str(channels[i-1])
    
# fig1 = erp_cond1.plot(picks=channels)