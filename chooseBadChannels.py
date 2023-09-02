import mne
import matplotlib.pyplot as plt

# Read the data
file_path = 'F:/ZWQ/anesthesia/anesthesia_profosol/20230706/mne_file'
file_name = 'awake_a01005_ns2_raw.fif'
raw = mne.io.read_raw_fif(file_path + '/' + file_name)

# Artifact detection
channels = mne.pick_types(raw.info, ecog=True)
channels_choosed = channels[:128]
raw.plot(duration=3, order=channels_choosed, n_channels=16, remove_dc=False, color='b')
plt.show()

# Save
raw.save(file_path + '/' + file_name[:-4] + '_badChannelChoosed.fif', overwrite=True)
