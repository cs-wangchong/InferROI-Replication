from pathlib import Path
import time
import re
import csv
import logging
import traceback
from tqdm import tqdm

from app.llms import LLM_FACTORY
from app.prompts import PROMPT_FACTORY
from app.llm4leak import LLM4Leak
from app.logging_util import init_log_file



if __name__ == "__main__":
    DATA_PATH = "data/DroidLeaks/DroidLeaks.csv"

    # MODEL = "gpt-4"
    # MODEL = "gpt-4-turbo"
    # MODEL = "gpt-3.5-turbo"
    # MODEL = "llama-3-8b"
    MODEL = "gemma-2-9b"

    PROMPT = "inferroi-paper"

    detector = LLM4Leak(llm=LLM_FACTORY[MODEL](), prompt_template=PROMPT_FACTORY[PROMPT])
    init_log_file(f"log/droidleaks-{MODEL}-{PROMPT}.log")

    instances = []
    with open(DATA_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            instances.append(row)

    tp, fp, fn = 0, 0, 0

    for id, inst in tqdm(list(enumerate(instances, 1))):
        buggy_method, fixed_method = inst['Buggy content'], inst['Fix content']
        
        resource_types = {inst['Concerned class'].strip().split(".")[-1]}
        logging.info(f"########### ID-{id} ###########")
        logging.info(f"resource type: {resource_types}")

        logging.info("###### BUGGY METHOD ######")
        logging.info(buggy_method)
        _, _, _, leaks = detector.detect(buggy_method, consider_exception=False, post_filtering=False)
        time.sleep(5)
        leaked_types = {leak["type"].split(".")[-1] for leak in leaks.values()}
        normalized_leaked_types = set()
        for leaked_type in leaked_types:
            leaked_type:str
            if leaked_type[0].islower() and leaked_type not in resource_types:
                for resource_type in resource_types:
                    if resource_type.lower() in leaked_type.lower():
                        resource_type = resource_type
            normalized_leaked_types.add(leaked_type)
        leaked_types = normalized_leaked_types

        logging.info(resource_types & leaked_types)
        if len(resource_types & leaked_types) > 0:
            tp += 1
        else:
            fn += 1
        logging.info("###### FIXED METHOD ######")
        logging.info(fixed_method)
        _, _, _, leaks = detector.detect(fixed_method, consider_exception=False, post_filtering=False)
        time.sleep(5)
        leaked_types = {leak["type"].split(".")[-1] for leak in leaks.values()}
        normalized_leaked_types = set()
        for leaked_type in leaked_types:
            leaked_type:str
            if leaked_type[0].islower() and leaked_type not in resource_types:
                for resource_type in resource_types:
                    if resource_type.lower() in leaked_type.lower():
                        resource_type = resource_type
            normalized_leaked_types.add(leaked_type)
        leaked_types = normalized_leaked_types
        logging.info(resource_types & leaked_types)
        if len(resource_types & leaked_types) > 0:
            fp += 1

        logging.info(f"tp: {tp}, fp: {fp}, fn: {fn}")
        logging.info(f"precision: {(tp / (tp + fp)) if tp > 0 else 0.}, recall: {(tp / (tp + fn)) if tp > 0 else 0.}")
        