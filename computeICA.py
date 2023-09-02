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
    if file_name_now[-18:] != 'preprocessed_1.fif':
        file_names.remove(file_name_now)


for i in range(0, len(file_names)):
    # Choose the file
    file_name = file_names[i]
    raw = mne.io.read_raw(file_path + '/' + file_name)
    file_name = file_name[:-19] # delete the suffix
    # ICA/SSP
    ica = mne.preprocessing.ICA(n_components=30, max_iter="auto")
    ica.fit(raw)
    ica.save(file_path + '/' + file_name + '_ica.fif', overwrite=True)

