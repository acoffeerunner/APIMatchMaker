import sys
import argparse
import time
from os import cpu_count
from runner import Runner
from common.file_ops import *
from common.logger import logger
import nltk

Presolved_PATH = "./data-dump/Presolved"
Description_PATH = "./data-dump/Description_fromGP/"
T_dir = ""
folds = 10


def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="arg parser")
    parser.add_argument("-pre", "--presolve", default=Presolved_PATH, help="Path of the presolved temporary files.")
    parser.add_argument("-d", "--description", default=Description_PATH, help="Path of the description of APKs.")
    parser.add_argument("-data", "--dataset", default=T_dir, help="Root dir of the dataset.")
    parser.add_argument("-m", "--maxjob", type=int, default=cpu_count(), help="Max jobs.")
    options = parser.parse_args(args)
    return options


if __name__ == '__main__':
    OPTIONS = getOptions()
    OPTIONS.log_obj = logger(0)
    nltk.download('punkt')
    for i in range(0, folds):

        OPTIONS.log_obj.info(f"Processing data for dataset fold {i+1}")
        OPTIONS.dataset = f"./dataset/dataset_{i+1}/"

        OPTIONS.log_obj.debug(f"Dataset fold {i+1} set at {OPTIONS.dataset}")

        if not OPTIONS.dataset.endswith("/"):
            OPTIONS.dataset += "/"
        T_dir = OPTIONS.dataset

        RECOMMENDATION_PATH = T_dir + "Recommendation/"
        Project_Sim = T_dir + "ProjectSim/"
        Training_Set = T_dir + "TrainingSet.txt"
        Training_Set_filtered = T_dir + "TrainingSet_filtered/"
        Test_Set = T_dir + "TestSet/"
        GroundTruth_PATH = T_dir + "GroundTruth/"
        custom_args = {
            'RECOMMENDATION_PATH': RECOMMENDATION_PATH,
            'Project_Sim': Project_Sim,
            'Training_Set_filtered': Training_Set_filtered,
            'Training_Set': Training_Set,
            'Test_Set': Test_Set,
            'GroundTruth_PATH': GroundTruth_PATH
        }

        OPTIONS.log_obj.info(f"Creating directories for processing and recommendations.")
        for item in custom_args:
            if item not in ['Training_Set']:
                OPTIONS.log_obj.debug(f"Checking for {custom_args[item]}")
                check_and_mk_dir(custom_args[item])
                OPTIONS.log_obj.debug(f"{custom_args[item]} is created")

        OPTIONS.log_obj.debug(f"Starting runner on dataset_{i+1}")
        Runner(OPTIONS, custom_args).start()
        OPTIONS.log_obj.info(f"Operations for dataset fold {i+1} completed!")
        
