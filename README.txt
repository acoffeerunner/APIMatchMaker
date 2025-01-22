==============================================================================================================================================================
========================================================================APISmartSelect========================================================================
==============================================================================================================================================================

1. Install dependencies using: pip install -r requirements.txt

2. Run the dataset-prep script using: python dataset-prep.py

3. Run the dataset-gen script using: python dataset-gen.py

4. Run the main script for the system using: python main.py

5. Once all dataset folds are processed by APIMatchmaker, run the Evaluation script for each dataset fold using: python Evaluation.py <dataset fold number>
For example, dataset fold 1 (in ./dataset/dataset_1) can be evaluated using: python Evaluation.py 1