from pathlib import Path
import time
import re
import csv
import logging
import json
from tqdm import tqdm


from app.llms import LLM_FACTORY
from app.prompts import PROMPT_FACTORY
from app.llm4leak import LLM4Leak
from app.logging_util import init_log_file



if __name__ == "__main__":
    with Path("data/Lucene-100.json").open("r") as f:
        methods = [tuple(item) for item in json.load(f)]

    MODEL = "gpt-4"
    PROMPT = "inferroi-paper"


    detector = LLM4Leak(llm=LLM_FACTORY[MODEL](), prompt_template=PROMPT_FACTORY[PROMPT])
    init_log_file(f"log/lucene-100-{MODEL}-{PROMPT}.log")

    for path, _, code, _, _ in methods:
        func_code = code.replace("&#10;", "\n")
        _, _, _, leaks = detector.detect(func_code, consider_exception=True)
        time.sleep(5)
        if len(leaks) > 0:
            logging.info(f"########### REPORTED BUG ###########")
            logging.info(f"path: {path}")
            logging.info(f"method: \n{func_code}")