import inspect
from pprint import pprint
from astplus import AstCreator, ValNotString
import unittest
import ast

class t_creator(unittest.TestCase):

    def test_create_new_args(self):
        l = lambda x: x + 1

        args = AstCreator.create_new_args(a="c", b=AstCreator.NotString("lambda x : x -1"), c=l)
        self.assertIsInstance(args, ast.arguments)
        self.assertEqual(len(args.args), 3)
        self.assertEqual(len(args.defaults), 3)
        
        self.assertEqual(args.args[0].arg, "a")
        self.assertEqual(args.defaults[0].value, "c")
        
        self.assertEqual(args.args[1].arg, "b")
        self.assertIsInstance(args.defaults[1], ast.Lambda)

        self.assertEqual(args.args[2].arg, "c")
        self.assertIsInstance(args.defaults[2], ast.Lambda)

        pprint(ast.unparse(args))

    def test_create_new_decorater(self):
        l = lambda x: x + 1
        dec = AstCreator.create_new_decorater("deco",a="c", b=l)
        self.assertIsInstance(dec, ast.Call)

        pprint(ast.unparse(dec))

    def test_create_new_func(self):
        dec = AstCreator.create_new_func(
            funcname="func1",
            funcBody=["print('hello')"],
            decorators=[AstCreator.create_new_decorater("deco", a="c", b=ValNotString("lambda x: x + 1"))],
            isAsync=True,
            arguments=AstCreator.create_new_args(a="c", b=ValNotString("lambda x: x + 1")),
        )

        pprint(ast.unparse(dec).split("\n"))