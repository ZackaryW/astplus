import unittest
import ast
from astplus import AstCreator, ValNotString
from astplus.ext import AstPlusDecorator

class t_poc(unittest.TestCase):
    def test_poc_0(self):
        x = ast.parse("lambda x: x + 1", mode="eval")
        pass

    def test_poc_1(self):
        dec = AstCreator.create_new_decorater("deco", "c", a="c", b=ValNotString("lambda x: x + 1"))
        print(ast.unparse(dec))
        
        wdec = AstPlusDecorator(dec)
        for k, v in wdec.kwargs.items():
            print(k, v)

        pass