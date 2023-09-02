from brpylib import NevFile, NsxFile
import os
import mne
import tkinter as tk
import tkinter.filedialog
import numpy as np

def translate(file_path, file_name):
    # Read data and header and event
    sample_frequencies = [500., 1000., 2000., 10000., 30000., 30000.]
    file_type = 2 # 选择用ns几的数据
    sample_frequency = sample_frequencies[file_type - 1]

    nsx_file = NsxFile(file_path + '/' + file_name + '.ns' + str(file_type))
    event_file = NevFile(file_path + '/' + file_name + '.nev')
    basic_header = nsx_file.basic_header
    extended_header = nsx_file.extended_headers
    raw_data = nsx_file.getdata()

    channel_names = raw_data['elec_ids']
    for i in range(0, len(channel_names)):
        channel_names[i] = str(channel_names[i])
    data = raw_data['data'][0]/1e6 # 把μV变成V

    # get events
    events = event_file.getdata()
    my_events = events['comments']
    my_events_array = np.zeros([len(my_events['TimeStamps']),3], 'int64')
    my_events_array[:,0] = list(np.round(np.array(my_events['TimeStamps']) / (30000/sample_frequency)))
    my_events_array[:,2] = my_events['TimeStampsStarted']

    # Write data into mne raw file
    mne_info = mne.create_info(ch_names=channel_names, sfreq=sample_frequency, ch_types='ecog')
    mne_raw = mne.io.RawArray(data=data, info=mne_info)
    raw_event_info = mne.create_info(ch_names=['Comments'], sfreq=sample_frequency)
    raw_event = mne.io.RawArray(data=np.zeros([1, data.shape[1]], dtype='int64'), info=raw_event_info)
    mne_raw.add_channels([raw_event]) # add stim channels
    mne_raw.add_events(my_events_array, 'Comments',replace=True)

    save_path = file_path + '/mne_file/'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    mne_raw.save(save_path + file_name + '_ns' + str(file_type) + '_raw.fif', overwrite=True)

    # Close the files
    nsx_file.close()
    event_file.close()
    

# 选择文件夹
# initialdir = 'F:/ZWQ/anesthesia/anesthesia_profosol' # 默认路径，没有就赋值''
initialdir = ''
if initialdir != '':
    file_path = tk.filedialog.askdirectory(title='选择包含原始数据的文件夹:', initialdir=initialdir)
else:
    file_path = tk.filedialog.askdirectory(title='选择包含原始数据的文件夹:')
    
file_names = os.listdir(file_path)
for file_name_now in file_names.copy():
    if file_name_now[-3:] != 'nev':
        file_names.remove(file_name_now)

for i in range(0, len(file_names)):
    # Choose the file
    file_name = file_names[i]
    file_name = file_name[:-4] # delete the suffix
    translate(file_path, file_name)

