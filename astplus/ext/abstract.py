import ast
from dataclasses import dataclass
import typing

@dataclass(frozen=True)
class AstPlusUniversal:
    """
    a more readable ast object that can be used to modify and traverse the ast
    """

    astObj : ast.AST
    parent : ast.AST = None

    def _inplace_parent_replace(self, obj, replacement_obj, parent_attr: str = "body"):
        if self.parent is None:
            raise Exception("Parent is None")

        parent_c = getattr(self.parent, parent_attr)
        if parent_c is None:
            raise Exception(f"Parent has no {parent_attr}")

        if not isinstance(parent_c, typing.Iterable):
            raise Exception(f"Parent {parent_attr} is not iterable")

        for i, x in enumerate(parent_c):
            if x is obj:
                ast.copy_location(replacement_obj, obj)
                parent_c[i] = replacement_obj
                break
        
        self.astObj = replacement_obj

    def _setattr(self, name: str, value):
        object.__setattr__(self, name, value)

    @property
    def sourcelines(self):
        return ast.unparse(self.astObj)

@dataclass(frozen=True)
class AstPlusInterface(AstPlusUniversal):
    pass

@dataclass(frozen=True)
class AstPlusIterableInterface(AstPlusUniversal):
    def __post_init__(self):
        if not isinstance(self.astObjs, typing.Iterable):
            raise Exception("astObjs is not iterable")

