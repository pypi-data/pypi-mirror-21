import os
import pickle
import zipfile
from pip._vendor.progress.bar import ShadyBar

import ilms


class ProgressBar(ShadyBar):

    suffix = ' %(percent).1f%%'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calc_step(self, size):
        if size < 10:
            self.max = size
            return 1
        else:
            self.max = size // 10
            return 10


def unzip(filepath, dest_folder):
    if filepath.endswith('.zip'):
        zip_ref = zipfile.ZipFile(filepath, 'r')
        zip_ref.extractall(dest_folder)
        zip_ref.close()


def get_home_dir():
    _base_dir = os.path.expanduser('~')
    _ilms_dir = os.path.join(_base_dir, '.ilms')
    return _ilms_dir


def save_session(sess):
    base = ilms._ilms_dir
    with open(os.path.join(base, 'sess.pickle'), 'wb') as f:
        pickle.dump(sess, f, pickle.HIGHEST_PROTOCOL)


def load_session():
    base = ilms._ilms_dir
    filepath = os.path.join(base, 'sess.pickle')
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        return pickle.load(f)
