from common.file_ops import *
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from concurrent.futures import ProcessPoolExecutor
from gensim.parsing.preprocessing import remove_stopwords, strip_multiple_whitespaces, strip_non_alphanum, stem_text

class DescriptionSimCounter:
    def __init__(self, OPTIONS, custom_args, Threshold):
        self.OPTIONS = OPTIONS
        self.custom_args = custom_args
        self.Threshold = Threshold

    # preprocess func
    def preprocess(self, data):
        data = data
        data = data.lower()
        data = strip_multiple_whitespaces(data)
        data = strip_non_alphanum(data)
        data = remove_stopwords(data)
        data = stem_text(data)
        return data 

    def cosine_sim(self, text1, text2):
        vectorizer = TfidfVectorizer(input='filename', preprocessor=self.preprocess, max_features=2000)
        tfidf = vectorizer.fit_transform([text1, text2])
        return round((tfidf * tfidf.T).A[0, 1], 6)

    def process_similarity(self, apk):
        apk_hash = os.path.split(apk)[-1][:-4]
        test_desc_path = os.path.join(self.OPTIONS.description, apk_hash + ".txt")

        # Check if this hash has already been processed or not
        if os.path.exists(os.path.join(self.custom_args['Training_Set_filtered'], apk_hash + ".csv")):
            return
        
        try:
            self.OPTIONS.log_obj.debug(f"Starting description analysis of {apk_hash}")
            
            sim_map = {}
            flag = False
            training_set = self.custom_args['Training_Set']
            train_files = getFileList_from_txt(training_set)
            
            for train_file in train_files:
                train_filename = train_file
                train_desc_path = os.path.join(self.OPTIONS.description, train_filename + ".txt")
                score = self.cosine_sim(train_desc_path, test_desc_path)
            
                # add score to dict only if greater than defined thresh
                if score > self.Threshold:
                    sim_map[train_filename] = score
                    flag = True

            # write scores if similar apks were found in training set
            self.OPTIONS.log_obj.debug(f"Flag for {apk_hash}: {flag}")
            if flag:
                sim_lst = dict2sortedlist(sim_map)
                headings = ['Training file', 'similarity']
                self.OPTIONS.log_obj.debug(f"Writing similarity scores for {apk_hash}")
                writeScores(self.custom_args['Training_Set_filtered'], apk_hash, sim_lst, headings)
            self.OPTIONS.log_obj.info(f"Description analysis of {apk_hash} completed")

        except Exception as e:
            self.OPTIONS.log_obj.error(f"{e} encountered while performing description analysis for {apk_hash}")
            exit(1)

    def start(self):
        apks = getFileList(self.custom_args['Test_Set'], ".csv")
        self.OPTIONS.log_obj.info(f"Total test apks found: {len(apks)}")
        self.OPTIONS.log_obj.info(f"Processed results saved to {self.custom_args['Training_Set_filtered']}")
        
        args = [(apk) for apk in apks]

        n_workers = self.OPTIONS.maxjob - 1
        self.OPTIONS.log_obj.info(f"Starting {n_workers} workers for description similarity calculations")
        with ProcessPoolExecutor(max_workers=n_workers) as executor:
            executor.map(self.process_similarity, args)
