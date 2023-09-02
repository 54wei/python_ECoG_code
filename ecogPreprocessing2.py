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

# Choose the file
file_name = file_names[0]
raw = mne.io.read_raw(file_path + '/' + file_name)
file_name = file_name[:-19] # delete the suffix
ica = mne.preprocessing.read_ica(file_path + '/' + file_name + '_ica.fif')

# 查看哪些components需要去除
# ica_sources = ica.get_sources(raw)
# ica_sources.plot(duration=10, n_channels=16, remove_dc=True, color='b', scalings=dict(misc=2))
# ica_sources.plot_psd(fmin=0, fmax=10, picks=['misc'])
# plt.show()
# # ctypes = ica_sources.get_channel_types()

# 去除指定components
# ica.plot_sources(raw)
# plt.show()
ica.exclude = [15]
print(ica.exclude)
raw.load_data()
raw_exclude_ica = raw.copy()
ica.apply(raw_exclude_ica)

# 对比图、保存
# raw.plot(duration=10, n_channels=16, remove_dc=True, color='b', scalings=dict(ecog=500e-6), title='raw')
# raw_exclude_ica.plot(duration=10, n_channels=16, remove_dc=True, color='b', scalings=dict(ecog=500e-6), title='excluded')
# plt.show()
raw_exclude_ica.save(file_path + '/' + file_name + '_preprocessed_2.fif', overwrite=True)
