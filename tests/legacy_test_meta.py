import ast
import unittest
from astMod import ASTWrapper, ASTNodeCreator
from astMod.modifier.decorator import DecoratorModifier
from pprint import pprint
from discord.ext import commands
class t_meta(unittest.TestCase):
    def test_1(self):
        deco : ast.Call = ASTNodeCreator._create_new_decorater(
            "commands.command",
            "x", "y", a=1, b=2,
        )
        pprint(ast.unparse(deco))

        dm = DecoratorModifier(deco)
        for a in dm.args:
            print(a.id)

        for k, v in dm.kwargs_modifier.items():
            print(f"{k}={ast.literal_eval(v)}")
        
        self.deco = deco
        self.dm = dm

    def test_2(self):
        self.test_1()
        self.dm.kwargs_modifier["a"] = 3
        self.dm.kwargs_modifier["abc"] = 4
        pprint(ast.unparse(self.deco))

        