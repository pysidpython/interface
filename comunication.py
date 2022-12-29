"""
Module for the functions that do the prints and make the connection with the user
"""
import tkinter as tk   
from tkinter.filedialog import askopenfilename
from pysid.io.csv_data import *
from pysid.interface import solve, plot

def initial_menu():
    print(f'Pysid(v0.1) - Identificação de sistemas')
    print("Escolha uma opção:")
    print("1 - Solução de minímos quadrados (MQ)")
    print("2 - Solução de minímos quadrados estendido (EMQ)")
    print("3 - Solução de minímos quadrados recursivo (RMQ)")
    print("4 - Informações relevantes")
    print("5 - Configurações")
    print("0 - Sair")
    cmd = int(input(">> "))
    if cmd >= 0 and cmd <= 5:
        return cmd
    else:
        print("*** Comando Inválido ***\n")
        return initial_menu()

def print_infos():
    print("- O seprador default é a vírgula.")
    print("- No .csv a ordem das colunas deve ser entradas(u), saídas(y)")
    print("- As ordens dos polinomios devem ser inteiros")
    print("- Utilize arquivos .csv ou .txt")
    print("- O minimos quadrados(MQ) e o minimos quadrados recursivo(MQR) devem dar resultados\n muito próximos, variam apenas na implementação")
    print("\n--------------\n")


def print_config_menu(config):
    # numero de alg sig
    # numero de treshold 
    # numero max de repetições
    # separador padrão do csv
    # numero de linhas a serem ignoradas no csv
    print("Escolha uma opção de configuração:")
    print("1 - Alterar separador padrão do csv\nAtual: ", config[0])
    print("2 - Quantidade de linha de dados a serem ignorados(pelo cabeçalho)\nAtual: ", config[1])
    print("3 - Numero de algarismos significativos a serem mostrados nos resultados\nAtual: ", config[2])
    print("4 - Numero máximo de reptições(Apenas para MQE)\nAtual: ", config[3])
    print("5 - Diferença miníma entre a soma quadratica de dois erros consecutivos necessaria para assumir-se que houve convergencia(em %)(Apenas para MQE)\nAtual: ", config[4])
    print("0 - Sair")
    cmd = int(input(">> "))
    if cmd >= 0 and cmd <= 5:
        return cmd
    else:
        print("*** Comando Inválido ***\n")
        return print_config_menu()

def change_config(cmd,config):
    if cmd == 1:
        print("Informe o novo separador:")
        config[cmd-1] = input("\n>> ")
    elif cmd == 2:
        print("Informe a quantidade de linha de dados a serem ignorados(pelo cabeçalho):")
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 3:
        print("Informe o numero de algarismos significativos a serem mostrados nos resultados:")
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 4:
        print("Informe o numero máximo de reptições a serem feitas(Apenas para MQE):") 
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 5:
        print("Informe a diferença miníma entre a soma quadratica de dois erros consecutivos necessaria para assumir-se que houve convergencia(em %):")
        config[cmd-1] = int(input("\n>> "))
    elif cmd == 0:
        pass
    print("\n *** Configurações salvas *** \n")
    
    return config
def sep_data(nu,ny,data):
    u = data[:,:nu]
    y = data[:,nu:ny+nu]
    return u,y

def get_order_polys(cmd):
    na = int(input("Ordem de A(q):\n>> "))
    nb = int(input("Ordem de B(q):\n>> "))
    if(cmd == 2):
        nc = int(input("Ordem de C(q):\n>> "))
    else:
        nc = 0
    nk = int(input("nk:\n>> "))
    return na,nb,nc,nk

def main():
    cmd = -1
    # sep, linhas ignorar, alg sig, max iterac, dif erro
    try:
        with open('config.txt','r') as f:
            config = f.readline()
            config = config.split('-')
            for i in range(4):
                config[i+1] = config[i+1]
            config = config[:-1]
            
    except:
        config = [",",1,4,100,0.05]
    filename = None
    repeat_file = False
    # print(config)
    while(cmd != 0):
        cmd = initial_menu()
        if cmd <= 3 and cmd != 0:
            #Abrir o seletor de arquivos
            if not repeat_file:
                file = False
                input("Precione ENTER para escolher um arquivo ")
                filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
                if filename is not None:
                    if filename.endswith('.csv') or filename.endswith('.txt'):
                        data = load_data(filename,delim=config[0],skip_rows=int(config[1]))
                        nu = int(input("Informe quantas colunas de entradas há na amostragem:\n>> "))
                        if nu > data.shape[1]-1:
                            print("***Valor inválido, não há colunas referentes a saída***\n")
                        else:
                            file = True #ok, tudo certo com o file
                            ny = data.shape[1]-nu
                            u,y = sep_data(nu,ny,data)
            if file:
                na, nb, nc, nk = get_order_polys(cmd)
                if   cmd == 1:
                    m = solve.mq_interface(na,nb,nk,u,y,prec=int(config[2]))
                    if nu == 1 and ny == 1:
                        p = input("Deseja plotar os dados?[Y/N]\n>> ")
                        if p == 'y' or p == 'Y':
                            plot.plot(m,u,y)
                elif cmd == 2:
                    m = solve.mqe_interface(na,nb,nc,nk,u,y,float(config[4])/100,int(config[3]),int(config[2]))
                    if nu == 1 and ny == 1:
                        p = input("Deseja plotar os dados?[Y/N]\n>> ")
                        if p == 'y' or p == 'Y':
                            plot.plot(m,u,y)
                elif cmd == 3:
                    solve.mqr_interface(na,nb,nk,u,y,int(config[2]))

                print("\n-------------------\n")
                repeat = input("Deseja usar os mesmos dados?[Y/N]\n>> ")
                if repeat == 'Y' or repeat == 'y':
                    repeat_file = True
                else:
                    repeat_file = False    
        elif cmd == 4:
            print_infos()
        elif cmd == 5:
           config = change_config(print_config_menu(config),config)
           with open('config.txt','w') as f:
               for item in config:
                   f.write(str(item)+"-")
           # print(config)

main()