import math
import os
# import re
from random import shuffle
from os.path import exists as path_exists
from os import mkdir
import shutil
from common import logger, file_ops
from concurrent.futures import ThreadPoolExecutor 

class DatasetGenerator:
    def __init__(self, n_folds,train_size, train_desc_path, train_presolved_path, test_desc_path, test_presolved_path, splitdata_path, processed_data_path, log_obj):
        self.n_folds = n_folds
        self.train_size = train_size

        self.log_obj = log_obj
        if not (path_exists(train_desc_path) or path_exists(test_desc_path) or path_exists(train_presolved_path) or path_exists(test_presolved_path)):
            self.log_obj.error('One of the train/test paths do not exist!')
            exit(1)

        self.train_desc_path = train_desc_path
        self.train_presolved_path = train_presolved_path
        self.test_desc_path = test_desc_path
        self.test_presolved_path = test_presolved_path

        if not path_exists(processed_data_path):
            mkdir(processed_data_path)
        self.processed_data_path = processed_data_path

        self.splitdata_path = splitdata_path
        if not path_exists(splitdata_path):
            mkdir(splitdata_path)

    def split_training_data(self):
        train_hashes = file_ops.get_file_names(self.train_presolved_path, self.log_obj)
        if len(train_hashes) < self.train_size:
            self.log_obj.error(f"Training data size larger than number of available train files {len(train_hashes)} < {self.train_size}")
        shuffle(train_hashes)
        train_hashes = train_hashes[:self.train_size]

        self.log_obj.info(f"Found {len(train_hashes)} data points in training directories.")

        for train_hash in train_hashes:
            if not os.path.join(self.train_desc_path, train_hash+'.txt'):
                self.log_obj.error(f'Description for {train_hash} not found!')
                exit(1)

        n = int(math.ceil(len(train_hashes) * 1.0 / self.n_folds))
        folds = [train_hashes[i: i + n] for i in range(0, len(train_hashes), n)]

        self.write_to_splitdata(folds)

        self.log_obj.info(f'Train records written to splitdata text file.')

        def copy_file(fold, file):
            src = os.path.join(self.train_presolved_path, file)
            dest = os.path.join(self.processed_data_path, f'dataset_{fold+1}', 'GroundTruth', file)
            shutil.copy(src, dest)
            self.log_obj.debug(f'{file} copied to dataset_{fold+1} GroundTruth.')

        for fold in range(len(folds)):
            dest = os.path.join(self.processed_data_path, f'dataset_{fold+1}', 'TrainingSet.txt')
            open(dest, 'w')

        with ThreadPoolExecutor() as executor:
            for fold in range(len(folds)):
                for file in folds[fold]:
                    dest = os.path.join(self.processed_data_path, f'dataset_{fold+1}', 'TrainingSet.txt')
                    with open(dest, 'a') as fw:
                        fw.write(file[:-4]+"\n")
                    executor.submit(copy_file, fold, file)
        
        self.log_obj.info(f'Train records copied to dataset target.')

    def split_testing_data(self):
        test_hashes = file_ops.get_file_names(self.test_presolved_path, self.log_obj)
        shuffle(test_hashes)

        self.log_obj.info(f"Found {len(test_hashes)} data points in testing directories.")

        for test_hash in test_hashes:
            if not os.path.join(self.train_desc_path, test_hash+'.txt'):
                self.log_obj.error(f'Description for {test_hash} not found!')
                exit(1)

        n = int(math.ceil(len(test_hashes) * 1.0 / self.n_folds))
        folds = [test_hashes[i: i + n] for i in range(0, len(test_hashes), n)]

        self.write_to_splitdata(folds)

        self.log_obj.info(f'Test records written to splitdata text file.')

        def copy_file(fold, file):
            src = os.path.join(self.test_presolved_path, file)
            dest = os.path.join(self.processed_data_path, f'dataset_{fold+1}', 'TestSet', file)
            shutil.copy(src, dest)
            self.log_obj.debug(f'{file} copied to dataset_{fold+1} TestSet.')

        with ThreadPoolExecutor() as executor:
            for fold in range(len(folds)):
                for file in folds[fold]:
                    executor.submit(copy_file, fold, file)
        
        self.log_obj.info(f'Test records copied to dataset target.')


    def write_to_splitdata(self, folds):
        self.log_obj.debug(f'Writing to splitdata.')
        for i in range(self.n_folds):
            splitdata_file = os.path.join(self.splitdata_path, str(i + 1) + ".txt")
            with open(splitdata_file, "a") as fw:
                for item in folds[i]:
                    self.log_obj.debug(f'Writing record for {item}.')
                    fw.write(item + "\n") 

    def start(self):
        self.log_obj.debug(f'Creating dataset directories!')
        for fold in range(0, self.n_folds):
            fold_path = self.processed_data_path+f"dataset_{fold + 1}/"
            file_ops.check_and_mk_dir(fold_path)
            self.log_obj.debug(f'Creating dataset_{fold + 1} GroundTruth directory!')
            file_ops.check_and_mk_dir(fold_path + "GroundTruth")
            self.log_obj.info(f'Created dataset_{fold + 1} GroundTruth directory!')
            self.log_obj.debug(f'Creating dataset_{fold + 1} TestSet directory!')
            file_ops.check_and_mk_dir(fold_path +  "TestSet")
            self.log_obj.info(f'Created dataset_{fold + 1} TestSet directory!')

        for i in range(self.n_folds):
            splitdata_file = os.path.join(self.splitdata_path, str(i + 1) + ".txt")
            open(splitdata_file, "w")

        self.split_training_data()
        self.split_testing_data()



if __name__ == '__main__':
    train_desc_path = "./data/Description_fromGP_train/"
    train_presolved_path = "./data/Presolved_train/"
    test_desc_path = "./data/Description_fromGP_test/"
    test_presolved_path = "./data/Presolved_test/"
    processed_data_path = "./dataset/"
    splitdata_path = processed_data_path + "splitdata/"
    log_obj = logger.logger(1)
    size = 12000
    datasetGenerator = DatasetGenerator(10, size, train_desc_path, train_presolved_path, test_desc_path, test_presolved_path, splitdata_path, processed_data_path, log_obj)
    datasetGenerator.start()