import mne
import matplotlib.pyplot as plt
from matplotlib import colormaps
from mne_bids import BIDSPath, read_raw_bids
import os
import tkinter as tk
import tkinter.filedialog

# 选择文件夹
# initialdir = 'F:/ZWQ/anesthesia/anesthesia_profosol/20230706' # 默认路径，没有就赋值''
initialdir = ''
if initialdir != '':
    file_path = tk.filedialog.askdirectory(title='选择mne_file文件夹:', initialdir=initialdir)
else:
    file_path = tk.filedialog.askdirectory(title='选择mne_file文件夹:')

# Read the data
file_names = os.listdir(file_path)
for file_name_now in file_names.copy():
    if file_name_now[-18:] != 'preprocessed_2.fif':
        file_names.remove(file_name_now)

# Choose the file
file_name = file_names[0]
raw = mne.io.read_raw(file_path + '/' + file_name)
file_name = file_name[:-19] # delete the suffix

# Choose bad span
# fig = raw.plot(duration=20, n_channels=1, remove_dc=False, color='b')
# fig.fake_keypress('a')

# Divide continuous raw data into equal-sized consecutive epochs
event_dict = {
    'equal_event': 1
}
event_color = {
    'equal_event': 'green'
}
events_equal = mne.make_fixed_length_events(raw, 1, duration=10)
# epochs1 = mne.Epochs(raw, events_equal, event_dict, 0., 30., baseline=None, preload=True)
epochs = mne.Epochs(raw, events_equal, event_dict, -5., 5., baseline=None, preload=True)
epoch_colors = [['b']*128]*epochs.__len__()
mne.viz.plot_epochs(epochs, scalings=600e-6, n_epochs=3, n_channels=16, 
                    events=events_equal, event_color=event_color, event_id=event_dict, 
                    epoch_colors=epoch_colors)
plt.show()

# Save
epochs.save(file_path + '/' + file_name + '_epochs(badChoosed).fif', overwrite=True)
