import logging
import re
from collections import defaultdict

from srctoolkit.dependency_analyzer import DependencyAnalyzer
from srctoolkit.javalang.parse import parse
from srctoolkit.javalang.tree import IfStatement, MethodDeclaration

from app.intention import Intention

ANALYZER = DependencyAnalyzer()

EXIT = "exit"
EXIT_LINE = -99999

class CFG:
    def __init__(self, nodes, edges, node_lines, node_descs, code, ast):
        self.nodes = nodes
        self.edges = edges
        self.node_lines = node_lines
        self.node_descs = node_descs
        self.code_lines = [line.strip() for line in code.split("\n")]
        self.ast = ast
        self.initilize()
        
    @classmethod
    def from_code(cls, code):
        wrapped_code = 'class Foo{\n' + code + '\n}'
        nodes, edges = [], []
        node_lines, node_descs = [], []
        try:
            ast = parse(wrapped_code)
            cfg_json = ANALYZER.build_cfg(wrapped_code)[0]
        except Exception:
            return cls(nodes, edges, node_lines, node_descs, code, None)  
        
        special_counter = 0
        for node in cfg_json['nodes']:
            nodes.append(node['id'])
            if node['line'] > 0:
                node_line = node['line'] - 1
            else:
                special_counter += 1
                node_line = -special_counter
            node_lines.append(node_line)
            node_descs.append(node['label']) 
        nodes.append(len(nodes))
        node_lines.append(EXIT_LINE)
        node_descs.append(EXIT)
        for edge in cfg_json['edges']:
            src, tgt = edge['source'], edge['target']
            edges.append((src, tgt))
        return cls(nodes, edges, node_lines, node_descs, code, ast)  

 
    def initilize(self):
        self.lineno2node = defaultdict(list)
        for node_id, line in enumerate(self.node_lines):
            # logging.debug(f"node id: {node_id}, line no: {line}")
            self.lineno2node[line].append(node_id)
        for lineno, line in enumerate(self.code_lines, 1):
            if lineno in self.lineno2node:
                continue
            line = re.sub(r"\s", "", line.strip().strip("{};"))
            # logging.info(f"line {lineno}: {line}")
            for cfg_node, cfg_lineno, cfg_desc in zip(self.nodes, self.node_lines, self.node_descs):
                if line in re.sub(r"\s", "", cfg_desc) and cfg_lineno < lineno:
                    self.lineno2node[lineno].append(cfg_node)
                    break

        self.inedge_lines = defaultdict(set)
        self.outedge_lines = defaultdict(set)
        for src, tgt in self.edges:
            # print(f"src: `{self.node_lines[src]}: {self.node_descs[src]}`, tgt: `{self.node_lines[tgt]}: {self.node_descs[tgt]}`")
            self.inedge_lines[self.node_lines[tgt]].add(self.node_lines[src])
            self.outedge_lines[self.node_lines[src]].add(self.node_lines[tgt])
        self.if_lines = dict()
        if self.ast is not None:
            for _, ifstmt in self.ast.filter(IfStatement):
                # logging.debug(f"if-statement: {ifstmt.begin_pos.line}")
                if ifstmt.begin_pos and re.match(r"if(\s|\()", self.code_lines[ifstmt.begin_pos.line - 1]):
                    self.if_lines[ifstmt.begin_pos.line - 1] = ifstmt.end_pos.line - 1
        # logging.info(f"outedges: {self.outedge_lines}")
        # logging.info(f"if lines: {self.if_lines}")

    def prune(self, intentions): 
        logging.info("start pruning cfg")
        # expand loop
        for src_line, tgt_lines in self.outedge_lines.items():
            for tgt_line in tgt_lines.copy():
                if self.node_descs[self.lineno2node[src_line][0]] == "end-catch" and self.node_descs[self.lineno2node[tgt_line][0]] == "end-try":
                    tgt_lines.remove(tgt_line)
                    end_try_next_lines = self.outedge_lines[tgt_line]
                    if len(end_try_next_lines) == 1:
                        end_try_next_lines.add(EXIT_LINE)
                    for l in end_try_next_lines:
                        if l != src_line:
                            self.outedge_lines[src_line].add(l)
                if src_line == tgt_line:
                    tgt_lines.remove(tgt_line)
                    continue
                if tgt_line < 0:
                    continue
                while src_line < 0 and src_line in self.inedge_lines:
                    src_line = max(self.inedge_lines[src_line])
                
                if src_line > tgt_line:
                    tgt_lines.remove(tgt_line)
                    for l in self.outedge_lines[tgt_line]:
                        if l < 0:
                            tgt_lines.add(l)
                            break
        # logging.info(f"outedges: {self.outedge_lines}")
        # merge if-branches
        op_linenos = set()
        for lineno, op, _, _ in intentions:
            if op in {Intention.OPEN, Intention.CLOSE}:
                op_linenos.add(lineno)
            
        def should_prune(cur_line, e_line, visited):
            if cur_line in visited:
                return True
            visited.add(cur_line)
            if "return" in self.code_lines[cur_line - 1].split() or cur_line in op_linenos:
                return False
            for out_line in self.outedge_lines[cur_line]:
                if out_line > e_line:
                    continue
                if not should_prune(out_line, e_line, visited):
                    return False
            return True
        
        for s_line, e_line in self.if_lines.items():
            if not should_prune(s_line, e_line, set()):
                continue
            if len(self.outedge_lines[s_line]) > 1:
                self.outedge_lines[s_line] = {self.outedge_lines[s_line].pop()}

        # logging.info(f"outedges after pruning: {self.outedge_lines}")
        
        
    def desc_path(self, path):
        s = []
        for node in path:
            s.append(f'line {self.node_lines[node] if self.node_lines[node] > 0 else "x"}: {self.node_descs[node]}')
        return "-> " + "\n\t-> ".join(s)

        # start_node = f'line {self.node_lines[path[0]] if self.node_lines[path[0]] > 0 else "x"}: {self.node_descs[path[0]]}'
        # end_node = f'line {self.node_lines[path[-1]] if self.node_lines[path[-1]] > 0 else "x"}: {self.node_descs[path[-1]]}'
        # return start_node if start_node == end_node else f'{start_node} -> {end_node}'
        
    
    def get_paths_between_two_nodes(self, start_node, end_node): 
        paths = []   
        def dfs(cur_node, cur_path):
            if cur_node in cur_path:
                return
            # print([self.node_lines[n] for n in cur_path])
            cur_path.append(cur_node) 
            if cur_node == end_node:
                paths.append(cur_path.copy())
            for node_line in self.outedge_lines[self.node_lines[cur_node]]: 
                for n in self.lineno2node[node_line]:
                    dfs(n, cur_path)
            cur_path.pop()
        dfs(start_node, [])
        return paths
    
 
    def enumerate_paths(self, intentions):
        logging.info("start enumerating paths")
        start_nodes, end_nodes = [], []

        for lineno, op, res, t_res in intentions:
            if op == Intention.OPEN:
                # handle try_with_resources
                if not any(self.node_descs[node_index].__contains__('try') for node_index in self.lineno2node[lineno]):
                    start_nodes.extend(self.lineno2node[lineno])
        for node in self.nodes:
            if len(self.outedge_lines[self.node_lines[node]]) == 0:
                end_nodes.append(node)
        self.all_paths = []
        for start_node in start_nodes:
            for end_node in end_nodes:
                # logging.info(f"start: `{self.node_descs[start_node]}`, end: `{self.node_descs[end_node]}`")
                # logging.info(f"start: `{self.node_lines[start_node]}`, end: `{end_node}`")
                paths = self.get_paths_between_two_nodes(start_node, end_node)
                for path in paths:
                    stmts = [self.node_descs[node].strip().split()[0] for node in path]
                    stmt_set = set(stmts)
                    if "return" in stmt_set and "end-finally" in stmt_set:
                        last_idx = len(path) - 1
                        for idx in range(last_idx - 1, -1, -1):
                            if stmts[idx] == "end-finally":
                                last_idx = idx
                                break
                        path = path[:last_idx + 1]
                    # logging.info(f"path: {[self.node_descs[n] for n in path]}")
                    self.all_paths.append(tuple(path))
            
    def detect_for_one_resource(self, intentions):
        # use node instead of lineno, as one node maybe correspond to multiple lines
        acq_nodes, rel_nodes, val_nodes = set(), set(), set()
        for lineno, operation, resource, _ in intentions:
            nodes = self.lineno2node[lineno]
            if operation == Intention.OPEN:
                acq_nodes.update(nodes)
            elif operation == Intention.CLOSE:
                rel_nodes.update(nodes)
            elif operation == Intention.VALIDATE and any([re.match(r"if(\s|\()", self.node_descs[node].strip()) for node in nodes]):
                val_nodes.update(nodes)

        logging.info(f'acq_nodes: {acq_nodes}\n, rel_nodes: {rel_nodes}\n, val_nodes: {val_nodes}')
        
        leaky_map = dict()
        validation_map = defaultdict(list)
        for path in self.all_paths:
            # logging.info(f"####################\npath:\n\t{self.desc_path(path)}")
            if len(acq_nodes) <= 0 :
                continue
            if path[0] != min(acq_nodes):
                continue
            counter = 0
            for idx, node in enumerate(path):
                # logging.info(f'node is {node} {self.node_descs[node]}')
                if node in acq_nodes:
                    counter += 1
                elif node in rel_nodes:
                    counter -= 1
                elif node in val_nodes:
                    validation_map[path[:idx+1]].append(path)
            if counter > 0:
                leaky_map[path] = True
                # logging.info(f"potential leak of `{resource}` in this path")
            else:
                leaky_map[path] = False
        # logging.info(['leaky map', leaky_map])
        # logging.info(['validation_map', validation_map])
        for prefix, paths in sorted(validation_map.items(), key=lambda pair: self.node_lines[pair[0][-1]], reverse=True):
            branches = defaultdict(list)
            for path in paths:
                branches[path[:len(prefix) + 1]].append(path)
            branches = list(branches.values())
            # logging.info(f"line {self.node_lines[prefix[-1]]}: branch number: {len(branches)}")
            if len(branches) != 2:
                continue
            branch1, branch2 = branches
            if all(leaky_map[path] for path in branch1) and all(not leaky_map[path] for path in branch2):
                for path in branch1:
                    leaky_map[path] = False
            if all(not leaky_map[path] for path in branch1) and all(leaky_map[path] for path in branch2):
                for path in branch2:
                    leaky_map[path] = False

        leaky_paths = list(set(path for path, leaky in leaky_map.items() if leaky))
        return leaky_paths
    
    def is_leaky_caused_by_exception(self, intentions):
        if all(md.throws is None for _, md in self.ast.filter(MethodDeclaration)):
            return False
        # check whether resource is closed in finally-block
        for lineno, operation, resource, _ in intentions:
            leaky = True
            cur_line = lineno
            if operation != Intention.CLOSE:
                continue
            visited_nodes = set()
            while cur_line in self.inedge_lines:
                node_id = self.lineno2node[cur_line][0]
                visited_nodes.add(node_id)
                if self.node_descs[node_id] == "finally":
                    leaky = False
                    break
                in_lines = [l for l in self.inedge_lines[cur_line] if l <= cur_line and self.lineno2node[l][0] not in visited_nodes]
                if len(in_lines) == 0:
                    break
                cur_line = in_lines[0]
            if leaky:
                return True
        
        return False

            
    def detect(self, intentions, consider_exception=True):
        logging.info("start detecting leaks")
        # for node in self.nodes:
        #     logging.info(f'line: {self.node_lines[node]} {self.node_descs[node]}')
        res2intentions = defaultdict(list)
        res2type = dict()
        for lineno, operation, resource, resource_type in intentions:
            res2intentions[resource].append((lineno, operation, resource, resource_type))
            res2type[resource] = resource_type
        
        leaks = defaultdict(set)
        for resource, res_intentions in res2intentions.items():
            leaky_paths = self.detect_for_one_resource(res_intentions)
            formatted_leaky_paths = [self.desc_path(path) for path in leaky_paths]
            leaks[resource].update(formatted_leaky_paths)
        if consider_exception:
            for resource, res_intentions in res2intentions.items():
                if len(leaks[resource]) == 0 and self.is_leaky_caused_by_exception(res_intentions):
                    leaks[resource].update("potiential resource leaks caused by unhandled exception")
        leaks = {
            res: {
                "type": res2type.get(res, res),
                "paths": list(paths)
            }
            for res, paths in leaks.items() if len(paths) > 0
        }

        logging.info("#" * 50)
        logging.info(f'detect {len(leaks)} resource leaks: {[leak["type"] for _, leak in leaks.items()]}')
        # for resource, leaky_paths in leaks.items():
        #     formatted_paths = "\n".join(f"path-{i}:\n\t{p}" for (i, p) in enumerate(leaky_paths, 1))
            # logging.info(f'leaks of `{resource}`, leaky paths:\n{formatted_paths}')
        return leaks
      