from Yacc import *


AbreFicheiro = input("!!Introduza o nome do ficheiro que quer abrir!! >> ")
with open(AbreFicheiro, 'r') as r:
    texto = r.read()
    parser.parse(texto)
    if parser.sucesso:
        print("-----------------------Ficheiro Compilado--------------------------------")
        CriaFicheiro = input("!!Introduza o nome do ficheiro que quer criar!! >> ")
        with open(CriaFicheiro, 'w') as w:
            w.write(parser.vmc + "\n\n\nPara efeitos de visualizacao das variaveis:\n" + str(parser.variaveis))
        w.close()
    else:
        print("---------------------------Ficheiro Nao Compilado-----------------------------------------")        
r.close()