import ast
import typing

class AstVisitor(ast.NodeVisitor):
    def __init__(self, node : ast.AST) -> None:
        super().__init__()
        self._node = node

    def __getattribute__(self, name: str):
        if not name.startswith('visit_'):
            return super().__getattribute__(name)

        objname = name[6:]
        newobjname = objname.split('_')[0]

        if hasattr(self._node, objname) or hasattr(self._node, newobjname):
            return lambda *args, **kwargs: self._visit_generic(loopattr=objname, *args, **kwargs)

        if hasattr(ast, name[6:]):
            obj = getattr(ast, objname)
            return lambda *args, **kwargs: self._visit_generic(type=obj, *args, **kwargs)
    def _visit_generic(
        self, 
        target : ast.AST= None,  
        type : ast.AST = None,
        loopattr : str = "body",
        dig : bool = False, 
        max_recurs : int = 3,
        base_recurs : int = 0,
        yield_lv : bool = False,
    ):
        
        if target is None:
            target = self._node
        
        try:
            looptarget = getattr(target, loopattr)
        except:
            looptarget = target

        #if not iterable 
        if not isinstance(looptarget, typing.Iterable):
            # split into a list
            loopattrs = loopattr.split('_')
            
            for attr in loopattrs:
                if hasattr(looptarget, attr):
                    looptarget = getattr(looptarget, attr)
                else:
                    raise AttributeError(f"{attr} not found")

        for node in looptarget:
            if (type and isinstance(node, type)) or not type:
                if yield_lv:
                    yield node, base_recurs
                else:
                    yield node
            if dig and max_recurs > 0 and hasattr(node, loopattr):
                for child in self._visit_generic(
                    type=type,
                    target=node,
                    loopattr=loopattr,
                    dig=dig,
                    max_recurs=max_recurs-1,
                    base_recurs=base_recurs+1,
                    yield_lv=yield_lv
                ):
                    
                    yield child

    def visit(self, target :str = "body"):
        node = getattr(self._node, target, None)
        if node is None or not isinstance(node, typing.Iterable):
            return
        for x in node:
            yield x
