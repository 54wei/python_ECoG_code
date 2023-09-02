import mne
import matplotlib.pyplot as plt
from matplotlib import colormaps
from mne_bids import BIDSPath, read_raw_bids
import os
import tkinter as tk
import tkinter.filedialog

def preProcessing1(file_path, file_name):
    raw = mne.io.read_raw(file_path + '/' + file_name)
    file_name = file_name[:-12] # delete the suffix

    # Remove empty channels
    empty_channels = list()
    for i in range(129, 257): empty_channels.append(str(i))
    raw.info['bads'] = []
    raw.info['bads'].extend(empty_channels)
    raw.drop_channels(raw.info['bads'])

    # Load the data
    raw.load_data()

    # Resample
    print(raw.info['sfreq'])
    raw.resample(500)
    print(raw.info['sfreq'])


    # raw.plot_psd(fmin=0, fmax=100)
    # Remove line frequency interference
    raw.notch_filter([50], trans_bandwidth=3)
    # raw.plot_psd(fmin=0, fmax=100)

    # Band pass filter
    # filter_params  = mne.filter.create_filter(data=raw.get_data(), sfreq=raw.info['sfreq'], l_freq=0.1, h_freq=45)
    # mne.viz.plot_filter(filter_params, raw.info["sfreq"], flim=(0.01, 100))
    # fig = raw.plot(duration=20, n_channels=16, remove_dc=False, color='b')
    raw.filter(l_freq=0.1, h_freq=45)
    # fig2 = raw.plot(duration=20, n_channels=16, remove_dc=True, color='b', scalings=dict(ecog=250e-6))

    save_path = file_path + '/'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    raw.save(save_path + file_name + '_preprocessed_1.fif', overwrite=True)

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
    if file_name_now[-7:] != 'raw.fif':
        file_names.remove(file_name_now)

for i in range(0, len(file_names)):
    # Choose the file
    file_name = file_names[i]
    preProcessing1(file_path, file_name)


