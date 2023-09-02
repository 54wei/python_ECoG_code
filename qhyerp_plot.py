import mne
import matplotlib.pyplot as plt
from matplotlib import colormaps
import os
import numpy as np


# 选择文件夹
# # initialdir = 'F:/ZWQ/anesthesia/anesthesia_profosol/20230706' # 默认路径，没有就赋值''
# initialdir = ''
# if initialdir != '':
#     file_path = tk.filedialog.askdirectory(title='选择mne_file文件夹:', initialdir=initialdir)
# else:
#     file_path = tk.filedialog.askdirectory(title='选择mne_file文件夹:')
file_path = '/media/pscognition/2023GNwxc/pure_tonefinedata/mne_file8_7'

# Read the data
file_names = os.listdir(file_path)
for file_name_now in file_names.copy():
    if file_name_now[-20:] != '(badChoosed)_new.fif':
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
    ecog = 300e-6
)
epochs_all.drop_bad(reject=reject_criteria)

# use the average of all channels as reference
# epochs_all.set_eeg_reference(ref_channels="average")

power_all=[]
itc_all=[]
#freqs = np.logspace(*np.log10([1, 30]), num=25)
freqs=np.linspace(1,20,num=19)
n_cycles = freqs / 2.0  # different number of cycle per frequency
for i in ("cond_1","cond_2","cond_3"):
    power, itc = mne.time_frequency.tfr_morlet(
        epochs_all[i],
        freqs=freqs,
        n_cycles=n_cycles,
        use_fft=True,
        return_itc=True,
        decim=3,
        n_jobs=None)
    power_all.append(power)    
    itc_all.append(itc)


for i in range(3):
     ax=plt.subplot(2,2,i+1)
     ax.subtitle=str(5*(i-1)+1)+"Hz"
     power_all[i].plot([24,25,27,30], baseline=(-0.5, 0), mode="ratio", title=str(5*(i-1)+1)+"Hz",show=False,axes=ax,combine= 'mean')
    
plt.show()   
    
for i in range(3):
      ax=plt.subplot(2,2,i+1)
      
      itc_all[i].plot([24,25,27,30], baseline=(-0.5, 0), mode="logratio", title=str(5*(i-1)+1)+"Hz",show=False,axes=ax,combine= 'mean',mask_style='contour')
     

ax=plt.subplot(2,2,4)      
mne.viz.plot_compare_evokeds(evokeds, combine="mean", picks=[24,25,27,30], colors=evokeds_colors, show=False, legend=True,ci=0.85,axes=ax)     
plt.savefig("/media/pscognition/2023GNwxc/pure_tonefinedata/mne_file8_7/example.png",dpi=400)

ERP_all_1 = epochs_all['cond_1'].average()
ERP_all_2 = epochs_all['cond_2'].average()
ERP_all_3 = epochs_all['cond_3'].average()

#24,25,27,30

#14,12,10,16
#将三种条件叠加在一起,取平均
# all_ERP_condition = [ERP_all_1,ERP_all_2,ERP_all_3]
# average_ERP_condition = mne.combine_evoked(all_ERP_condition,weights='equal')
# # new ERP
# ERP_all_1 = mne.combine_evoked(all_ERP_condition, weights=[2/3, -1/3, -1/3])
# ERP_all_2 = mne.combine_evoked(all_ERP_condition, weights=[-1/3, 2/3, -1/3])
# ERP_all_3 = mne.combine_evoked(all_ERP_condition, weights=[-1/3, -1/3, 2/3])

#11,有 bar

epochs_all.filter(l_freq=0.5,h_freq=20)
evokeds = dict(
    auditory_sti1_1Hz=list(epochs_all["cond_1"].iter_evoked()),
    auditory_sti2_5Hz=list(epochs_all["cond_2"].iter_evoked()),
    auditory_sti3_10Hz=list(epochs_all["cond_3"].iter_evoked()),
)


#基线的归一化处理zsore,将数据减去基线期间的均值，再除以基线期间的标准差。
baseline = (-0.3, 0)
times = evokeds['auditory_sti1_1Hz'][0].times
# ERP_all_1.data = mne.baseline.rescale(ERP_all_1.data, times, baseline = baseline, mode='mean',copy=True, verbose=None)
# ERP_all_2.data = mne.baseline.rescale(ERP_all_2.data,times, baseline = baseline, mode='mean',copy=True, verbose=None)
# ERP_all_3.data = mne.baseline.rescale(ERP_all_3.data,times, baseline = baseline, mode='mean',copy=True, verbose=None)


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
mne.viz.plot_compare_evokeds(evokeds, combine="mean", picks=[24,25,27,30], colors=evokeds_colors, show=False, legend=True,ci=0.85)
plt.show()

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


