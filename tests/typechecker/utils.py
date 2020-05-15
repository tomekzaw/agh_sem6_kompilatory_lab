from Mparser import parser
from TypeChecker import TypeChecker


def typechecker_passes(text: str):
    ast = parser.parse(text)
    typechecker = TypeChecker()
    typechecker.visit(ast)
    return typechecker.errorok


def typechecker_fails(text: str):
    ast = parser.parse(text)
    typechecker = TypeChecker()
    typechecker.visit(ast)
    return not typechecker.errorok
