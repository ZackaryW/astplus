import inspect
from pprint import pprint
import unittest
import ast
from itertools import chain, product
from astMod.wrapper import ASTWrapper, ASTNodeCreator
from astMod.modifier.decorator import DecoratorModifier

class misc(unittest.TestCase):
    def test_1(self):
        self.aw = ASTWrapper(filename='test_src/a.py')
        for node, lv in self.aw.visit_FunctionDef(dig=True, yield_lv=True):
            node : ast.AST
            print(f"{lv} - {node.name}")
            functionaw = ASTWrapper(node)
            try:
                if len(functionaw.ast_tree.args.args) > 0:
                    for i in range(len(functionaw.ast_tree.args.args)):
                        print(f"{functionaw.ast_tree.args.args[i].arg} = {functionaw.ast_tree.args.defaults[i].value}" )
                        functionaw.ast_tree.args.defaults[i].value = None
            except Exception as e:
                print(e)
        
        pprint(self.aw.sourcelines)
        
    def test_2(self):
        self.aw = ASTWrapper(filename='test_src/b.py')
        for x in self.aw.visit_AsyncFunctionDef(dig=True):
            x : ast.AsyncFunctionDef
            x1 = ASTWrapper(x)
            for y in x1.visit_decorator_list():
                y1 = DecoratorModifier(y, parent=x)
                print(y1.name)
                y1.name = "dowhatever." + y1.name.split('.')[-1]
                print(y1.name)
        
        pprint(self.aw.sourcelines)

