import ply.yacc as yacc
from Lex import tokens


def p_Prog(p):
    "Prog : Dcls" 
    parser.vmc = f'{p[1]}'

def p_Prog_Corpo(p):
    "Prog : Corpo"    
    parser.vmc = f'START\n{p[1]}STOP'

def p_Prog_Dcls(p):
    "Prog : Dcls Corpo"
    parser.vmc = f'{p[1]}START\n{p[2]}STOP'

def p_Dcls(p):
    "Dcls : Dcl"
    p[0] = f'{p[1]}'

def p_Dcls_Dcls(p):
    "Dcls : Dcl Dcls"
    p[0] = f'{p[1]}{p[2]}'

def p_Dcl_Var(p):
    "Dcl : INT VAR"
    if p[2] not in p.parser.variaveis:
        lista = []
        lista.append(0)
        lista.append(p.parser.gp)
        lista.append("int")
        p.parser.variaveis[p[2]] = lista
        p.parser.gp += 1
        p[0] = f'PUSHI 0\n'
    else:
        print("ERRO!! : Variavel ja atribuida")
        p.parser.sucesso = False

def p_Dcl_Atr_Var(p):
    "Dcl : INT VAR '=' NUM"
    if p[2] not in p.parser.variaveis:
        lista = []
        lista.append(int(p[4]))
        lista.append(p.parser.gp)
        lista.append("int")
        p.parser.variaveis[p[2]] = lista
        p.parser.gp += 1
        p[0] = f'PUSHI {p[4]}\n'
    else:
        print("ERRO!! : Variavel ja atribuida")
        p.parser.sucesso = False 

def p_Dcl_Array(p):
    "Dcl : ARRAY '(' VAR ',' NUM ')'"
    if p[3] not in p.parser.variaveis:
        lista = []
        lista.append(list(0 for i in range(int(p[5]))))
        lista.append(p.parser.gp)
        lista.append("array")
        p.parser.gp += int(p[5])
        p.parser.variaveis[p[3]] = lista
        p[0] = f'PUSHN {p[5]}\n'
    else:
        print("ERRO!! : Variavel ja atribuida")
        p.parser.sucesso = False

def p_Dcl_Matriz(p):
    "Dcl : MATRIZ '(' VAR ',' NUM ',' NUM ')'"        
    if p[3] not in p.parser.variaveis:
        lista = []
        lista.append(list(list(0 for i in range(int(p[7]))) for j in range (int(p[5]))))
        lista.append(p.parser.gp)
        lista.append("matriz")
        p.parser.gp += int(p[5]) * int(p[7])
        p.parser.variaveis[p[3]] = lista
        p[0] = f'PUSHN {str(int(p[5]) * int(p[7]))}\n'
    else:
        print("ERRO!! : Variavel ja atribuida")
        p.parser.sucesso = False    

def p_Dcl_PrinT(p):                
    "Dcl : Print"
    p[0] = p[1]

def p_Dcl_Scan(p):
    "Dcl : Scan"
    p[0] = p[1]     

def p_Corpo(p):
    "Corpo : Prox"
    p[0] = f'{p[1]}'

def p_Corpo_Prox(p):
    "Corpo : Prox Corpo"
    p[0] = f'{p[1]}{p[2]}'

def p_Prox_Stats(p):
    "Prox : '{' Stats '}'"
    p[0] = f'{p[2]}'

def p_Stats_Stat(p):
    "Stats : Stat"
    p[0] = f'{p[1]}'

def p_Stats_Stats_Stat(p):
    "Stats : Stats Stat"
    p[0] = f'{p[1]}{p[2]}'  

def p_Stat_Atr(p):
    "Stat : Atr"
    p[0] = p[1]

def p_Stat_If(p):
    "Stat : If"
    p[0] = p[1]

def p_Stat_While(p):
    "Stat : While"
    p[0] = p[1]    

def p_Stat_Scan(p):
    "Stat : Scan"
    p[0] = p[1]    

def p_Stat_Print(p):
    "Stat : Print"
    p[0] = p[1]    

def p_Atr_array(p):
    "Atr : VAR '[' Exp ']' '=' Exp"
    if p[1] in p.parser.variaveis:
        if p.parser.variaveis.get(p[1])[2] == "array":
            p[0] = f'PUSHGP\nPUSHI {p.parser.variaveis.get(p[1])[1]}\nPADD\n{p[3]}{p[6]}STOREN\n'
        else:
            print(f'A variavel {p[1]} é um array')
            p.parser.sucesso = False
    else:
        print("Variavel nao existe")
        p.parser.sucesso = False  

def p_Atr_matriz(p):
    "Atr : VAR '[' Exp ']' '[' Exp ']' '=' Exp" 
    if p[1] in p.parser.variaveis:
        if p.parser.variaveis.get(p[1])[2] == "matriz":
            p[0] = f'PUSHGP\nPUSHI {p.parser.variaveis.get(p[1])[1]}\nPADD\n{p[3]}PUSHI {len(p.parser.variaveis.get(p[1])[0][0])}\nMUL\n{p[6]}ADD\n{p[9]}STOREN\n'
        else:
            print(f'A variavel {p[1]} é uma matriz')
            p.parser.sucesso = False
    else:
        print("Variavel nao existe")
        p.parser.sucesso = False

def p_Atr_var(p):         
    "Atr : VAR '=' Exp"
    if p[1] in p.parser.variaveis:
        if p.parser.variaveis.get(p[1])[2] == "int":
            p[0] = f'{p[3]}STOREG {p.parser.variaveis.get(p[1])[1]}\n'
        else:
            print(f'A variavel {p[1]} é um inteiro')
            p.parser.sucesso = False
    else:
        print("Variavel nao existe")
        p.parser.sucesso = False 

def p_If_Stats(p):                               
    "If : IF '(' Cond ')' '{' Stats '}'"
    p[0] = f'{p[3]}JZ END{p.parser.count}\n{p[6]}END{p.parser.count}:\n'
    p.parser.count += 1

def p_If_Else(p):                                
    "If : IF '(' Cond ')' '{' Stats '}' ELSE '{' Stats '}'"
    p[0] = f'{p[3]}JZ END{p.parser.count}\n{p[6]}JUMP ENDT{p.parser.count}\nEND{p.parser.count}:\n{p[10]}ENDT{p.parser.count}:\n'
    p.parser.count += 1                                         

def p_While(p):
    "While : WHILE '(' Cond ')' '{' Stats '}'"
    p[0] = f'WHILE{p.parser.count}:\n{p[3]}JZ END{p.parser.count}\n{p[6]}JUMP WHILE{p.parser.count}\nEND{p.parser.count}:\n'
    p.parser.count += 1

def p_Exp_OpA(p):
    "Exp : OpA"
    p[0] = p[1] 

def p_Exp_OpR(p):
    "Exp : OpR"
    p[0] = p[1]  

def p_Exp_OpL(p):
    "Exp : OpL"
    p[0] = p[1]        

def p_Exp_Term(p):
    "Exp : Term"
    p[0] = p[1]

def p_Cond_OpL(p):
    "Cond : OpL"
    p[0] = p[1]

def p_Cond_OpR(p):
    "Cond : OpR"
    p[0] = p[1]

def p_OpL_e(p):
    "OpL : '&' '(' OpR ',' OpR ')'"
    p[0] = f'{p[3]}{p[5]}SUP\n'

def p_OpL_nao(p):
    "OpL : '~' OpR"
    p[0] = f'{p[2]}NOT\n'  

def p_OpL_ou(p):
    "OpL : '|' '(' OpR ',' OpR ')'"
    p[0] = f'{p[3]}{p[5]}OR\n'                        

def p_OpR_maior(p):
    "OpR : '>' '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}SUP\n'

def p_OpR_maiorig(p):
    "OpR : MAIORIG '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}SUPEQ\n'

def p_OpR_menor(p):
    "OpR : '<' '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}INF\n'

def p_OpR_menorig(p):
    "OpR : MENORIG '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}INFEQ\n'     

def p_OpR_igualdade(p):
    "OpR : IGUALDADE '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}Equal\n'

def p_OpR_diferente(p):
    "OpR : DIFERENTE '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}Equal\nNOT\n'

def p_OpA_soma(p):
    "OpA : '+' '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}ADD\n'

def p_OpA_dif(p):
    "OpA : '-' '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}SUB\n'

def p_OpA_mult(p):
    "OpA : '*' '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}MUL\n'

def p_OpA_div(p):
    "OpA : '/' '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}DIV\n'

def p_OpA_resto(p):
    "OpA : '%' '(' Exp ',' Exp ')'"
    p[0] = f'{p[3]}{p[5]}MOD\n'

def p_Term_NUM(p):  
    "Term : NUM"
    p[0] = f'PUSHI {p[1]}\n'


def p_Term_VAR(p):       
    "Term : VAR"
    if p[1] in p.parser.variaveis:
        p[0] = f'PUSHG {p.parser.variaveis.get(p[1])[1]}\n'
    else:
        print("Variavel atribuida nao existe")
        p.parser.sucesso = False

def p_Term_ARRAY(p):              
    "Term : VAR '[' Term ']'"
    if p[1] in p.parser.variaveis:
        p[0] = f'PUSHGP\nPUSHI {p.parser.variaveis.get(p[1])[1]}\nPADD\n{p[3]}LOADN\n'
    else:
        print("Variavel atribuida nao existe")
        p.parser.sucesso = False   

def p_Term_MATRIZ(p):                             
    "Term : VAR '[' Term ']' '[' Term ']'"
    if p[1] in p.parser.variaveis:
        p[0] = f'PUSHGP\nPUSHI {p.parser.variaveis.get(p[1])[1]}\nPADD\n{p[3]}{p[6]}ADD\nLOADN\n' 
    else:
        print("Variavel atribuida nao existe")
        p.parser.sucesso = False

def p_Scan_var(p):
    "Scan : SCAN '(' VAR ')'"
    if p[3] in p.parser.variaveis:
        p[0] = f'READ\nATOI\nSTOREG {p.parser.variaveis.get(p[3])[1]}\n'
    else:
        print("Variavel não existe")
        p.parser.sucesso = False    

def p_Scan_array(p):
    "Scan : SCAN '(' VAR '[' NUM ']' ')'"
    if p[3] in p.parser.variaveis:
        p[0] = f'READ\nATOI\nSTOREG {p.parser.variaveis.get(p[3])[1] + int(p[5])}\n'
    else:
        print("Array não existe")
        p.parser.sucesso = False

def p_Scan_matriz(p):
    "Scan : SCAN '(' VAR '[' NUM ']' '[' NUM ']' ')'"
    if p[3] in p.parser.variaveis:
        tam = len(p.parser.variaveis.get(p[3])[0][0]) * int(p[5]) + int(p[8]) + p.parser.variaveis.get(p[3])[1]
        p[0] = f'READ\nATOI\nSTOREG {int(tam)}\n'                        
    else:
        print("Matriz não existe")
        p.parser.sucesso = False

def p_Print_T(p):
    "Print : PRINTT '(' TEXTO ')'"
    p[0] = f'PUSHS{p[3]}\nWRITES\nWRITELN\n'

def p_Print_V(p):
    "Print : PRINTV '(' Term ')'"
    p[0] = f'{p[3]}WRITEI\nWRITELN\n'                     



def p_error(p):
    print('Syntax error!')
    parser.sucesso = False


parser = yacc.yacc() 

parser.sucesso = True
parser.vmc = ""
parser.variaveis = {}
parser.gp = 0
parser.count = 0 # para entrada e saida de condiçoes