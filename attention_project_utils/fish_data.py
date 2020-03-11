from .file_handling import *
import pandas as pd
from tqdm import tqdm


class Trial:
    def __init__(self, fish, trial_id, stimulus, eye_angle, neural):
        self.fish = fish
        self.trial_id = trial_id
        self.stimulus = stimulus
        self.eye_angle = eye_angle
        self.tail = None
        self.neural = neural


class Fish:
    def __init__(self, directory):
        self.id = directory.split('/')[-1]
        trial_ids = []
        for folder in list_directories(f'{directory}/neural/PVN'):
            trial_id = int(folder.split('_')[-1])
            trial_ids.append(trial_id)

        area_data = {}
        for area_folder in list_directories(f'{directory}/neural/'):
            area = area_folder.split('/')[-1]
            print(f'Loading {area} data...')
            for folder in tqdm(list_directories(area_folder)):
                trial_id = int(folder.split('_')[-1])

                columns = []
                for file in list_files(folder):
                    columns.append(pd.read_csv(file, index_col=0, usecols=[0, 1]).rename(
                        columns={'Mean': int(file.split('_')[-1].split('.')[0][1:])}))
                df = pd.concat(columns, axis=1, sort=True).transpose().sort_index()
                df.columns = pd.MultiIndex.from_product([[area], df.columns])
                if trial_id in area_data:
                    area_data[trial_id].append(df)
                else:
                    area_data[trial_id] = []
                    area_data[trial_id].append(df)

        trials = dict((trial, {'neural': pd.concat(data, axis=1)}) for trial, data in area_data.items())
        for eye_csv in tqdm(list_files(f'{directory}/eye angle', extension='csv')):
            print(eye_csv.split('_')[-1].split('.')[0])
            trial_id = int(eye_csv.split('_')[-1].split('.')[0])
            if trial_id in trial_ids:
                trials[trial_id]['eye'] = pd.read_csv(eye_csv, index_col=0)
        # print('Loading tail data...')
        # for tail_csv in tqdm(list_files(f'{directory}/tail')):
        #     trial_id = int(tail_csv.split('_')[-1].split('.')[0])
        #     if trial_id in trial_ids:
        #         trials[trial_id]['tail'] = pd.read_csv(tail_csv, index_col=0)

        # self.trials = [Trial(self, i, j['stimulus'], pd.concat([j['eye'], j['tail']], axis=1, sort=True), j['neural'])
        #                for i, j in trials.items()]
        self.trials = [Trial(self, i, None, j['eye'], j['neural'])
                       for i, j in trials.items()]
