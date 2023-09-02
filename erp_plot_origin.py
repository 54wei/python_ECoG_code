import mne
import matplotlib.pyplot as plt
from matplotlib import colormaps
from mne_bids import BIDSPath, read_raw_bids
import os
import numpy as np
import tkinter as tk
import tkinter.filedialog

# 选择文件夹
# # initialdir = 'F:/ZWQ/anesthesia/anesthesia_profosol/20230706' # 默认路径，没有就赋值''
# initialdir = ''
# if initialdir != '':
#     file_path = tk.filedialog.askdirectory(title='选择mne_file文件夹:', initialdir=initialdir)
# else:
#     file_path = tk.filedialog.askdirectory(title='选择mne_file文件夹:')
file_path = '/Users/wxc/Desktop/auditory_initial_trigger'

# Read the data
file_names = os.listdir(file_path)
for file_name_now in file_names.copy():
    if file_name_now[-16:] != '(badChoosed).fif':
        file_names.remove(file_name_now)
#

#
epochs_list = []
for file_name in file_names:
    epochs_now = mne.read_epochs(file_path+ '/' + file_name)
    epochs_list.append(epochs_now)
#
epochs_all = mne.concatenate_epochs (epochs_list) # 使用mne.concatenate_epochs函数来合并列表中的所有epoch文件

# 拒绝250*10-6以上的值
reject_criteria = dict(
    ecog = 250e-6
)
epochs_all.drop_bad(reject=reject_criteria)

# use the average of all channels as reference
# epochs_all.set_eeg_reference(ref_channels="average")


ERP_all_1 = epochs_all['cond_1'].average()
ERP_all_2 = epochs_all['cond_2'].average()
ERP_all_3 = epochs_all['cond_3'].average()
# smooth
# ERP_all_1 = ERP_all_1.smooth(n_jobs=1, h_freq=15)


#将三种条件叠加在一起,取平均
# all_ERP_condition = [ERP_all_1,ERP_all_2,ERP_all_3]
# average_ERP_condition = mne.combine_evoked(all_ERP_condition,weights='equal')
# # new ERP
# ERP_all_1 = mne.combine_evoked(all_ERP_condition, weights=[2/3, -1/3, -1/3])
# ERP_all_2 = mne.combine_evoked(all_ERP_condition, weights=[-1/3, 2/3, -1/3])
# ERP_all_3 = mne.combine_evoked(all_ERP_condition, weights=[-1/3, -1/3, 2/3])

#11,有 bar
evokeds = dict(
    auditory_sti1_1Hz=list(epochs_all["cond_1"].iter_evoked()),
    auditory_sti2_5Hz=list(epochs_all["cond_2"].iter_evoked()),
    auditory_sti3_10Hz=list(epochs_all["cond_3"].iter_evoked()),
)


#基线的归一化处理zsore,将数据减去基线期间的均值，再除以基线期间的标准差。
baseline = (-1.0, 0)
times = evokeds['auditory_sti1_1Hz'][0].times
ERP_all_1.data = mne.baseline.rescale(ERP_all_1.data, times, baseline = baseline, mode='zscore',copy=True, verbose=None)
ERP_all_2.data = mne.baseline.rescale(ERP_all_2.data,times, baseline = baseline, mode='zscore',copy=True, verbose=None)
ERP_all_3.data = mne.baseline.rescale(ERP_all_3.data,times, baseline = baseline, mode='zscore',copy=True, verbose=None)


# 有error bar和无error bar和有error bar
#无
# erps = dict(
#     auditory_sti1_1Hz = epochs_all['cond_1'].average(),
#     auditory_sti2_5Hz = epochs_all['cond_2'].average(),
#     auditory_sti3_10Hz = epochs_all['cond_3'].average(),
# )
# no errorbar
erps = dict(
    auditory_sti1_1Hz = ERP_all_1,
    auditory_sti2_5Hz = ERP_all_2,
    auditory_sti3_10Hz = ERP_all_3,
)

evokeds_colors = [(1.,122/255.,94/255.), (0.,64/255.,91/255.), (130/255.,178/255.,154/255.)]

# # calculate error bar,se
# def se(data):
#     # data is an array of shape (n_channels, n_times)
#     # return an array of shape (n_times,) with standard error values
    

#     # keys = data.keys
#     # ses = data
#     # for ind in range(0, len(keys)):
#     #     data_now = data[keys[ind]]
#     #     epochs_mean = np.zeros((128, len(data_now)))
#     #     for i in range(0, len(data_now)):
#     #         epoch_now = data_now[i]
#     #         epoch_now_mean = np.mean(epoch_now.data, axis=1)
#     #         epochs_mean[:, i] = epoch_now_mean
#     #     se_now = np.std(epochs_mean, axis=1) / np.sqrt(epochs_mean.shape[1])
#     #     ses[keys(ind)] = se_now
#     # return ses


    # epochs_mean = np.mean(data, axis=1)
    # epochs_mean_se = np.std(epochs_mean, axis=0) / np.sqrt(epochs_mean.shape[0])

    # return epochs_mean_se
    

# figure = plt.figure(0)
# for i in range(1,16):
#     axes_now = plt.subplot(2, 8, i+1) # i-16+1
#     mne.viz.plot_compare_evokeds(erps, combine="mean", picks=str(i+1), colors=evokeds_colors, show=False, axes=axes_now, legend=False)
#    # mne.viz.plot_compare_evokeds(erps, combine="mean", picks=str(i+1), show=False, axes=axes_now, legend=False)
    
#     if i != 0:
#         axes_now.set_xlabel('')
#         axes_now.set_ylabel('')
#     else:
#         handles, labels = axes_now.get_legend_handles_labels()
# figure.legend(handles, labels, loc='upper left')        

# plt.show()


mne.viz.plot_compare_evokeds(erps, combine="mean", picks=str(20), colors=evokeds_colors, show=False, legend=True,ci=0.95/1.96)
plt.show()