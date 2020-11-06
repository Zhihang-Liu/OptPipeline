from typing import Callable, Type, TypeVar, Any
from ast import expr, stmt, AST, FunctionDef, ClassDef, Attribute


class Pos:
    lineno: int
    col_offset: int

    def __init__(self, i: AST):
        self.col_offset = i.col_offset
        self.lineno = i.lineno


class InvalidExpression(RuntimeError):
    pos: Pos
    def __init__(self, i: AST):
        self.pos = Pos(i)

class UserAST:...

FilterFunction = Callable[[AST], AST]

# def type_bind_optional(tp: type, op: FilterFunction) -> FilterFunction:
    # def r(i: Any) -> UserAST:
        # if isinstance(i, tp):
            # return op(i)
        # else:
            # raise InvalidExpression(i)
    # return r

def union_p(a: Callable, b: Callable) -> Callable[[AST], AST]:
    def f(i: AST) -> AST:
        try:
            return a(i)
        except InvalidExpression:
            return b(i)
    return f

def match_row_filter(i: Attribute) -> Attribute:
    if i.attr != 'row_filter':
        raise InvalidExpression(i)
    return i

def match_line_filter(i: Attribute) -> Attribute:
    raise InvalidExpression(i)

match_any_filter = union_p(match_row_filter, match_line_filter)

def identity(i: AST) -> AST:
    return i


def filter_stmt(i: stmt) -> stmt:
    r = {
        FunctionDef: identity,
        ClassDef: identity,
    }
    raise InvalidExpression(i)

def filter_expr(i: expr) -> expr:
    raise InvalidExpression(i)