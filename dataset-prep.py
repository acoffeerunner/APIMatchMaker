import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from langdetect import detect
from gensim.parsing.preprocessing import strip_non_alphanum\

# remove any files that exist in description but don't exist in presolved
def get_commons_presolved(name, source_dirs):
    file_path = os.path.join(source_dirs[0], f"{name}.csv")
    if not os.path.exists(file_path):
        file_path = os.path.join(source_dirs[1], f"{name}.txt")
        os.remove(file_path)


# remove any files that exist in presolved but don't exist in description
def get_commons_descriptions(name, source_dirs):
    file_path = os.path.join(source_dirs[0], f"{name}.txt")
    if not os.path.exists(file_path):
        file_path = os.path.join(source_dirs[1], f"{name}.csv")
        os.remove(file_path)
    else:
        f = open(file_path, 'r')
        lang = detect(strip_non_alphanum(' '.join(f.readlines())))
        if(lang == 'en'):
            pass
        else:
            os.remove(file_path)
            file_path = os.path.join(source_dirs[1], f"{name}.csv")
            os.remove(file_path)

# multithreading for removing uncommon files
def process_get_commons(desc_file_list, presolved_file_list, source_dirs):
    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(
            get_commons_presolved, desc_file_list, [source_dirs] * len(desc_file_list)
        )
        executor.map(
            get_commons_descriptions,
            presolved_file_list,
            [source_dirs[::-1]] * len(presolved_file_list),
        )


# copy files from source to target (train/test)
def copy_files(name, source_dirs, target_dirs):
    file_path = os.path.join(source_dirs[0], f"{name}.csv")
    if os.path.exists(file_path):
        shutil.copy(file_path, target_dirs[0])
        file_path = os.path.join(source_dirs[1], f"{name}.txt")
        shutil.copy(file_path, target_dirs[1])


# multithreading for copying files to train/test
def process_copy_list(file_list, source_dirs, target_dirs):
    with ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(
            copy_files,
            file_list,
            [source_dirs] * len(file_list),
            [target_dirs] * len(file_list),
        )

if __name__ == '__main__':
    # description list
    descList = [i for i in os.walk("./data-dump/Description_fromGP")][0][2]
    descList = [i.split(".")[0] for i in descList]

    # presolved list
    presolvedList = [i for i in os.walk("./data-dump/Presolved")][0][2]
    presolvedList = [i.split(".")[0] for i in presolvedList]

    # source directories
    source_dirs = ["./data-dump/Presolved/", "./data-dump/Description_fromGP"]
    process_get_commons(descList, presolvedList, source_dirs)

    # total file count after getting commons
    total_file_count = len([i for i in os.walk("./data-dump/Presolved")][0][2])
    print(f"{total_file_count} usable data points found.")

    # target directories
    target_dirs = ["./data/Presolved_test/", "./data/Description_fromGP_test/"]


    # create data directory
    if not os.path.exists("./data"):
        os.mkdir("./data")

    # create test target directories if they do not exist
    if not os.path.exists(target_dirs[0]):
        os.mkdir(target_dirs[0])

    if not os.path.exists(target_dirs[1]):
        os.mkdir(target_dirs[1])


    # copy test data
    minSdkList = open("minSdkVersion.txt", "r")
    sha256List = minSdkList.readlines()
    sha256List = [i.split()[0] for i in sha256List]
    print(str(len(sha256List)) + " testing data points found from minSdkList.")
    process_copy_list(sha256List, source_dirs, target_dirs)
    testDescList = [i for i in os.walk("./data/Description_fromGP_test")][0][2]
    testDescList = [i.split(".")[0] for i in testDescList]
    print(f"{str(len(testDescList))} testing data points found.")


    target_dirs = ["./data/Presolved_train/", "./data/Description_fromGP_train/"]

    # create train target directories if they do not exist
    if not os.path.exists(target_dirs[0]):
        os.mkdir(target_dirs[0])

    if not os.path.exists(target_dirs[1]):
        os.mkdir(target_dirs[1])



    # copy training data
    process_copy_list(descList, source_dirs, target_dirs)
    descList = [i for i in os.walk("./data/Description_fromGP_train")][0][2]
    descList = [i.split(".")[0] for i in descList]
    print(f"{str(len(descList))} training data points copied.")
