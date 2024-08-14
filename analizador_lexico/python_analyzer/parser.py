import ply.yacc as yacc
from analizador_lexico.python_analyzer.lexer import init_lexer, lexer
from lexer import tokens, parse_fstring

# Definición del analizador sintáctico
def p_program(p):
    '''program : statement_list
               | empty'''
    p[0] = ('program', p[1])
    
def p_empty(p):
    'empty :'
    pass

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : simple_statement
                 | compound_statement
                 | function_def
                 | class_def'''
    p[0] = p[1]

def p_simple_statement(p):
    '''simple_statement : assignment_statement NEWLINE
                        | return_statement NEWLINE
                        | print_statement NEWLINE
                        | expression_statement NEWLINE'''
    p[0] = p[1]

def p_compound_statement(p):
    '''compound_statement : if_statement
                          | while_statement
                          | for_statement'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : ID EQUALS expression
                            | attribute EQUALS expression'''
    p[0] = ('assignment', p[1], p[3])

def p_return_statement(p):
    '''return_statement : RETURN expression'''
    p[0] = ('return', p[2])

def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression RPAREN
                       | PRINT LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = ('print', p[3])
    else:
        p[0] = ('print', None)

def p_expression_statement(p):
    '''expression_statement : expression
                            | function_call'''
    p[0] = ('expression_statement', p[1])

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_if_statement(p):
    '''if_statement : IF expression COLON NEWLINE INDENT statement_list DEDENT
                    | IF expression COLON NEWLINE INDENT statement_list DEDENT ELSE COLON NEWLINE INDENT statement_list DEDENT'''
    if len(p) == 8:
        p[0] = ('if', p[2], p[6])
    else:
        p[0] = ('if-else', p[2], p[6], p[12])

def p_while_statement(p):
    '''while_statement : WHILE expression COLON NEWLINE INDENT statement_list DEDENT'''
    p[0] = ('while', p[2], p[6])

def p_for_statement(p):
    '''for_statement : FOR ID IN expression COLON NEWLINE INDENT statement_list DEDENT'''
    p[0] = ('for', p[2], p[4], p[8])

def p_function_def(p):
    '''function_def : DEF ID LPAREN parameter_list RPAREN COLON NEWLINE INDENT statement_list DEDENT'''
    p[0] = ('function_def', p[2], p[4], p[9])

def p_class_def(p):
    '''class_def : CLASS ID COLON NEWLINE INDENT class_body DEDENT'''
    p[0] = ('class_def', p[2], p[6])

def p_class_body(p):
    '''class_body : statement_list'''
    p[0] = p[1]

def p_parameter_list(p):
    '''parameter_list : ID
                      | parameter_list COMMA ID
                      | '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression(p):
    '''expression : arithmetic_expr
                  | comparison_expr
                  | function_call
                  | method_call
                  | attribute
                  | lambda_expr
                  | list_expr
                  | fstring_expr
                  | STRING'''
    p[0] = p[1]

def p_lambda_expr(p):
    '''lambda_expr : LAMBDA parameter_list COLON expression'''
    p[0] = ('lambda', p[2], p[4])

def p_list_expr(p):
    '''list_expr : LBRACKET expression_list RBRACKET
                 | LBRACKET RBRACKET'''
    if len(p) == 4:
        p[0] = ('list', p[2])
    else:
        p[0] = ('list', [])

def p_dict_expr(p):
    '''dict_expr : LBRACE dict_items RBRACE'''
    p[0] = ('dict', p[2])

def p_dict_items(p):
    '''dict_items : expression COLON expression
                  | dict_items COMMA expression COLON expression'''
    if len(p) == 4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = p[1] + [(p[3], p[5])]

def p_fstring_expr(p):
    '''fstring_expr : FSTRING'''
    components = parse_fstring(p[1])
    p[0] = ('fstring', components)

def p_arithmetic_expr(p):
    '''arithmetic_expr : term
                       | arithmetic_expr PLUS term
                       | arithmetic_expr MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | NUMBER
              | STRING
              | ID
              | attribute
              | function_call'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_function_call(p):
    '''function_call : ID LPAREN expression_list RPAREN
                     | ID LPAREN RPAREN
                     | ID LPAREN lambda_expr COMMA expression RPAREN'''
    if len(p) == 5:
        p[0] = ('function_call', p[1], p[3])
    elif len(p) == 4:
        p[0] = ('function_call', p[1], [])
    else:
        p[0] = ('function_call', p[1], [p[3], p[5]])

def p_method_call(p):
    '''method_call : ID DOT ID LPAREN expression_list RPAREN
                   | ID DOT ID LPAREN RPAREN'''
    if len(p) == 7:
        p[0] = ('method_call', p[1], p[3], p[5])
    else:
        p[0] = ('method_call', p[1], p[3], [])

def p_attribute(p):
    '''attribute : ID DOT ID'''
    p[0] = ('attribute', p[1], p[3])

def p_comparison_expr(p):
    '''comparison_expr : arithmetic_expr comparison_op arithmetic_expr'''
    p[0] = (p[2], p[1], p[3])

def p_comparison_op(p):
    '''comparison_op : EQ
                     | NE
                     | LT
                     | LE
                     | GT
                     | GE'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value '{p.value}', line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")

# Construir el parser con modo de depuración
parser = yacc.yacc(debug=True)
parser.error = 0