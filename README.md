# APIMatchMaker

## Running steps

1. Install dependencies using: `pip install -r requirements.txt`

2. Run the dataset-prep script using: `python dataset-prep.py`

3. Run the dataset-gen script using: `python dataset-gen.py`

4. Run the main script for the system using: `python main.py`

5. Once all dataset folds are processed by APIMatchmaker, run the Evaluation script for each dataset fold using: `python Evaluation.py <dataset fold number>`.
   For example, dataset fold 1 (in ./dataset/dataset_1) can be evaluated using: `python Evaluation.py 1`
    

## The code structure

1. The *data-dump* folder contains a file that points to the url of the openly available dataset.

3. The *common* folder contains some basic functions, such as the crawler we used to collect the descriptions.

4. The *main* folder contains the contains the most core code, including the implementation of the approach.
