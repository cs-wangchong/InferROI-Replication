import logging
import os
import re
import time
from collections import defaultdict

import openai
import spacy
from srctoolkit.javalang.parse import parse
from srctoolkit.javalang.tree import *

from app.cfg import CFG
from app.intention import Intention
from app.prompt import *

GPT_VERSION = "gpt-4-turbo-preview"
OPENAI_KEY = "Your Key"



INTENTION_TEMPLATE = re.compile(
    r"line (\d+|\d+-\d+)(:?.*?) (%s|%s|%s)s (.*?) resource" % (Intention.OPEN, Intention.CLOSE, Intention.VALIDATE),
    re.I
)


INVALID_RESOURCES = {
    "", "object", "string", "char", "int", "long", "short", "byte", "boolean", "bool", "float", "double",
    "word",
}


class LLM4Leak:
    def __init__(self, gpt_version=GPT_VERSION, openai_key=OPENAI_KEY, prompt_template=PROMPT_TEMPLATE, vote=5, retry=3): 
        self.gpt_version = gpt_version
        os.environ["OPENAI_API_KEY"] = openai_key
        openai.api_key = openai_key
        self.prompt_template = prompt_template
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe("merge_noun_chunks")
        self.retry = retry
        self.vote = vote

    def detect(self, code, consider_exception=True):
        leaks = dict()
        question, answer = None, None
        for _ in range(self.retry):
            try:
                question, answer = self.ask_llm(code)
            except openai.OpenAIError:
                time.sleep(5)
                continue
            break
        if answer is None:
            return question, answer, [], leaks
        intentions = self.parse_answer(code, answer)
        cfg = CFG.from_code(code)
        if len(cfg.nodes) == 0:
            return question, answer, intentions, leaks
        cfg.prune(intentions)
        cfg.enumerate_paths(intentions)
        leaks = cfg.detect(intentions, consider_exception=consider_exception)
        return question, answer, intentions, leaks

    def ask_llm(self, code):
        logging.info("ask llm for resource acquisition and release.")

        code_with_lineno = self.__add_line_numbers(code)
        response = openai.ChatCompletion.create(
            model=self.gpt_version,
            messages=[
                # {
                #     "role": "system",
                #     "content": SYSTEM_PROMPT
                # },
                {
                    "role": "user",
                    "content": self.prompt_template.format(code=code_with_lineno)
                }
            ],
            temperature=0,
            max_tokens=1024,
            # top_p=0,
            frequency_penalty=0,
            presence_penalty=0
        )
        question = self.prompt_template.format(code=code_with_lineno)
        answer = response['choices'][0]['message']["content"]
        logging.info(f'Q: \n{question}\n')
        logging.info(f'A: \n{answer}\n\n')
        return question, answer
    
    def __add_line_numbers(self, code):
        lines = []
        for lineno, line in enumerate(code.split('\n'), 1):
            lines.append(f'line {lineno}: {line}')
        return "\n".join(lines)

    def __rulebased_extract(self, code):
        validation_intentions = set()
        for lineno, line in enumerate(code.split("\n"), 1):
            mobj = re.search(r"if\s*\((.*?)(==|!=)\s*null\s*\)", line)
            if mobj is None:
                continue
            logging.info(f"line {lineno}: {mobj.group(0)}")
            logging.info(f"\t{(lineno, Intention.VALIDATE, mobj.group(1).strip())}")
            validation_intentions.add((lineno, mobj.group(1).strip()))
        return validation_intentions


    def parse_answer(self, code, answer):
        logging.info("parse answer for resource-oriented intentions.")
        type_map, ref_map = self.__get_decl_map(code)
        intentions = set()
        for searchObj in INTENTION_TEMPLATE.finditer(answer):
            if '-' in searchObj.group(1):
                lineno = int(searchObj.group(1).split('-')[0])
            else:
                lineno = int(searchObj.group(1))
            line, stmt, operation, resource  = searchObj.group(0), searchObj.group(2), searchObj.group(3), searchObj.group(4)
            if len(set(line.lower().split()) & {"no", "not"}) > 0:
                continue
            # logging.info(f"{line}\t{(lineno, operation, resource)")
            resource = self.__clean_resource(resource)
            if resource.lower() in INVALID_RESOURCES:
                continue
            resource, resource_type = self.__resolve_type(lineno, resource, type_map, ref_map)
            if resource_type.lower() in INVALID_RESOURCES:
                continue
            # logging.info(f"\t{(lineno, operation, resource)}")
            intentions.add((lineno, operation, resource, resource_type))
        for lineno, resource in self.__rulebased_extract(code):
            resource = self.__clean_resource(resource)
            if resource.lower() in INVALID_RESOURCES:
                continue
            resource, resource_type = self.__resolve_type(lineno, resource, type_map, ref_map)
            if resource_type.lower() in INVALID_RESOURCES:
                continue
            intentions.add((lineno, Intention.VALIDATE, resource, resource_type))
       
        intentions = list(intentions)
        intentions.sort(key=lambda item: item[0])
        logging.info(f'final intentions: {intentions}')
        return intentions
    
    def __clean_resource(self, resource):
        if resource.count("`") == 2:
            resource = re.search(r"`(.*?)`", resource).group(0)
        words = resource.replace("`", "").split()
        while len(words) > 0:
            if words[0].lower() in {"resource", "resources", "a", "an", "the", "open", "leakable", "acquired"}:
                words = words[1:]
            elif words[-1].lower() in {"resource", "resources", "a", "an", "the", "leakable"}:
                words = words[:-1]
            else:
                break
        return " ".join(words)
    
    def __resolve_type(self, lineno, resource, type_map, ref_map):
        # logging.info([lineno, resource, type_map, ref_map])
        types = set(type_map.values())
        if resource not in type_map and resource in types:
            resource_type = resource
            for ref in ref_map.get(lineno, set()):
                if type_map.get(ref) == resource_type:
                    resource = ref
                    break
        resource_type = type_map.get(resource, resource)
        return resource, resource_type
    
    def __get_decl_map(self, code):
        code = 'class Foo{\n' + code + '\n}'
        ast = parse(code)

        def __get_type(type):
            parts = []
            parts.append(type.name)
            while hasattr(type, 'sub_type') and type.sub_type:
                parts.append(type.sub_type.name)
                type = type.sub_type
            type_name = ".".join(parts)
            
            if hasattr(type, 'dimensions') and isinstance(type.dimensions, list) and len(type.dimensions) > 0:
                type_name += "[]" * len(type.dimensions)
            return type_name
        
            # generate declaration variables list
        type_map = dict()
        ref_map = defaultdict(set)
        for _, md in ast.filter((MethodDeclaration)):
            for parameter in md.parameters:
                type_map[parameter.name] = __get_type(parameter.type)
                ref_map[parameter.begin_pos.line - 1].add(parameter.name)
            for _, var in md.filter(LocalVariableDeclaration):
                for declarator in var.declarators:
                    type_map[declarator.name] = __get_type(var.type) 
                    ref_map[declarator.begin_pos.line - 1].add(declarator.name)
            for _, try_res in md.filter(TryResource):
                type_map[try_res.name] = __get_type(try_res.type)
                ref_map[try_res.begin_pos.line - 1].add(try_res.name)
            for _, ref in md.filter(MemberReference):
                ref_map[ref.begin_pos.line - 1].add(ref.member)
                if ref.qualifier:
                    ref_map[ref.begin_pos.line - 1].add(ref.qualifier)
            for _, mi in md.filter(MethodInvocation):
                if mi.qualifier:
                    ref_map[mi.begin_pos.line - 1].add(mi.qualifier)
        return type_map, ref_map
