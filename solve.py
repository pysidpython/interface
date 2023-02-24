
from pysid.io.print import print_model
from pysid.identification.models import polymodel
from pysid.identification.pemethod import arx, els
from pysid.identification.recursive import rls
from pysid.io.csv_data import gen_data
from numpy.linalg import inv
from numpy import matmul,concatenate,ones,power

def ls_interface(na,nb,nk,u,y,prec=3):
    
    ny = y.shape[1]
    nu = u.shape[1]
    
    na = ones((ny,ny),dtype=int)*na
    nb = ones((ny,nu),dtype=int)*nb
    nk = ones((ny,nu),dtype=int)*nk
    
    m = arx(na,nb,nk,u,y)
    print_model(m,prec=prec)
    print(m.gen_model_string().split('\n')[0] ,end='')
    print(f' identificado com {u.shape[0]} amostras')
    print(f'para um total de {m.nparam} parâmetros',end='\n\n')
    return m


def els_interface(na,nb,nc,nk,u,y,th,n_max,prec):
    m = els(na, nb, nc, nk, u, y, th, n_max)
    print_model(m,prec=prec)
   
    # TODO : print(f'Cost function per sample: ...')
    # print("Infos de saída(matriz de covariancia) e tal")
    # print("Infos de regressão(n de amostras, sis mimo..)\n")
    return m

def els_interface(na,nb,nk,u,y,prec):
    m = rls(na,nb,nk,u,y)
    print_model(m,prec=prec)
    # TODO : print(f'Cost function per sample: ...')
    # print("Infos de saída(matriz de covariancia) e tal")
    # print("Infos de regressão(n de amostras, sis mimo..)\n")
    return m
