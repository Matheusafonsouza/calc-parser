import re
import math
from lark import Lark, InlineTransformer, Token


grammar = Lark(
    r"""
    ?assign: NAME "=" comp
    ?start  : assign* comp?
    ?comp  : expr "<" expr  -> lt
        | expr "<=" expr -> le
        | expr ">" expr  -> gt
        | expr ">=" expr -> ge
        | expr "!=" expr -> ne
        | expr "==" expr -> eq
        | expr
    ?term  : term "*" pow   -> mul
        | term "/" pow   -> div
        | pow
    ?expr  : expr "-" term  -> sub
        | expr "+" term  -> add
        | term
    ?pow   : atom "^" pow   -> exp
        | atom
    ?atom  : NUMBER                        -> number
        | NAME "(" expr ")"             -> func
        | NAME "(" expr ("," expr)* ")" -> func
        | NAME                          -> var
        | "(" expr ")"
    NAME   : /[-+]?\w+/
    NUMBER : /-?(?:0|\d\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/
    %ignore /\s+/
    %ignore /\#.*/
""",
    parser="lalr",
)


class CalcTransformer(InlineTransformer):
    from operator import add, sub, mul, truediv as div, pow as exp, gt, ge, lt, le, ne, eq

    def __init__(self):
        super().__init__()
        self.vars = {}
        self.variables = {k: v for k, v in vars(math).items() if not k.startswith("_")}
        self.variables.update(max=max, min=min, abs=abs)

    def number(self, token):
        try:
            return int(token)
        except ValueError:
            return float(token)

    def assign(self, name_var, value):
        self.vars[name_var] = value
        return self.vars[name_var]

