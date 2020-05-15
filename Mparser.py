#!/usr/bin/python

import sys
import ply.yacc as yacc
from scanner import tokens, lexer, find_tok_column  # noqa
from AST import *
from TreePrinter import TreePrinter  # noqa

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ('nonassoc', '<', '>', 'LTE', 'GTE', 'EQ', 'NEQ'),
    ('nonassoc', ':'),
    ('left', '+', '-', 'DOTADD', 'DOTSUB'),
    ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
    ('right', 'UMINUS'),
    ('left', "'"),
)


def p_error(p):
    if p is None:
        print('Unexpected end of input')
    else:
        column = find_tok_column(p)
        print(f"Syntax error at line {p.lineno}, column {column}: LexToken({p.type}, '{p.value}')")


def p_program(p):
    """program : instructions"""
    p[0] = Program(p[1])


def p_instructions(p):
    """instructions : instructions instruction"""
    p[0] = Instructions(p[1].instructions + [p[2]])


def p_instructions_empty(p):
    """instructions : """
    p[0] = Instructions([])


def p_instruction_block(p):
    """instruction : '{' instructions '}'"""
    p[0] = p[2]


# def p_instruction_empty(p):
#     """instruction : ';' """
#     p[0] = EmptyInstruction()


def p_instruction_if(p):
    """instruction : IF '(' condition ')' instruction %prec IFX"""
    p[0] = If(p[3], p[5])


def p_instruction_if_else(p):
    """instruction : IF '(' condition ')' instruction ELSE instruction"""
    p[0] = If(p[3], p[5], p[7])


def p_instruction_for(p):
    """instruction : FOR variable '=' range instruction"""
    p[0] = For(p[2], p[4], p[5])


def p_instruction_while(p):
    """instruction : WHILE '(' condition ')' instruction"""
    p[0] = While(p[3], p[5])


def p_condition(p):
    """condition : expression EQ expression
                 | expression NEQ expression
                 | expression LTE expression
                 | expression GTE expression
                 | expression '<' expression
                 | expression '>' expression"""
    p[0] = Condition(p[2], p[1], p[3])


def p_variable(p):
    """variable : ID"""
    p[0] = Variable(p[1])


def p_range(p):
    """range : expression ':' expression"""
    p[0] = Range(p[1], p[3])


def p_instruction_statement(p):
    """instruction : statement ';'"""
    p[0] = p[1]


def p_statement_break(p):
    """statement : BREAK"""
    p[0] = Break()


def p_statement_continue(p):
    """statement : CONTINUE"""
    p[0] = Continue()


def p_statement_return(p):
    """statement : RETURN"""
    p[0] = Return()


def p_statement_return_expression(p):
    """statement : RETURN expression"""
    p[0] = Return(p[2])


def p_statement_print(p):
    """statement : PRINT expression_list"""
    p[0] = Print(p[2])


def p_statement_assignment(p):
    """statement : lvalue '=' expression
                 | lvalue ADDASSIGN expression
                 | lvalue SUBASSIGN expression
                 | lvalue MULASSIGN expression
                 | lvalue DIVASSIGN expression"""
    p[0] = Assignment(p[2], p[1], p[3])


def p_lvalue_variable(p):
    """lvalue : variable"""
    p[0] = p[1]


def p_lvalue_reference(p):
    """lvalue : variable '[' expression_list ']'"""
    p[0] = Reference(p[1], p[3])


def p_expression_binary(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""
    p[0] = BinExpr(p[2], p[1], p[3])


def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = UnaryExpr(p[1], p[2])


def p_expression_transpose(p):
    """expression : expression "'" """
    p[0] = UnaryExpr(p[2], p[1])


def p_expression_group(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_expression_lvalue(p):
    """expression : lvalue"""
    p[0] = p[1]


def p_expression_range(p):
    """expression : range"""
    p[0] = p[1]


def p_expression_intnum(p):
    """expression : INTNUM"""
    p[0] = IntNum(p[1])


def p_expression_floatnum(p):
    """expression : FLOATNUM"""
    p[0] = FloatNum(p[1])


def p_expression_string(p):
    """expression : STRING"""
    p[0] = String(p[1])


def p_expression_list(p):
    """expression_list : expression_list ',' expression"""
    p[0] = p[1] + [p[3]]


def p_expression_list_single(p):
    """expression_list : expression"""
    p[0] = [p[1]]


def p_expression_list_empty(p):
    """expression_list : """
    p[0] = []


def p_vector(p):
    """expression : '[' expression_list ']'"""
    p[0] = Vector(p[2])


# def p_matrix(p):
#     """expression : '[' matrix_rows ']'"""
#     p[0] = Matrix(p[2])


# def p_matrix_rows(p):
#     """matrix_rows : matrix_rows ';' expression_list"""
#     p[0] = p[1] + [p[3]]


# def p_matrix_rows_single(p):
#     """matrix_rows : expression_list"""
#     p[0] = [p[1]]


def p_eye_1(p):
    """expression : EYE '(' expression ')'"""
    p[0] = Eye(p[3])


def p_eye_2(p):
    """expression : EYE '(' expression ',' expression ')'"""
    p[0] = Eye(p[3], p[5])


def p_zeros_1(p):
    """expression : ZEROS '(' expression ')'"""
    p[0] = Zeros(p[3])


def p_zeros_2(p):
    """expression : ZEROS '(' expression ',' expression ')'"""
    p[0] = Zeros(p[3], p[5])


def p_ones_1(p):
    """expression : ONES '(' expression ')'"""
    p[0] = Ones(p[3])


def p_ones_2(p):
    """expression : ONES '(' expression ',' expression ')'"""
    p[0] = Ones(p[3], p[5])


parser = yacc.yacc()


def make_parser(start=None):
    return yacc.yacc(start=start)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    ast = parser.parse(text, lexer=lexer)
    if not parser.errorok:
        raise SystemExit

    ast.printTree()
