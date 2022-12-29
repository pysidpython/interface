

from pysid.io.print import print_model
from pysid.identification.models import polymodel
from pysid.identification.pemethod import arx, emq
from pysid.identification.recursive import mqr
from pysid.io.csv_data import gen_data
from numpy.linalg import inv
from numpy import matmul,concatenate,ones,power

def mq_interface(na,nb,nk,u,y,prec=3):
    
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


def mqe_interface(na,nb,nc,nk,u,y,th,n_max,prec):
    m = emq(na, nb, nc, nk, u, y, th, n_max)
    print_model(m,prec=prec)
    # y_m = gen_data(m.A[0,0], m.B[0,0], u.shape[0], u, 0)[:,1]
    # print(y_m[:15])
    # print(y[:15])
    # soma = power((y-y_m),2)
    # soma = soma.sum()/y.shape[0]
    
    # print(soma.max())
    # print(soma)
    # print(f'Cost function per sample: {soma:.7f}')
    # print("Infos de saída(matriz de covariancia) e tal")
    # print("Infos de regressão(n de amostras, sis mimo..)\n")
    return m

def mqr_interface(na,nb,nk,u,y,prec):
    m = mqr(na,nb,nk,u,y)
    print_model(m,prec=prec)
    # print("Infos de saída(matriz de covariancia) e tal")
    # print("Infos de regressão(n de amostras, sis mimo..)\n")
    return m
