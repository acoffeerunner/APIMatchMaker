# coding:utf-8
from main.ProjectSimCounter import ProjectSimCounter
from main.DescriptionSimCounter import DescriptionSimCounter
from main.ContextAwareRecommendation import ContextAwareRecommendation
from main.Evaluation import Evaluation
import time


class Runner:
    def __init__(self, OPTIONS, custom_args):
        self.OPTIONS = OPTIONS
        self.custom_args = custom_args

    def start(self):
        start_time = time.time()
        # print("[+] Starting ... ")

        # # (1)

        self.OPTIONS.log_obj.info("Calculating description similarities")
        descriptionSimCounter = DescriptionSimCounter(self.OPTIONS, self.custom_args, 0)
        descriptionSimCounter.start()
        self.OPTIONS.log_obj.info("Description similarities calculated")

        # Compute similarity between projects
        self.OPTIONS.log_obj.info("Calculating method similarities")
        projectSimCounter = ProjectSimCounter(self.OPTIONS, self.custom_args)
        projectSimCounter.computeProjectSimilarity()
        self.OPTIONS.log_obj.info("Method similarities calculated")
        
        # Recommendation processing
        self.OPTIONS.log_obj.info("Starting recommendation engine")
        contextAwareRecommendation = ContextAwareRecommendation(self.OPTIONS, self.custom_args, 10, 6, 6, 1, 0)
        contextAwareRecommendation.recommendation()
        self.OPTIONS.log_obj.info("Recommendations written to directory!")
        

        # Evaluation @1, @5, @10, @15, @20
        self.OPTIONS.log_obj.info("Evaluating results")
        
        self.OPTIONS.log_obj.debug("Evaluating results @1")
        evaluation = Evaluation(self.OPTIONS, self.custom_args, 1)
        evaluation.start()
        self.OPTIONS.log_obj.debug("Evaluation of results @1 completed")

        self.OPTIONS.log_obj.debug("Evaluating results @5")
        evaluation = Evaluation(self.OPTIONS, self.custom_args, 5)
        evaluation.start()
        self.OPTIONS.log_obj.debug("Evaluation of results @5 completed")

        self.OPTIONS.log_obj.debug("Evaluating results @10")
        evaluation = Evaluation(self.OPTIONS, self.custom_args, 10)
        evaluation.start()
        self.OPTIONS.log_obj.debug("Evaluation of results @10 completed")

        self.OPTIONS.log_obj.debug("Evaluating results @15")
        evaluation = Evaluation(self.OPTIONS, self.custom_args, 15)
        evaluation.start()
        self.OPTIONS.log_obj.debug("Evaluation of results @15 completed")

        self.OPTIONS.log_obj.debug("Evaluating results @20")
        evaluation = Evaluation(self.OPTIONS, self.custom_args, 20)
        evaluation.start()
        self.OPTIONS.log_obj.debug("Evaluation of results @20 completed")

        self.OPTIONS.log_obj.info("Evaluation completed")

        end = time.time()
        running_time = end - start_time
        self.OPTIONS.log_obj.info(f"Fold run completed in {running_time:.2f} seconds")


