import os

DATA_DIR = os.path.join(os.getcwd(), "data", "physionet.org", "files", "eegmmidb", "1.0.0")
print(DATA_DIR)
# "/content/drive/MyDrive/physionet.org/files/eegmmidb/1.0.0/"
DATA_URL = "https://physionet.org/files/eegmmidb/1.0.0"

N_SUBJECTS = 30 # 109

DATA_EX_RUNS = [3, 7, 11]
DATA_IM_RUNS = [4, 8, 12]
DATA_RUNS = [*DATA_EX_RUNS, *DATA_IM_RUNS]

SELECTED_NODES = ["C1", "C2", "C3", "C4", "C5", "C6", "Cz"]

# for our runs, according to https://physionet.org/content/eegmmidb/1.0.0/
# T1 means left fist, T2 means right fist. just in case, const below
LEFT_ANNO = "T1"
RIGHT_ANNO = "T2"
NONE_ANNO = "T0"

DELTA_BAND = (0.5, 4)          # Deep sleep, very slow brain activity
THETA_BAND = (4, 8)            # Drowsiness, memory, some cognitive processes
ALPHA_BAND = MU_BAND = (8, 13) # Relaxed wakefulness, especially eyes closed
                               # Sensorimotor rhythm; closely related to motor activity
BETA_BAND = (13, 30)           # Active thinking, motor activity
GAMMA_BAND = (30, 9999999)     # Higher-frequency neural activity, perception/cognition

BANDS = [DELTA_BAND, THETA_BAND, ALPHA_BAND, BETA_BAND, GAMMA_BAND]

import os

def format_subject(subject):
  return f"S{subject:03d}"

def get_filename(subject, run):
  return f"{format_subject(subject)}R{run:02d}.edf"

def get_filepath(subject, run=None):
  subject_f = format_subject(subject)
  if run is None:
    return os.path.join(DATA_DIR, subject_f)
  return os.path.join(DATA_DIR, subject_f, get_filename(subject, run))

def get_url(subject, run):
  return f"{DATA_URL}/{format_subject(subject)}/{get_filename(subject, run)}"

import mne

def load_path(path, *, preload):
  raw = mne.io.read_raw_edf(path, preload=preload)
  # weirdly formatted channel names that have periods
  # to keep consistent column width, just get rid of those
  raw.rename_channels(lambda name: name.replace(".", ""))
  return raw

def load(subject, run, *, preload):
  return load_path(get_filepath(subject, run), preload=preload)

raw = load(1, DATA_EX_RUNS[0], preload=False)

raw.plot(
    picks=SELECTED_NODES,
    scalings=5e-4)

import matplotlib.pyplot as plt

plt.show()
