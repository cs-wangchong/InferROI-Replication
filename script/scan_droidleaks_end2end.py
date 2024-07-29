from pathlib import Path
import time
import re
import csv
import logging
import traceback
from tqdm import tqdm

from app.llms import ChatGPT
from app.prompts import PROMPT_FACTORY
from app.llm4leak import LLM4Leak
from app.logging_util import init_log_file

def clean_resource(resource):
    resource = resource.split("\n")[0].strip()
    resource = resource.split("(")[0].strip()
    if resource.count("`") == 2:
        resource = re.search(r"`(.*?)`", resource).group(0)
    words = resource.replace("`", "").split()
    while len(words) > 0:
        if words[0].lower() in {"resource", "resources", "a", "an", "the", "any", "open", "leakable", "acquired"}:
            words = words[1:]
        elif words[-1].lower() in {"resource", "resources", "a", "an", "the", "any", "leakable"}:
            words = words[:-1]
        else:
            break
    return " ".join(words)

def extract(answer):
    mobj = re.search(r"Leaky Resources[\W\n]*([\w, ]+)(\n|$)", answer, re.S|re.M|re.I)
    if not mobj:
        return set()
    logging.info(mobj.group(1))
    resource_types = {clean_resource(res).strip() for res in mobj.group(1).strip().split(",")}
    resource_types = {res for res in resource_types if res}
    return resource_types



if __name__ == "__main__":
    DATA_PATH = "data/DroidLeaks/DroidLeaks.csv"

    # MODEL = "gpt-4"
    MODEL = "gpt-4-turbo"
    # MODEL = "gpt-3.5-turbo"

    PROMPT = "gptleak"
    # PROMPT = "gptleak-roi"
    # PROMPT = "gptleak-exp"

    llm: ChatGPT = ChatGPT(MODEL, max_len=512)
    PROMPT_TEMPLATE = PROMPT_FACTORY[PROMPT]
    
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
        prompt = PROMPT_TEMPLATE.format(code=buggy_method)
        logging.info(prompt)
        answer = llm.query(prompt)
        logging.info(answer)
        time.sleep(5)
        leaked_types = extract(answer)
        logging.info(leaked_types)
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
        prompt = PROMPT_TEMPLATE.format(code=buggy_method)
        logging.info(prompt)
        answer = llm.query(prompt)
        logging.info(answer)
        time.sleep(5)
        leaked_types = extract(answer)
        logging.info(leaked_types)
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
        