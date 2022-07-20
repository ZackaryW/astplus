import ast
import inspect
from re import L
import typing

class AstCreator:
    """
    this class does not have any associated methods except for grouping all the ast creation methods
    """

    class NotString:
        """
        this class is used to represent a value that is not a string
        """

        def __init__(self, value) -> None:
            self.value = value

    @staticmethod
    def toSrc(val):
        if isinstance(val, str):
            return f'"{val}"'
        elif isinstance(val, AstCreator.NotString):
            return val.value
        elif isinstance(val, typing.Callable):
            asrc = ast.parse(inspect.getsource(val).strip())
            src_target = asrc.body[0].value
            return src_target
        elif isinstance(val, ast.AST):
            return val
        else:
            return str(val)
    
    @staticmethod
    def create_new_node(string : str, mode = "eval") -> ast.AST:
        return ast.parse(string, mode=mode).body[0]

    @staticmethod
    def create_new_decorater(name : str, *args,vararg = None, kwvarg= None,  **kwargs) -> ast.Call:
        if not isinstance(name, str):
            raise Exception("name must be str")

        pending = {}

        line = f"@{name}("
        line += ", ".join(map(str, args))
        if len(kwargs) > 0 and len(args)>0:
            line += ", "


        subline = ""
        for k, v in kwargs.items():
            vk = AstCreator.toSrc(v)
            if isinstance(vk, ast.AST):
                pending[k] = vk
            else:
                subline += f"{k}={vk},"

        line = line + subline + ","
        line = line.rstrip(",")

        if vararg is not None:
            line += f",*{vararg}"
        if kwvarg is not None:
            line += f",**{kwvarg}"
        line = line.rstrip(",")
        line += ")"
        line += "\ndef test():\n    pass"
        
        astc : ast.Call= ast.parse(line).body[0].decorator_list[0]

        for k, v in pending.items():
            astc.keywords.append(ast.keyword(arg=k, value=v))

        return astc 

    @staticmethod
    def create_new_kwarg_constant(**kwargs) -> ast.Constant:
        return [ast.keyword(
            arg=k,
            value=ast.Constant(value=v),
        ) for k,v in kwargs.items()]

    @staticmethod
    def create_new_args(*args, **kwargs):

        pending = {}

        line = "def test("
        line += ", ".join(map(str, args))
        if len(kwargs) > 0 and len(args) > 0:
            line += ", "
        for k, v in kwargs.items():
            vk = AstCreator.toSrc(v)
            if isinstance(vk, ast.AST):
                pending[k] = vk
            else:
                line += f"{k}={vk}, "
        line += "):\n    pass\n"

        astc = ast.parse(line)
        func_args : ast.arguments= astc.body[0].args

        for k, v in pending.items():
            func_args.args.append(ast.arg(arg=k))
            func_args.defaults.append(v)

        return func_args
    
    @staticmethod
    def create_new_func(
        funcname, 
        decorators : typing.List[ast.Call],
        arguments : ast.arguments,
        isAsync : bool = False,
        funcBody : typing.List[str] = None,
        funcBodyAst : typing.List[ast.AST] = None,
    ):    
        line = f"{'async ' if isAsync else ''}def {funcname}("
        line += ast.unparse(arguments)
        line += "):\n"

        if funcBody:
            for x in funcBody:
                line += " "*4+f"{x}\n"

        line += "    pass\n"
        func_ast = ast.parse(line).body[0]
        func_ast.decorator_list = decorators

        if funcBodyAst:
            func_ast.body = funcBodyAst

        return func_ast

    @staticmethod
    def create_new_arguments_arg(key, value =None):
        arg = ast.arg(arg=key)

    