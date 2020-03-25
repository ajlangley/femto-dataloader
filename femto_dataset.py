from collections import defaultdict
import glob
import numpy as np
import os
import shutil
import urllib
import zipfile

femto_url = 'https://ti.arc.nasa.gov/c/18/'
bearing_loads = {}
bearing_rpms = {}

class FEMTODataset:
    def __init__(self, data_dir='femto-st'):
        # Download if not already downloaded
        if not os.path.exists(data_dir):
            print('Downloading FEMTO-ST dataset...')
            urllib.request.urlretrieve(femto_url, '.femto-zip.zip')

            os.mkdir(data_dir)
            train_path = os.path.join(data_dir, 'train')
            val_path = os.path.join(data_dir, 'val')
            test_path = os.path.join(data_dir, 'test')

            print('Unzipping files...')
            main_zip = zipfile.ZipFile('.femto-zip.zip', 'r')
            main_zip.extractall('.femto-temp')
            train_zip = zipfile.ZipFile('.femto-temp/Training_set.zip')
            train_zip.extractall('.train-temp')
            shutil.move('.train-temp/Learning_set', train_path)
            val_zip = zipfile.ZipFile('.femto-temp/Test_set.zip')
            val_zip.extractall('.val-temp')
            shutil.move('.val-temp/Test_set', val_path)
            test_zip = zipfile.ZipFile('.femto-temp/Validation_Set.zip')
            test_zip.extractall('.test-temp')
            shutil.move('.test-temp/Full_Test_Set', test_path)

            os.remove('.femto-zip.zip')
            shutil.rmtree('.femto-temp')
            shutil.rmtree('.train-temp')
            shutil.rmtree('.val-temp')
            shutil.rmtree('.test-temp')

            print('Download complete.\n')


        print('Loading training set...')
        self.train = FEMTOPartition(os.path.join(data_dir, 'train'))
        print('Loading validation set...')
        self.val = FEMTOPartition(os.path.join(data_dir, 'val'))
        print('Loading test set...')
        self.test = FEMTOPartition(os.path.join(data_dir, 'test'))
        print('Loading complete.')


class FEMTOPartition:
    def __init__(self, data_dir):
        self.data_dir = data_dir
#         self.is_loaded = defaultdict(lambda: False)
        regex = os.path.join(self.data_dir, 'Bearing*')
        fps = list(glob.iglob(regex))
        self.bearing_names = []
        self.rtf_exps = dict()

        for fp in fps:
            bearing_name = fp[7:]
            self.bearing_names.append(bearing_name)
            self.rtf_exps[bearing_name] = RTFExperiment(fp)

        self.bearing_names.sort()

    def __getitem__(self, idx):
        if type(idx) is not str:
            idx = self.bearing_names[idx]

        return self.rtf_exps[idx]

    def __len__(self):
        return len(self.bearing_names)


class RTFExperiment:
    def __init__(self, exp_dir):
        fps = list(glob.iglob(os.path.join(exp_dir, 'acc*.csv')))
        fps.sort()

        self.bearing_name = exp_dir.split('/')[-1][7:]
        self.total_useful_life = len(fps) * 10
        self.bearing_load = None
        self.rpm = None
        self.measurements = []

        for fp in fps:
            try:
                self.measurements.append(np.loadtxt(fp, dtype=np.float32, delimiter=',')[:, -2:])
            except ValueError:
                self.measurements.append(np.loadtxt(fp, dtype=np.float32, delimiter=';')[:, -2:])

        self.measurements = np.stack(self.measurements)

    def __getitem__(self, i):
        return self.measurements[i]

    def __len__(self):
        return len(self.measurements)
