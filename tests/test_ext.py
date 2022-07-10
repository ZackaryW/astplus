from pprint import pprint
import unittest
from astplus import AstWrapper, ValNotString
from astplus.ext import AstPlusFunc

class t_ext_arg(unittest.TestCase):
    def test_1(self):
        self.awrapper = AstWrapper.fromModule('tests.src.a')
        for x in self.awrapper.visitor.visit_FunctionDef():
            break
        
        ax = AstPlusFunc(x)
        print(ax.name)

        kwargs = ax.kwargs
        turn_keys = []
        for k, v in kwargs.kwargItems():
            turn_keys.append(k)

        for i, key in enumerate(turn_keys):
            kwargs[key] = ValNotString(f"lambda x: x + {i+1}")

        pprint(ax.sourcelines.split("\n"))