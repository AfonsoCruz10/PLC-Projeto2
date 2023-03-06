import ply.lex as lex
import sys

tokens = [
'INT', 'MATRIZ', 'ARRAY', 
'IF', 'ELSE', 'WHILE', 
'SCAN', 'PRINTT', 'PRINTV',
'VAR', 'NUM',
'MAIORIG', 'MENORIG', 'IGUALDADE', 'DIFERENTE', 'TEXTO'
]

literals = ['(', ')', '[', ']', ',', '{','}','=','+','-','*','/','%','>','<','~',"|",'&']

def t_MAIORIG(t):
    r'>=' 
    return t

def t_MENORIG(t):
    r'<='
    return t

def t_IGUALDADE(t):
    r'=='
    return t

def t_DIFERENTE(t):
    r'!='
    return t

def t_INT(t):
    r'(?i:int)'
    return t

def t_ARRAY(t):
    r'(?i:array)'
    return t

def t_MATRIZ(t):
    r'(?i:matriz)'
    return t

def t_IF (t):
    r'(?i:if)'
    return t

def t_ELSE (t):
    r'(?i:else)'
    return t

def t_WHILE (t):
    r'(?i:while)'
    return t

def t_SCAN (t):
    r'(?i:scan)'
    return t

def t_PRINTT (t):
    r'(?i:printt)'
    return t

def t_PRINTV (t):
    r'(?i:printv)'
    return t

def t_VAR(t):
    r'[a-zA-Z]+'
    return t

def t_TEXTO(t):    
    r'".+"'
    return t

def t_NUM(t):
    r'\d+'
    return t

t_ignore = ' \r\n\t'

def t_error(t):
    print('Illegal character: ' + t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

'''
for linha in sys.stdin:
    lexer.input(linha) 
    tok = lexer.token()
    while tok:
        print(tok)
        tok = lexer.token()
'''
        