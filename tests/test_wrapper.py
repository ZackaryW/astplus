import ast
from pprint import pprint
import unittest
from astplus import AstWrapper
from astplus.ext import AstPlusArg

class t_wrapper(unittest.TestCase):
    def test_1(self):
        self.awrapper = AstWrapper.fromModule('tests.src.a')
        pprint(self.awrapper.sourcelines)
        self.assertTrue(True)

    def test_2(self):
        self.awrapper = AstWrapper.fromModule('tests.src.a')
        for x in self.awrapper.visitor.visit_FunctionDef():
            x : ast.FunctionDef
            if x.name == "func2":
                args = AstPlusArg.fromFunc(x)
                for k, v in args.kwargItems():
                    print(k)
    