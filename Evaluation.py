import re
import sys
import os
import csv
from common.file_ops import *

csv.field_size_limit(100000000)

def count_precision(files):
    all = 0.0
    num = 0
    for file in files:
        with open(file, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                score = float(line[1])
                all += score
                num += 1
    print("precision: " + str(all / (num + 0.01)))


def count_recall(files):
    all = 0.0
    num = 0
    for file in files:
        with open(file, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                score = float(line[2])
                all += score
                num += 1
    print("recall: " + str(all / (num + 0.01)))


def count_successrate(files):
    valid = 0
    num = 0
    for file in files:
        with open(file, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                score = float(line[1])
                if score:
                    valid += 1
                num += 1
    print("valid samples: " + str(num))
    print("success rate: " + str(valid / (num + 0.01)))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        dataset_fold = str(sys.argv[1])
        print("Calculating results for dataset fold " + dataset_fold)
        for topnum in ['1', '5', '10', '15', '20']:
            print("@"+topnum+" results:")
            start_s = "evaluation" + topnum + "_" + "dataset_" + dataset_fold

            path = os.getcwd()
            files = getFileList2(path, start_s, ".csv")

            count_precision(files)
            count_recall(files)
            count_successrate(files)
            print("\n\n")
    else:
        print("Retry with the following usage pattern!\n\nUsage pattern: python Evaluation.py <dataset_fold number>")
