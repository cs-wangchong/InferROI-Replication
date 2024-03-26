import openpyxl
import traceback
from app.llm4leak import LLM4Leak
from app.logging_util import init_log_file
import logging
import time


init_log_file("log/open-source.log")

app = LLM4Leak("gpt-4")


workbook = openpyxl.load_workbook('data/SampledMethods.xlsx')
sheet = workbook['methods']

bug_methods = set()
for func_name, func_code, resource, path, start_line, end_line in sheet.iter_rows(values_only=True):
    if path is None or not isinstance(path, str) or "/" not in path:
        continue
    try:
        path = "/".join([path.split("/")[5].split("#")[1]] + path.split("/")[6:])
    except Exception:
        traceback.print_exc()
        continue

    func_code = func_code.replace("&#10;", "\n")
    _, _, _, leaks = app.detect(func_code, consider_exception=True)
    time.sleep(5)
    if len(leaks) > 0:
        logging.info(f"########### REPORTED BUG ###########")
        logging.info(f"path: {path}")
        logging.info(f"method: \n{func_code}")


    
