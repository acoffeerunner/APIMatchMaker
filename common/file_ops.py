import os
import csv
import hashlib
import re
import pandas as pd

csv.field_size_limit(100000000)

def get_file_list(path, log_obj):
    if not os.path.exists(path):
        log_obj.error(f'path {path} does not exist')
        exit(1)

    return [j.split() for j in [i for i in os.walk(path)][0][2]]

def get_file_names(path, log_obj):
    return [i[0] for i in get_file_list(path, log_obj)]
      
def getFileList(rootDir, pick_str):
    filePath = []
    for parent, dirnames, filenames in os.walk(rootDir):
        for filename in filenames:
            if filename.endswith(pick_str):
                file = os.path.join(parent, filename)
                filePath.append(file)
    return filePath


def getFileList2(rootDir, start_str, end_str):
    filePath = []
    for file in os.listdir(rootDir):
        if file.startswith(start_str) and file.endswith(end_str):
            filename = os.path.join(rootDir, file)
            filePath.append(filename)
    return filePath


def getFileList_from_txt(txtfile):
    files = []
    with open(txtfile, "r") as fr:
        for line in fr.readlines():
            files.append(line.strip())
    return files


def getFileList_from_csv(csvfile):
    files = []
    with open(csvfile, "r") as fr:
        reader = csv.reader(fr)
        headings = next(reader)
        for line in reader:
            files.append(line[0].strip())
    return files


def get_sha256(s):
    m = hashlib.sha256()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def dict2sortedlist(dic: dict):
    lst = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    return lst


def writeScores(saveDir, project_name, score_list, headings):
    with open(os.path.join(saveDir, project_name + ".csv"), "w", newline="") as fw:
        writer = csv.writer(fw)
        writer.writerow(headings)
        writer.writerows(score_list)

def load_device(filename):
    devices = {}
    with open(filename, 'r') as fr:
        reader = csv.reader(fr)
        for line in reader:
            if line[0] == "level":
                continue
            api = line[1]
            devices[api] = 1
    return devices

def load_file(filename):
    res = {}
    with open(filename, "r") as fr:
        lines = fr.readlines()
        for line in lines:
            if not line:
                continue
            s = line.split(">:")
            api_sig = s[0].strip() + ">"
            sdks = re.split("]:", s[1].strip("<>"))
            tmp = sdks[0].strip("[] ").split(",")
            new = []
            for item in tmp:
                new.append(int(item))
            res[api_sig] = new
    return res


def load_all_apis(path):
    all = {}
    files = getFileList(path, ".csv")
    for file in files:
        with open(file, "r") as fr:
            reader = csv.reader(fr)
            headings = next(reader)
            for line in reader:
                string = line[1].strip('\"[] ')
                pattern = r'(<.*?>)'
                mi = re.findall(pattern, string)
                for item in mi:
                    all[item] = 1

    return list(all.keys())

def load_sdks(minsdk1):
    minsdkset = {}
    with open(minsdk1, "r") as fr:
        lines = fr.readlines()
        for line in lines:
            if line:
                sha256 = line.split(" ")[0]
                v = line.split(" ")[1]
                minsdkset[sha256] = int(v)
    return minsdkset


def row_count(filename):
    with open(filename) as in_file:
        return sum(1 for _ in in_file)


def check_and_mk_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
